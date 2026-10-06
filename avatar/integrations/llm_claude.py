"""Claude LLM adapter for LiveTalking's chat hook. Key comes from the environment only."""
import os
import anthropic

MODEL = os.environ.get("AVATAR_LLM_MODEL", "claude-sonnet-5-5")
SYSTEM = "You are a friendly conversational avatar. Reply in 1-3 short spoken sentences."


def stream_reply(history):
    """Yield text chunks for TTS. history: list of {"role","content"} dicts."""
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY; never log it
    with client.messages.stream(model=MODEL, max_tokens=300, system=SYSTEM, messages=history) as s:
        yield from s.text_stream
