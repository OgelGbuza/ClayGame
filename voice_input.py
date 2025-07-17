"""Voice command utilities using Whisper API (optional)."""

import os

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None


def transcribe(path: str) -> str:
    """Transcribe an audio file using OpenAI Whisper if available."""
    if openai is None:
        raise RuntimeError("openai package not installed")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    with open(path, "rb") as f:
        audio = f.read()
    resp = openai.Audio.transcribe("whisper-1", audio)
    return resp["text"]
