// BenchmarkRunner.swift
//
// Loads the shared N=20 sample corpus (edge-runtime/shared/benchmark_samples.json,
// bundled as a resource -- identical input to the Android port and traceable back
// to the same seeded draw used in evaluation notebooks 07/08), runs entity
// detection + mapping + substitution per sample, times each one, and writes a
// results JSON to the app's Documents directory for retrieval via `devicectl`.
//
// Cold-start and steady-state latency are reported separately (see the edge-
// runtime benchmark plan's Verification section): sample 0's timing includes
// NLTagger's one-time model load, which would misrepresent steady-state
// per-document cost if averaged in with the rest.

import Foundation

struct BenchmarkSample: Codable {
    let sampleId: Int
    let text: String

    enum CodingKeys: String, CodingKey {
        case sampleId = "sample_id"
        case text
    }
}

struct SampleResult: Codable {
    let sampleId: Int
    let entityCount: Int
    let latencyMs: Double
    let peakMemoryMb: Double
    let mapping: [String: String]

    enum CodingKeys: String, CodingKey {
        case sampleId = "sample_id"
        case entityCount = "entity_count"
        case latencyMs = "latency_ms"
        case peakMemoryMb = "peak_memory_mb"
        case mapping
    }
}

struct BenchmarkReport: Codable {
    let platform = "iOS"
    let osVersion: String
    let deviceModel: String
    let coldStartLatencyMs: Double
    let steadyStateLatencyMsMean: Double
    let steadyStateLatencyMsMedian: Double
    let results: [SampleResult]

    enum CodingKeys: String, CodingKey {
        case platform, results
        case osVersion = "os_version"
        case deviceModel = "device_model"
        case coldStartLatencyMs = "cold_start_latency_ms"
        case steadyStateLatencyMsMean = "steady_state_latency_ms_mean"
        case steadyStateLatencyMsMedian = "steady_state_latency_ms_median"
    }
}

/// Resident memory via mach_task_basic_info -- the standard way to sample a
/// process's own memory footprint on Apple platforms without Instruments.
private func currentMemoryMb() -> Double {
    var info = mach_task_basic_info()
    var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size) / 4
    let result: kern_return_t = withUnsafeMutablePointer(to: &info) {
        $0.withMemoryRebound(to: integer_t.self, capacity: Int(count)) {
            task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
        }
    }
    guard result == KERN_SUCCESS else { return 0 }
    return Double(info.resident_size) / 1_048_576.0
}

enum BenchmarkRunner {
    static func run() -> BenchmarkReport {
        guard let url = Bundle.main.url(forResource: "benchmark_samples", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let samples = try? JSONDecoder().decode([BenchmarkSample].self, from: data) else {
            fatalError("benchmark_samples.json missing or malformed in app bundle")
        }

        var results: [SampleResult] = []
        var coldStart: Double = 0

        for (i, sample) in samples.enumerated() {
            let start = DispatchTime.now()
            let (_, entities, mapping) = Generalization.generalize(sample.text)
            let elapsedMs = Double(DispatchTime.now().uptimeNanoseconds - start.uptimeNanoseconds) / 1_000_000.0

            if i == 0 {
                coldStart = elapsedMs
            }
            results.append(SampleResult(
                sampleId: sample.sampleId,
                entityCount: entities.count,
                latencyMs: elapsedMs,
                peakMemoryMb: currentMemoryMb(),
                mapping: mapping
            ))
        }

        let steadyState = results.dropFirst().map(\.latencyMs).sorted()
        let mean = steadyState.isEmpty ? 0 : steadyState.reduce(0, +) / Double(steadyState.count)
        let median = steadyState.isEmpty ? 0 : steadyState[steadyState.count / 2]

        let device = UIDeviceInfo.current()
        return BenchmarkReport(
            osVersion: device.osVersion,
            deviceModel: device.model,
            coldStartLatencyMs: coldStart,
            steadyStateLatencyMsMean: mean,
            steadyStateLatencyMsMedian: median,
            results: results
        )
    }

    static func runAndSave() -> URL {
        let report = run()
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        let data = try! encoder.encode(report)

        let docs = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let outURL = docs.appendingPathComponent("results.json")
        try! data.write(to: outURL)
        return outURL
    }
}
