// GeneralizationEngine.swift
//
// iOS native port of framework/generalization.py + the deterministic half of
// framework/extraction.py (Phase 1 scope: no on-device LLM yet -- see the
// edge-runtime benchmark plan). Entity detection uses Apple's NaturalLanguage
// framework (NLTagger) instead of spaCy, so it is genuinely on-device with no
// Python dependency. Relation extraction and the LLM fluency pass are
// explicitly out of scope for this port (Phase 2, not started).
//
// The mapping/substitution logic mirrors the Python implementation closely,
// including the lookaround boundary fix found live during the N=50 relation-
// aware evaluation (a plain \b anchor fails to match entities that start or
// end in punctuation, e.g. "Mtg." -- see framework/generalization.py's
// apply_mapping docstring for the full story). NSRegularExpression's ICU
// engine supports the same (?<!\w)/(?!\w) lookaround Python's re module does,
// so this port uses the identical pattern rather than \b.

import Foundation
import NaturalLanguage

enum EntityType: String, Codable {
    case person = "PERSON"
    case org = "ORG"
    case location = "LOCATION"
    case email = "EMAIL"
}

struct Entity: Codable {
    let text: String
    let type: EntityType
}

// Same pattern as validation/02_Privacy_Baseline_Profiling.ipynb and
// framework/extraction.py's EMAIL_REGEX, so all three implementations agree
// on what counts as an email address.
private let emailRegex = try! NSRegularExpression(
    pattern: #"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"#
)

/// Best-effort person-name guess from an email local part, mirroring
/// framework/extraction.py's _local_part_to_name. Ensures a person's email
/// address maps to THEIR placeholder rather than a generic email placeholder
/// -- the exact fix for the CC-list sample that leaked 29 addresses in the
/// Python evaluation's worst outlier before this was added.
func localPartToName(_ email: String) -> String? {
    guard let atIndex = email.firstIndex(of: "@") else { return nil }
    let local = String(email[email.startIndex..<atIndex])
    let parts = local
        .split(whereSeparator: { ".-_".contains($0) })
        .map(String.init)
        .filter { !$0.isEmpty && !$0.allSatisfy(\.isNumber) }
    guard !parts.isEmpty else { return nil }
    return parts.map { $0.prefix(1).uppercased() + $0.dropFirst().lowercased() }.joined(separator: " ")
}

/// Canonical dedupe key for person surfaces, mirroring extraction.py's
/// _person_key: "Maureen.riter" and "Maureen Riter" are the same identity.
private func personKey(_ surface: String) -> String {
    let tokens = surface.lowercased()
        .split(whereSeparator: { ".\u{20}_-,".contains($0) })
        .map(String.init)
        .sorted()
    return tokens.joined(separator: " ")
}

enum EntityExtraction {
    /// Merged deterministic entity extraction: NLTagger PERSON/ORG/LOCATION
    /// spans + regex email addresses (+ the person hidden inside each address).
    /// No LLM merge pass in Phase 1 -- see file header.
    static func extract(from text: String) -> [Entity] {
        var byKey: [String: Entity] = [:]

        func add(_ rawSurface: String, _ type: EntityType) {
            let surface = rawSurface
                .replacingOccurrences(of: ">", with: " ")
                .replacingOccurrences(of: "|", with: " ")
                .trimmingCharacters(in: .whitespacesAndNewlines)
                .trimmingCharacters(in: CharacterSet(charactersIn: "'\" \t,;:"))
            guard surface.count >= 2 else { return }
            let key = type == .person ? personKey(surface) : surface.lowercased()
            if byKey[key] == nil {
                byKey[key] = Entity(text: surface, type: type)
            }
        }

        // 1. Email addresses, and the person names hidden inside them.
        let fullRange = NSRange(text.startIndex..<text.endIndex, in: text)
        emailRegex.enumerateMatches(in: text, range: fullRange) { match, _, _ in
            guard let match, let range = Range(match.range, in: text) else { return }
            let email = String(text[range])
            add(email, .email)
            if let name = localPartToName(email) {
                add(name, .person)
            }
        }

        // 2. NLTagger PERSON / ORG / LOCATION spans. NLTagger's modern API takes
        // and returns Swift String.Index ranges directly (not NSRange).
        let tagger = NLTagger(tagSchemes: [.nameType])
        tagger.string = text
        let options: NLTagger.Options = [.omitWhitespace, .omitPunctuation, .joinNames]
        tagger.enumerateTags(in: text.startIndex..<text.endIndex, unit: .word, scheme: .nameType, options: options) { tag, range in
            guard let tag else { return true }
            let surface = String(text[range])
            switch tag {
            case .personalName: add(surface, .person)
            case .organizationName: add(surface, .org)
            case .placeName: add(surface, .location)
            default: break
            }
            return true
        }

        return Array(byKey.values)
    }
}

