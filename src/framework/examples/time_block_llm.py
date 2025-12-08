# in examples/time_block_llm.py or similar

from framework.al_llm import LlmSigil
from framework.openai_client import make_openai_call
from framework.al import Contrast, Resolution, Frame, Choice, Agent

EXEC_SYSTEM = """
You are the user's internal executive assistant.

You receive:
- the current block frame (energy, minutes, context),
- one candidate task,
- the current internal state of this sigil.

Return ONLY a JSON object like:
{"score": 7.5}

where score is between -10 and 10.
"""


def make_exec_agent() -> Agent:
    sigil = LlmSigil(
        name="exec",
        description="use this hour well",
        system_prompt=EXEC_SYSTEM.strip(),
        call_llm=make_openai_call("gpt-4.1-mini"),
        weight=1.0,
    )
    return Agent("me_exec").with_sigils(sigil)
