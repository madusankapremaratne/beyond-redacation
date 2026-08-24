// EdgeRuntimeBenchmarkApp.swift
//
// Minimal app -- not a real UI, just enough to launch, run the benchmark once,
// and display a status string confirming completion + the output path (for
// screenshot-based confirmation if needed). Results are written to
// Documents/results.json and retrieved via `xcrun devicectl device copy from`,
// not read off the screen.

import SwiftUI

@main
struct EdgeRuntimeBenchmarkApp: App {
    var body: some Scene {
        WindowGroup {
            BenchmarkView()
        }
    }
}

struct BenchmarkView: View {
    @State private var status = "Running benchmark..."

    var body: some View {
        VStack(spacing: 16) {
            Text("Beyond Redaction — Edge Runtime Benchmark")
                .font(.headline)
            Text(status)
                .font(.system(.body, design: .monospaced))
                .multilineTextAlignment(.center)
                .padding()
        }
        .padding()
        .task {
            let outURL = BenchmarkRunner.runAndSave()
            status = "Done.\nWrote: \(outURL.lastPathComponent)\nPull via devicectl."
        }
    }
}
