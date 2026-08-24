package com.beyondredaction.edgeruntimebenchmark

// GeneralizationEngine.kt
//
// Android native port of framework/generalization.py + the deterministic half
// of framework/extraction.py (Phase 1 scope: no on-device LLM yet -- see the
// edge-runtime benchmark plan).
//
// Entity detection here is a DIFFERENT approach than the iOS port, and this
// difference is deliberate and documented, not accidental: Google's ML Kit
// Entity Extraction API only covers structured entities (dates, addresses,
// phone numbers), not general PERSON/ORG/LOCATION NER comparable to spaCy or
// Apple's NLTagger, and using it would require an online model download the
// first time it runs, which conflicts with a genuinely on-device benchmark.
// Android's AOSP TextClassifier has the same structured-entity limitation.
// Per the benchmark plan's documented fallback, this uses a lightweight
// deterministic heuristic instead: a capitalized-word-sequence detector for
// PERSON entities, plus the same EMAIL_REGEX used by iOS and the Python
// framework. This is a weaker detector than NLTagger/spaCy by design --
// the Phase 1 goal is measuring the deterministic mapping/substitution
// pipeline's latency and memory footprint, not NER quality parity across
// platforms. ORG/LOCATION detection is intentionally out of scope here
// rather than faked with an unreliable heuristic.

data class Entity(val text: String, val type: EntityType)

enum class EntityType { PERSON, EMAIL }

// Same pattern as validation/02_Privacy_Baseline_Profiling.ipynb,
// framework/extraction.py's EMAIL_REGEX, and the iOS port -- all three
// implementations agree on what counts as an email address.
private val EMAIL_REGEX = Regex("""[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}""")

// Deliberately small stoplist for words that capitalize at sentence-start or
// as calendar terms and would otherwise false-positive as PERSON entities --
// the same category of fix the Python framework needed live (calendar words
// matching "Lastname, Firstname" patterns; see framework/extraction.py).
private val STOPWORDS = setOf(
    "the", "and", "for", "with", "from", "this", "that", "monday", "tuesday",
    "wednesday", "thursday", "friday", "saturday", "sunday", "january",
    "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "subject", "re", "fw",
    "fwd", "calendar", "entry", "appointment", "description", "date", "time"
)

/** Best-effort person-name guess from an email local part, mirroring
 * framework/extraction.py's _local_part_to_name and the iOS port's
 * localPartToName. Ensures a person's email address maps to THEIR
 * placeholder rather than a generic one. */
fun localPartToName(email: String): String? {
    val local = email.substringBefore("@")
    val parts = local.split(Regex("[._-]+"))
        .filter { it.isNotEmpty() && !it.all(Char::isDigit) }
    if (parts.isEmpty()) return null
    return parts.joinToString(" ") { it.replaceFirstChar(Char::uppercase).lowercase()
        .replaceFirstChar(Char::uppercase) }
}

private fun personKey(surface: String): String =
    surface.lowercase().split(Regex("[.\\s_,-]+")).filter { it.isNotEmpty() }.sorted().joinToString(" ")

object EntityExtraction {
    /** Two-or-more consecutive capitalized-word runs, filtered against the
     * stoplist -- a simple deterministic PERSON heuristic. Plus email
     * addresses and the person implied by each. No LLM merge pass in
     * Phase 1 (see file header). */
    fun extract(text: String): List<Entity> {
        val byKey = LinkedHashMap<String, Entity>()

        fun add(rawSurface: String, type: EntityType) {
            val surface = rawSurface.replace(">", " ").replace("|", " ")
                .trim().trim('\'', '"', ' ', '\t', ',', ';', ':')
            if (surface.length < 2) return
            val key = if (type == EntityType.PERSON) personKey(surface) else surface.lowercase()
            byKey.getOrPut(key) { Entity(surface, type) }
        }

        for (match in EMAIL_REGEX.findAll(text)) {
            val email = match.value
            add(email, EntityType.EMAIL)
            localPartToName(email)?.let { add(it, EntityType.PERSON) }
        }

        val capWordRun = Regex("""\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b""")
        for (match in capWordRun.findAll(text)) {
            val candidate = match.groupValues[1]
            val words = candidate.split(" ")
            if (words.any { it.lowercase() in STOPWORDS }) continue
            add(candidate, EntityType.PERSON)
        }

        return byKey.values.toList()
    }
}

object Generalization {
    private const val GENERIC_EMAIL = "a redacted email address"

    /** Assign one placeholder per entity, mirroring build_mapping in
     * generalization.py (Phase 1 scope: PERSON + EMAIL only, matching this
     * port's entity types -- see file header for why ORG/LOCATION aren't
     * detected here). */
    fun buildMapping(entities: List<Entity>): Map<String, String> {
        val mapping = LinkedHashMap<String, String>()
        val personLabelBySurface = HashMap<String, String>()
        val letters = ('A'..'Z').toList()

        val persons = entities.filter { it.type == EntityType.PERSON }
        for ((i, ent) in persons.withIndex()) {
            val label = if (i < letters.size) "Person-${letters[i]}" else "Person-${i + 1}"
            mapping[ent.text] = label
            personLabelBySurface[ent.text.lowercase()] = label
        }

        for (ent in entities) {
            if (ent.type != EntityType.EMAIL) continue
            val owner = localPartToName(ent.text)
            val label = owner?.let { personLabelBySurface[it.lowercase()] }
            mapping[ent.text] = if (label != null) "[$label's address]" else GENERIC_EMAIL
        }

        return mapping
    }

    /** Deterministic substitution: longest entity surface first, case-
     * insensitive, boundary-anchored via lookaround -- identical semantics
     * to the Python and iOS ports (Kotlin/JVM regex supports the same
     * (?<!\w)/(?!\w) lookaround Python's re and NSRegularExpression do). */
    fun applyMapping(text: String, mapping: Map<String, String>): String {
        var result = text
        for (surface in mapping.keys.sortedByDescending { it.length }) {
            val replacement = mapping[surface] ?: continue
            val escaped = Regex.escape(surface)
            val pattern = if (surface.contains("@")) escaped else "(?<!\\w)$escaped(?!\\w)"
            result = Regex(pattern, RegexOption.IGNORE_CASE).replace(result, Regex.escapeReplacement(replacement))
        }
        return result
    }

    data class Result(val generalized: String, val entities: List<Entity>, val mapping: Map<String, String>)

    fun generalize(text: String): Result {
        val entities = EntityExtraction.extract(text)
        val mapping = buildMapping(entities)
        val generalized = applyMapping(text, mapping)
        return Result(generalized, entities, mapping)
    }
}
