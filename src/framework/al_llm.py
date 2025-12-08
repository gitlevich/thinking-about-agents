# src/framework/al_llm.py

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, is_dataclass
from textwrap import dedent
from typing import Any, Callable, Dict

from .al import Frame, Choice, Sigil

LlmCall = Callable[[str], str]


@dataclass
class LlmSigil(Sigil):
    """
    LLM-backed sigil: the LLM is the preference field.

    You give it (frame, choice, state), it returns a numeric 'score'.
    """

    system_prompt: str
    call_llm: LlmCall

    def __init__(
            self,
            name: str,
            description: str,
            system_prompt: str,
            call_llm: LlmCall,
            weight: float = 1.0,
    ) -> None:
        super().__init__(name=name, description=description, weight=weight)
        self.system_prompt = system_prompt
        self.call_llm = call_llm

    def _build_prompt(self, frame: Frame, choice: Choice) -> str:
        frame_view: Dict[str, Any] = {c.name: v for c, v in frame.values.items()}

        payload = choice.payload
        if is_dataclass(payload):
            payload_json: Any = asdict(payload)
        elif isinstance(payload, (str, int, float, bool)) or payload is None:
            payload_json = payload
        else:
            # last resort: string form
            payload_json = repr(payload)

        choice_view: Dict[str, Any] = {
            "label": choice.label,
            "payload": payload_json,
        }

        user = {
            "sigil_name": self.name,
            "sigil_description": self.description,
            "state": self.state,
            "frame": frame_view,
            "choice": choice_view,
            "instruction": (
                "Return JSON with a single numeric field 'score' between -10 and 10. "
                "No extra text."
            ),
        }

        return dedent(
            f"""
            SYSTEM:
            {self.system_prompt}

            USER:
            {json.dumps(user, ensure_ascii=False, indent=2)}
            """
        ).strip()

    def score(self, frame: Frame, choice: Choice) -> float:
        prompt = self._build_prompt(frame, choice)
        raw = self.call_llm(prompt)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return 0.0

        val = data.get("score", 0.0)
        try:
            return float(val) * self.weight
        except (TypeError, ValueError):
            return 0.0
