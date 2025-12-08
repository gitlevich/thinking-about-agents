from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Sequence, Tuple


class Resolution(Enum):
    COARSE = auto()
    MEDIUM = auto()
    FINE = auto()


@dataclass(frozen=True)
class Contrast:
    """
    A dimension along which things can differ for this agent.
    is_self=True means proprioception / I-side telemetry.
    """
    name: str
    description: str = ""
    resolution: Resolution = Resolution.MEDIUM
    is_self: bool = False

    def __repr__(self) -> str:
        return f"Contrast({self.name})"


@dataclass
class Frame:
    """
    Packet of relevant observations along contrasts at this step.
    Already past I/not-I + relevance filtering conceptually.
    """
    values: Dict[Contrast, Any] = field(default_factory=dict)

    def see(self, contrast: Contrast, value: Any) -> Frame:
        self.values[contrast] = value
        return self

    def view(self, contrast: Contrast, default: Any = None) -> Any:
        return self.values.get(contrast, default)

    def __repr__(self) -> str:
        inner = ", ".join(f"{c.name}={v!r}" for c, v in self.values.items())
        return f"Frame({inner})"


@dataclass(frozen=True)
class Choice:
    """
    Candidate next event at this scale.
    """
    label: str
    payload: Any = None

    def __repr__(self) -> str:
        return f"Choice({self.label})"


class Sigil:
    """
    Named, stateful preference field over (frame, choice).

    - attend(frame): see what's present (attention hook)
    - score(frame, choice): how much this sigil wants that choice now
    - learn(frame, choice): update its internal state after collapse
    """

    def __init__(self, name: str, description: str, weight: float = 1.0) -> None:
        self.name = name
        self.description = description
        self.weight = weight
        self.state: Dict[str, Any] = {}

    def attend(self, frame: Frame) -> None:
        pass

    def score(self, frame: Frame, choice: Choice) -> float:
        return 0.0

    def learn(self, frame: Frame, choice: Choice) -> None:
        pass

    def __repr__(self) -> str:
        return f"Sigil({self.name})"


@dataclass
class Agent:
    """
    Observer with a bundle of sigils.
    Goal is not a field; it precipitates from the active sigils.
    """
    name: str
    sigils: List[Sigil] = field(default_factory=list)

    def with_sigils(self, *sigils: Sigil) -> Agent:
        self.sigils.extend(sigils)
        return self

    def attach(self, sigil: Sigil) -> None:
        self.sigils.append(sigil)

    def detach(self, sigil: Sigil) -> None:
        self.sigils = [s for s in self.sigils if s is not sigil]

    def _total_score(self, frame: Frame, choice: Choice) -> float:
        if not self.sigils:
            return 0.0
        return sum(s.weight * s.score(frame, choice) for s in self.sigils)

    def choose(self, frame: Frame, options: Sequence[Choice]) -> Tuple[Choice, float]:
        """
        Collapse: argmax over choices under current sigils.
        """
        for s in self.sigils:
            s.attend(frame)

        scored = [(self._total_score(frame, c), c) for c in options]
        scored.sort(key=lambda t: t[0], reverse=True)
        best_score, best_choice = scored[0]

        for s in self.sigils:
            s.learn(frame, best_choice)

        return best_choice, best_score

    @property
    def goal_hint(self) -> str:
        if not self.sigils:
            return ""
        return " & ".join(s.description for s in self.sigils)


# Observation stream = strip of frames (pre-collapse)


@dataclass
class Observation:
    frame: Frame


@dataclass
class ObservationStream:
    observations: List[Observation] = field(default_factory=list)

    def append(self, frame: Frame) -> None:
        self.observations.append(Observation(frame))

    def __iter__(self):
        return iter(self.observations)


# Collapse history = frames + choices + scores; narrative = choices only.


@dataclass
class Collapse:
    frame: Frame
    choice: Choice
    score: float


@dataclass
class History:
    agent: Agent
    collapses: List[Collapse] = field(default_factory=list)

    def record(self, frame: Frame, choice: Choice, score: float) -> None:
        self.collapses.append(Collapse(frame=frame, choice=choice, score=score))

    @property
    def narrative(self) -> List[Choice]:
        return [c.choice for c in self.collapses]

    def last_choice(self) -> Optional[Choice]:
        return self.collapses[-1].choice if self.collapses else None

    def __iter__(self):
        return iter(self.collapses)


# Regulator stub: higher-scale agent acting on telemetry (proprioception).


class Intervention(Enum):
    CONTINUE = auto()
    PAUSE = auto()
    SHRINK_FRAME = auto()
    RESET_SIGILS = auto()
    ASK_HUMAN = auto()


@dataclass
class Regulator:
    """
    Higher-scale agent that reads proprioceptive contrasts (telemetry)
    and decides interventions on the lower-scale agent.
    """

    name: str

    def decide(self, telemetry: Frame) -> Intervention:
        """
        Placeholder heuristic. You'd replace this with real logic or sigils.
        """
        # Very simple example using an 'overload' self-contrast if present.
        overload_level = 0.0
        for c, v in telemetry.values.items():
            if c.is_self and c.name.lower() in ("overload", "confusion"):
                try:
                    overload_level = float(v)
                except (TypeError, ValueError):
                    overload_level = 0.0

        if overload_level > 0.8:
            return Intervention.ASK_HUMAN
        if overload_level > 0.6:
            return Intervention.PAUSE
        return Intervention.CONTINUE
