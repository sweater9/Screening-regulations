"""Measures LLM time-to-first-token and time-to-first-sentence. STT/TTS timings: wire in your engines."""
import time
from llm_claude import stream_reply

t0 = time.perf_counter(); first = None; text = ""
for chunk in stream_reply([{"role": "user", "content": "Tell me a fun fact."}]):
    if first is None:
        first = time.perf_counter() - t0
    text += chunk
print(f"LLM first token: {first*1000:.0f} ms, total: {(time.perf_counter()-t0)*1000:.0f} ms")
# TODO: add STT (audio->text) and TTS (first audio chunk) timers using the chosen providers.
