package com.beyondredaction.edgeruntimebenchmark

// MainActivity.kt -- minimal, not a real UI, just enough to launch, run the
// benchmark once, and show a status string. Results are written to
// app-internal files/results.json and retrieved via `adb pull` (using `run-as`
// since app-internal storage isn't world-readable), not read off the screen.

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val textView = TextView(this).apply {
            text = "Running benchmark..."
            textSize = 16f
            setPadding(48, 96, 48, 48)
        }
        setContentView(textView)

        thread {
            val outFile = BenchmarkRunner.runAndSave(this)
            runOnUiThread {
                textView.text = "Done.\nWrote: ${outFile.absolutePath}\nPull via adb (run-as)."
            }
        }
    }
}