enum Generalization {
    /// Placeholder vocabulary per type -- mirrors _TYPE_TEMPLATES in
    /// generalization.py. Persons get stable letter labels because
    /// distinguishing individuals from each other is retained utility;
    /// other types get an indefinite generic description because their
    /// individual identity is exactly the leak.
    private static func genericPlaceholder(for type: EntityType) -> String {
        switch type {
        case .org: return "an internal organizational unit"
        case .location: return "an external location"
        case .email: return "a redacted email address"
        case .person: return "" // handled specially
        }
    }

    /// Assign one placeholder per entity. Mirrors build_mapping in
    /// generalization.py (Phase 1 scope: no relation-derived role hints,
    /// since relation extraction is Phase 2 / not built on-device yet).
    static func buildMapping(_ entities: [Entity]) -> [String: String] {
        var mapping: [String: String] = [:]
        var personLabelBySurface: [String: String] = [:]

        let persons = entities.filter { $0.type == .person }
        let letters = Array("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for (i, ent) in persons.enumerated() {
            let label = i < letters.count ? "Person-\(letters[i])" : "Person-\(i + 1)"
            mapping[ent.text] = label
            personLabelBySurface[ent.text.lowercased()] = label
        }

        var perTypeCount: [EntityType: Int] = [:]
        for type in [EntityType.org, .location] {
            perTypeCount[type] = entities.filter { $0.type == type }.count
        }
        var seenIndex: [EntityType: Int] = [:]

        for ent in entities {
            switch ent.type {
            case .person:
                continue // already assigned above
            case .email:
                if let owner = localPartToName(ent.text),
                   let label = personLabelBySurface[owner.lowercased()] {
                    mapping[ent.text] = "[\(label)'s address]"
                } else {
                    mapping[ent.text] = genericPlaceholder(for: .email)
                }
            case .org, .location:
                let base = genericPlaceholder(for: ent.type)
                let total = perTypeCount[ent.type] ?? 1
                if total <= 1 {
                    mapping[ent.text] = base
                } else {
                    let idx = (seenIndex[ent.type] ?? 0) + 1
                    seenIndex[ent.type] = idx
                    mapping[ent.text] = "\(base) (\(idx))"
                }
            }
        }
        return mapping
    }

    /// Deterministic substitution: longest entity surface first, case-
    /// insensitive, boundary-anchored via lookaround (not \b -- see file
    /// header for why). Email surfaces match unanchored since '@'/'.'
    /// characters break lookaround-adjacent-word semantics at their edges
    /// no more cleanly than \b would, and they're distinctive enough not to
    /// need it.
    static func applyMapping(_ text: String, _ mapping: [String: String]) -> String {
        var result = text
        let sortedSurfaces = mapping.keys.sorted { $0.count > $1.count }
        for surface in sortedSurfaces {
            guard let replacement = mapping[surface] else { continue }
            let escaped = NSRegularExpression.escapedPattern(for: surface)
            let pattern = surface.contains("@") ? escaped : "(?<!\\w)\(escaped)(?!\\w)"
            guard let regex = try? NSRegularExpression(pattern: pattern, options: [.caseInsensitive]) else { continue }
            let range = NSRange(result.startIndex..<result.endIndex, in: result)
            result = regex.stringByReplacingMatches(in: result, range: range, withTemplate: NSRegularExpression.escapedTemplate(for: replacement))
        }
        return result
    }

    /// Full generalization of one document. No LLM fluency pass in Phase 1
    /// (see file header) -- output is the direct result of deterministic
    /// substitution, which is also therefore trivially leak-free by
    /// construction (nothing to re-introduce a leak).
    static func generalize(_ text: String) -> (generalized: String, entities: [Entity], mapping: [String: String]) {
        let entities = EntityExtraction.extract(from: text)
        let mapping = buildMapping(entities)
        let generalized = applyMapping(text, mapping)
        return (generalized, entities, mapping)
    }
}
