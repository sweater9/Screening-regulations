"""Native low-latency client for a LiveTalking server (WebRTC receive, no browser).

Video/audio: aiortc recvonly session via POST /offer (same as LiveTalking's web client).
Speech in: local mic + faster-whisper. Brain: Claude on this Mac (key from ANTHROPIC_API_KEY).
Speech out: each finished sentence is sent to POST /human {type: echo}; the server does TTS + lip-sync.
Barge-in: loud mic input while the avatar is speaking calls POST /interrupt_talk.

Usage: ANTHROPIC_API_KEY=... python avatar_client.py http://VM_IP:8010
"""
import asyncio
import os
import queue
import re
import sys
import threading
import time

import aiohttp
import anthropic
import cv2
import numpy as np
import sounddevice as sd
from aiortc import RTCPeerConnection, RTCSessionDescription
from faster_whisper import WhisperModel

SERVER = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8010"
LLM_MODEL = os.environ.get("AVATAR_LLM_MODEL", "claude-sonnet-5-5")
SYSTEM = "You are a friendly conversational avatar. Reply in 1-3 short spoken sentences."
RATE_IN, BLOCK = 16000, 1600            # 100 ms mic blocks
SPEECH_RMS, BARGE_RMS = 0.015, 0.04     # tune for your mic
END_SILENCE_S = 0.7

frames = queue.Queue(maxsize=2)          # latest video frames -> UI thread
mic_q: "queue.Queue[np.ndarray]" = queue.Queue()
state = {"session": None, "speaking_until": 0.0, "stop": False}


async def play_audio(track):
    stream = None
    while True:
        f = await track.recv()
        pcm = f.to_ndarray()
        if stream is None:
            ch = len(f.layout.channels)
            stream = sd.OutputStream(samplerate=f.sample_rate, channels=ch, dtype="int16")
            stream.start()
        data = pcm.reshape(-1, len(f.layout.channels)) if pcm.ndim == 1 or pcm.shape[0] == 1 else pcm.T
        stream.write(np.ascontiguousarray(data.astype("int16")))
        if np.abs(data).max() > 300:     # crude "avatar is speaking" signal
            state["speaking_until"] = time.time() + 0.4


async def show_video(track):
    while True:
        f = await track.recv()
        img = f.to_ndarray(format="bgr24")
        if frames.full():
            try: frames.get_nowait()
            except queue.Empty: pass
        frames.put(img)


async def connect(http):
    pc = RTCPeerConnection()
    pc.addTransceiver("video", direction="recvonly")
    pc.addTransceiver("audio", direction="recvonly")

    @pc.on("track")
    def on_track(track):
        asyncio.ensure_future(show_video(track) if track.kind == "video" else play_audio(track))

    await pc.setLocalDescription(await pc.createOffer())
    async with http.post(f"{SERVER}/offer", json={"sdp": pc.localDescription.sdp,
                                                  "type": pc.localDescription.type}) as r:
        ans = await r.json()
    state["session"] = ans["sessionid"]
    await pc.setRemoteDescription(RTCSessionDescription(sdp=ans["sdp"], type=ans["type"]))
    return pc


def mic_callback(indata, n, t, s):
    mic_q.put(indata[:, 0].copy())


async def converse(http):
    whisper = WhisperModel("small.en", compute_type="int8")
    claude = anthropic.AsyncAnthropic()  # key from env only
    history, buf, voiced, last_voice = [], [], False, 0.0
    loop = asyncio.get_running_loop()
    while not state["stop"]:
        try:
            blk = await loop.run_in_executor(None, lambda: mic_q.get(timeout=0.2))
        except queue.Empty:
            continue
        rms = float(np.sqrt(np.mean(blk ** 2)))
        now = time.time()
        if rms > BARGE_RMS and now < state["speaking_until"]:
            await http.post(f"{SERVER}/interrupt_talk", json={"sessionid": state["session"]})
            state["speaking_until"] = 0
        if now < state["speaking_until"] and rms <= BARGE_RMS:
            continue                      # ignore speaker bleed while avatar talks
        if rms > SPEECH_RMS:
            voiced, last_voice = True, now
        if voiced:
            buf.append(blk)
        if voiced and now - last_voice > END_SILENCE_S:
            audio, buf, voiced = np.concatenate(buf), [], False
            segs, _ = await loop.run_in_executor(None, lambda: whisper.transcribe(audio, language="en"))
            text = " ".join(s.text for s in segs).strip()
            if len(text) < 2:
                continue
            print(f"you: {text}")
            history.append({"role": "user", "content": text})
            reply, pending = "", ""
            async with claude.messages.stream(model=LLM_MODEL, max_tokens=300, system=SYSTEM,
                                              messages=history) as s:
                async for chunk in s.text_stream:
                    reply += chunk; pending += chunk
                    m = re.search(r"(.+?[.!?])\s", pending)   # speak each sentence as soon as it ends
                    while m:
                        await say(http, m.group(1)); pending = pending[m.end():]
                        m = re.search(r"(.+?[.!?])\s", pending)
            if pending.strip():
                await say(http, pending.strip())
            print(f"avatar: {reply}")
            history.append({"role": "assistant", "content": reply})


async def say(http, text):
    state["speaking_until"] = time.time() + 1.0
    await http.post(f"{SERVER}/human", json={"sessionid": state["session"], "type": "echo", "text": text})


async def main_async():
    async with aiohttp.ClientSession() as http:
        pc = await connect(http)
        try:
            with sd.InputStream(samplerate=RATE_IN, blocksize=BLOCK, channels=1, dtype="float32",
                                callback=mic_callback):
                await converse(http)
        finally:
            await pc.close()


def main():
    t = threading.Thread(target=lambda: asyncio.run(main_async()), daemon=True)
    t.start()
    cv2.namedWindow("avatar", cv2.WINDOW_NORMAL)   # GUI must run on the main thread on macOS
    while t.is_alive():
        try:
            cv2.imshow("avatar", frames.get(timeout=0.05))
        except queue.Empty:
            pass
        if cv2.waitKey(1) & 0xFF in (27, ord("q")):
            state["stop"] = True
            break


if __name__ == "__main__":
    main()
