import http.client
import json
import os
from typing import Callable

LlmCall = Callable[[str], str]


def make_openai_call(model: str = "gpt-4.1-mini") -> LlmCall:
    """
    Returns a function prompt -> raw JSON string from the model.

    Uses /v1/responses with JSON mode, no extra dependencies.
    """

    def call_llm(prompt: str) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        body = json.dumps(
            {
                "model": model,
                "input": prompt,
                # force JSON output from the model itself
                "text": {"format": {"type": "json_object"}},
                "max_output_tokens": 64,
            }
        )

        conn = http.client.HTTPSConnection("api.openai.com")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        project = os.environ.get("OPENAI_PROJECT")
        if project:
            headers["OpenAI-Project"] = project

        conn.request("POST", "/v1/responses", body, headers)
        res = conn.getresponse()
        raw = res.read().decode("utf-8")
        conn.close()

        if res.status != 200:
            raise RuntimeError(f"OpenAI API error {res.status}: {raw}")

        # Extract the assistant text from the Responses object.
        # Shape: {"output": [{"type": "message", "content":[{"type":"output_text","text": "..."}]}], ...}
        data = json.loads(raw)
        pieces = []
        for item in data.get("output", []):
            if item.get("type") == "message":
                for c in item.get("content", []):
                    if c.get("type") == "output_text":
                        pieces.append(c.get("text", ""))

        text = "".join(pieces).strip()
        # Our LlmSigil expects *JSON* as a string (e.g. {"score": 3.2})
        # If we somehow failed to extract it, fall back to the raw assistant text.
        return text or raw

    return call_llm
