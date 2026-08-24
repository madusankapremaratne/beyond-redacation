package com.beyondredaction.edgeruntimebenchmark

// BenchmarkRunner.kt
//
// Loads the shared N=20 sample corpus (edge-runtime/shared/benchmark_samples.json,
// bundled as an asset -- identical input to the iOS port and traceable back to
// the same seeded draw used in evaluation notebooks 07/08), runs entity
// detection + mapping + substitution per sample, times each one, and writes a
// results JSON to app-internal storage for retrieval via `adb pull`.
//
// Cold-start and steady-state latency are reported separately, same rationale
// as the iOS port: sample 0's timing includes JIT/class-load warm-up, which
// would misrepresent steady-state per-document cost if averaged in.

import android.app.Activity
import android.os.Build
import android.os.Debug
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.io.File

@Serializable
data class BenchmarkSample(@SerialName("sample_id") val sampleId: Int, val text: String)

@Serializable
data class SampleResult(
    @SerialName("sample_id") val sampleId: Int,
    @SerialName("entity_count") val entityCount: Int,
    @SerialName("latency_ms") val latencyMs: Double,
    @SerialName("peak_memory_mb") val peakMemoryMb: Double,
    val mapping: Map<String, String>
)

@Serializable
data class BenchmarkReport(
    val platform: String = "Android",
    @SerialName("os_version") val osVersion: String,
    @SerialName("device_model") val deviceModel: String,
    @SerialName("cold_start_latency_ms") val coldStartLatencyMs: Double,
    @SerialName("steady_state_latency_ms_mean") val steadyStateLatencyMsMean: Double,
    @SerialName("steady_state_latency_ms_median") val steadyStateLatencyMsMedian: Double,
    val results: List<SampleResult>
)

private fun currentMemoryMb(): Double {
    val info = Debug.MemoryInfo()
    Debug.getMemoryInfo(info)
    return info.totalPss / 1024.0 // totalPss is in KB
}

object BenchmarkRunner {
    private val json = Json { prettyPrint = true }

    fun run(activity: Activity): BenchmarkReport {
        val samplesText = activity.assets.open("benchmark_samples.json").bufferedReader().use { it.readText() }
        val samples = json.decodeFromString<List<BenchmarkSample>>(samplesText)

        val results = mutableListOf<SampleResult>()
        var coldStart = 0.0

        for ((i, sample) in samples.withIndex()) {
            val start = System.nanoTime()
            val out = Generalization.generalize(sample.text)
            val elapsedMs = (System.nanoTime() - start) / 1_000_000.0

            if (i == 0) coldStart = elapsedMs
            results.add(
                SampleResult(
                    sampleId = sample.sampleId,
                    entityCount = out.entities.size,
                    latencyMs = elapsedMs,
                    peakMemoryMb = currentMemoryMb(),
                    mapping = out.mapping
                )
            )
        }

        val steadyState = results.drop(1).map { it.latencyMs }.sorted()
        val mean = if (steadyState.isEmpty()) 0.0 else steadyState.sum() / steadyState.size
        val median = if (steadyState.isEmpty()) 0.0 else steadyState[steadyState.size / 2]

        return BenchmarkReport(
            osVersion = Build.VERSION.RELEASE,
            deviceModel = Build.MODEL,
            coldStartLatencyMs = coldStart,
            steadyStateLatencyMsMean = mean,
            steadyStateLatencyMsMedian = median,
            results = results
        )
    }

    fun runAndSave(activity: Activity): File {
        val report = run(activity)
        val outFile = File(activity.filesDir, "results.json")
        outFile.writeText(json.encodeToString(BenchmarkReport.serializer(), report))
        return outFile
    }
}
