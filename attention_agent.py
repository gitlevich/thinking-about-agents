"""
Why Your Agent Gets Captured

An agent that can observe, generate, get captured, detect capture, and recover.
Demonstrates: observer/agent modes, bandwidth as resource, capture detection, regulator.

Author: Vladimir Gitlevich
Developed in conversation with Claude.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum, auto
from typing import Optional, Generator
import random


class Mode(Enum):
    """Two modes appear when I pay attention."""
    OBSERVER = auto()  # Present to frame, high bandwidth, low cost
    AGENT = auto()      # Captured by narrative, generating, consuming bandwidth


@dataclass(frozen=True)
class Bandwidth:
    """
    A single abstract resource standing in for attention, energy, and compute.

    Generation competes with everything else for this resource,
    including the meta-cognitive process that could interrupt generation.
    """
    current: float
    maximum: float

    @property
    def ratio(self) -> float:
        return self.current / self.maximum

    @property
    def exhausted(self) -> bool:
        return self.current <= 0

    def can_afford(self, cost: float) -> bool:
        return self.current >= cost

    def above_threshold(self, threshold: float) -> bool:
        return self.ratio > threshold

    def deplete(self, amount: float) -> Bandwidth:
        return replace(self, current=self.current - amount)

    def recover(self, rate: float) -> Bandwidth:
        return replace(self, current=min(self.maximum, self.current + rate))


@dataclass(frozen=True)
class CaptureSignal:
    """A sign that attention may be captured."""
    name: str


@dataclass(frozen=True)
class CaptureAssessment:
    """
    Capture detection monitors for circular reasoning and goalless drift.

    In code, I approximate these with cycles in the path,
    long goalless trajectories, and high-gravity terminal nodes.
    """
    signals: tuple[CaptureSignal, ...]

    @property
    def detected(self) -> bool:
        return len(self.signals) > 0

    @property
    def severity(self) -> int:
        return len(self.signals)

    @property
    def signal_names(self) -> list[str]:
        return [s.name for s in self.signals]

    def warrants_interruption(self, threshold: int = 2) -> bool:
        return self.severity >= threshold


@dataclass
class Trajectory:
    """
    Path through topology.

    Each token conditions the next until the chain hits a terminus
    too heavy to traverse past without deliberate effort.
    """
    path: list[str] = field(default_factory=list)
    momentum: float = 0.0
    goal: Optional[str] = None
    cycles_detected: int = 0

    @property
    def current(self) -> Optional[str]:
        return self.path[-1] if self.path else None

    @property
    def has_cycle(self) -> bool:
        """Circular reasoning."""
        return len(self.path) != len(set(self.path))

    @property
    def is_drifting(self) -> bool:
        """Long goalless trajectory."""
        return len(self.path) > 5 and self.goal is None

    @property
    def high_momentum_without_goal(self) -> bool:
        return self.momentum > 0.7 and self.goal is None

    def step(self, sigil: str) -> None:
        self.path.append(sigil)

    def accelerate(self, amount: float = 0.2) -> None:
        """Momentum builds when falling."""
        self.momentum += amount

    def decelerate(self, factor: float = 0.8) -> None:
        """Momentum decreases when climbing toward goal."""
        self.momentum *= factor

    def reached_goal(self) -> bool:
        return self.goal is not None and self.current == self.goal

    def note_cycle(self) -> None:
        self.cycles_detected += 1


@dataclass(frozen=True)
class Metrics:
    """Observable outcomes."""
    captures_detected: int = 0
    forced_returns: int = 0
    completions: int = 0

    def detected_capture(self) -> Metrics:
        return replace(self, captures_detected=self.captures_detected + 1)

    def forced_return(self) -> Metrics:
        return replace(self, forced_returns=self.forced_returns + 1)

    def completed(self) -> Metrics:
        return replace(self, completions=self.completions + 1)


@dataclass
class Sigil:
    """
    A node in the associative topology.

    Gravity determines how strongly this region pulls attention.
    High-gravity nodes are where trajectories tend to bottom out.
    """
    label: str
    gravity: float
    edges: list[str] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.label)

    @property
    def is_terminal(self) -> bool:
        """No edges means the chain ends here."""
        return not self.edges

    @property
    def is_gravity_well(self) -> bool:
        """High-mass region where attention falls without effort."""
        return self.gravity > 0.8


@dataclass
class Topology:
    """
    The shape of how concepts connect.

    Some regions are densely connected, high-mass—
    attention falls toward them without effort.
    """
    sigils: dict[str, Sigil] = field(default_factory=dict)

    @classmethod
    def from_list(cls, sigils: list[Sigil]) -> Topology:
        return cls({s.label: s for s in sigils})

    def __contains__(self, label: str) -> bool:
        return label in self.sigils

    def __getitem__(self, label: str) -> Sigil:
        return self.sigils[label]

    def get(self, label: str) -> Optional[Sigil]:
        return self.sigils.get(label)

    def traversable_edges(self, sigil: Sigil) -> list[str]:
        return [e for e in sigil.edges if e in self.sigils]

    def choose_by_gravity(self, candidates: list[str]) -> str:
        """Without a goal, you roll downhill toward whatever basin is nearby."""
        weights = [self.sigils[c].gravity for c in candidates]
        total = sum(weights) or 1.0
        normalized = [w / total for w in weights]
        return random.choices(candidates, weights=normalized)[0]


class CaptureDetector:
    """
    Detects signs of capture.

    Capture = generation following local gradients
    until it bottoms out in a gravity well.
    """

    def assess(self, trajectory: Trajectory, current_sigil: Optional[Sigil]) -> CaptureAssessment:
        signals: list[CaptureSignal] = []

        if trajectory.has_cycle:
            signals.append(CaptureSignal("circular_traversal"))
            trajectory.note_cycle()

        if trajectory.is_drifting:
            signals.append(CaptureSignal("goalless_drift"))

        if trajectory.high_momentum_without_goal:
            signals.append(CaptureSignal("high_momentum_no_goal"))

        if current_sigil and current_sigil.is_gravity_well:
            signals.append(CaptureSignal("gravity_well"))

        return CaptureAssessment(tuple(signals))


class Regulator:
    """
    The meta-cognitive process that can interrupt generation.

    The regulator monitors whether the current trajectory is productive
    and can cut the narrative to return to observer.

    But the regulator needs bandwidth to run.
    Heavy narrative starves it.
    """

    def __init__(self, bandwidth_threshold: float, metacognition_cost: float):
        self.bandwidth_threshold = bandwidth_threshold
        self.metacognition_cost = metacognition_cost

    def can_act(self, bandwidth: Bandwidth) -> bool:
        """The regulator needs bandwidth to run."""
        return bandwidth.above_threshold(self.bandwidth_threshold)

    def should_interrupt(
            self,
            bandwidth: Bandwidth,
            assessment: CaptureAssessment,
            cycles: int,
    ) -> bool:
        """
        Decide whether to hard-interrupt.

        Not another voice in the generation,
        but a hard cut that clears context and forces return to observer.
        """
        if not self.can_act(bandwidth):
            return False

        severity = assessment.severity
        if cycles > 1:
            severity += 2

        return severity >= 2


@dataclass
class AgentConfig:
    """Configuration for agent behavior."""
    max_bandwidth: float = 100.0
    generation_cost: float = 5.0
    metacognition_cost: float = 10.0
    recovery_rate: float = 20.0
    capture_threshold: float = 0.3


class Agent:
    """
    An agent with explicit modes and bandwidth.

    Observer is default. Agent mode is entered deliberately
    and exited on trajectory completion or capture detection.
    """

    def __init__(self, config: AgentConfig = AgentConfig()):
        self.config = config
        self.bandwidth = Bandwidth(config.max_bandwidth, config.max_bandwidth)
        self.mode = Mode.OBSERVER
        self.topology = Topology()
        self.trajectory = Trajectory()
        self.metrics = Metrics()

        self.capture_detector = CaptureDetector()
        self.regulator = Regulator(config.capture_threshold, config.metacognition_cost)

    # ── Setup ────────────────────────────────────────────────────────────────

    def load_topology(self, sigils: list[Sigil]) -> None:
        self.topology = Topology.from_list(sigils)

    # ── Observer Mode ────────────────────────────────────────────────────────

    def observe(self) -> Generator[str, None, None]:
        """
        Observer mode: present to frame, not narrating.
        High bandwidth, low energy cost.
        """
        self.mode = Mode.OBSERVER
        self.trajectory = Trajectory()
        self.bandwidth = self.bandwidth.recover(self.config.recovery_rate)

        yield f"[OBSERVER] Bandwidth: {self.bandwidth.current:.1f}/{self.bandwidth.maximum} | Present to frame"

    # ── Generation ───────────────────────────────────────────────────────────

    def generate(
            self,
            start: str,
            goal: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """
        Enter agent mode. Traverse topology from start.

        Goal-directed generation differs because the goal creates
        a gradient you're climbing. Without a goal, you roll downhill.
        """
        if start not in self.topology:
            yield f"[ERROR] Unknown sigil: {start}"
            return

        self.mode = Mode.AGENT
        self.trajectory = Trajectory(goal=goal)

        current = start
        while True:
            outcome = yield from self._generation_step(current)
            if outcome.done:
                return
            current = outcome.next_position

    @dataclass
    class StepOutcome:
        done: bool
        next_position: str = ""

    def _generation_step(self, current: str) -> Generator[str, None, StepOutcome]:
        sigil = self.topology[current]

        yield from self._emit_step(current, sigil)

        if (yield from self._check_capture_and_regulate(sigil)):
            return self.StepOutcome(done=True)

        if sigil.is_terminal:
            yield f"[CONVERGED] Terminal sigil reached: {current}"
            self.metrics = self.metrics.completed()
            yield from self.observe()
            return self.StepOutcome(done=True)

        if self.trajectory.reached_goal():
            yield f"[GOAL] Reached target: {current}"
            self.metrics = self.metrics.completed()
            yield from self.observe()
            return self.StepOutcome(done=True)

        next_pos = self._choose_next(sigil)
        if next_pos is None:
            yield "[DEAD END] No traversable edges"
            yield from self.observe()
            return self.StepOutcome(done=True)

        if self.bandwidth.exhausted:
            yield from self._handle_exhaustion()
            return self.StepOutcome(done=True)

        return self.StepOutcome(done=False, next_position=next_pos)

    def _emit_step(self, position: str, sigil: Sigil) -> Generator[str, None, None]:
        """Pay generation cost, record step."""
        self.bandwidth = self.bandwidth.deplete(self.config.generation_cost)
        self.trajectory.step(position)

        yield f"[AGENT] -> {position} (gravity: {sigil.gravity:.2f}) | Bandwidth: {self.bandwidth.current:.1f}"

    def _check_capture_and_regulate(self, sigil: Sigil) -> Generator[str, None, bool]:
        """
        Check for capture signals. If detected, try to regulate.

        Full capture means the regulator has nothing to execute with.
        You ride until convergence.
        """
        assessment = self.capture_detector.assess(self.trajectory, sigil)

        if not assessment.detected:
            return False

        yield f"[META] Capture signals: {assessment.signal_names}"

        self.bandwidth = self.bandwidth.deplete(self.config.metacognition_cost)

        if self.regulator.should_interrupt(
                self.bandwidth,
                assessment,
                self.trajectory.cycles_detected,
        ):
            self.metrics = self.metrics.detected_capture()
            self.metrics = self.metrics.forced_return()
            yield "[REGULATOR] Hard interrupt. Returning to observer."
            yield from self.observe()
            return True

        if not self.regulator.can_act(self.bandwidth):
            yield "[CAPTURED] Bandwidth exhausted. Riding trajectory to convergence."

        return False

    def _choose_next(self, sigil: Sigil) -> Optional[str]:
        """
        Choose next position.

        Goal-directed: climb toward target.
        Goalless: follow gravity, roll downhill.
        """
        candidates = self.topology.traversable_edges(sigil)
        if not candidates:
            return None

        goal = self.trajectory.goal

        if goal and goal in candidates:
            self.trajectory.decelerate()
            return goal

        self.trajectory.accelerate()
        return self.topology.choose_by_gravity(candidates)

    def _handle_exhaustion(self) -> Generator[str, None, None]:
        """Bandwidth depleted. Forced return."""
        yield "[EXHAUSTED] Bandwidth depleted. Forced return."
        self.metrics = self.metrics.forced_return()
        self.bandwidth = Bandwidth(self.config.recovery_rate, self.bandwidth.maximum)
        yield from self.observe()

    # ── Reporting ────────────────────────────────────────────────────────────

    def stats(self) -> str:
        m = self.metrics
        return (
            f"Captures detected: {m.captures_detected} | "
            f"Forced returns: {m.forced_returns} | "
            f"Completions: {m.completions}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Demo: The Bookcase Topology
# ─────────────────────────────────────────────────────────────────────────────

def build_bookcase_topology() -> list[Sigil]:
    """
    The topology from the essay.

    bookcase → new_york_2008 → storage_san_bruno →
    9_lafayette → 1550_mission → fathers_death

    With branches and gravity wells.
    """
    return [
        Sigil("room", gravity=0.1, edges=["bookcase", "window", "chair"]),
        Sigil("bookcase", gravity=0.3, edges=["new_york_2008", "books", "wood"]),
        Sigil("books", gravity=0.2, edges=["reading", "shelf"]),
        Sigil("reading", gravity=0.2),
        Sigil("wood", gravity=0.1),
        Sigil("shelf", gravity=0.1),
        Sigil("window", gravity=0.2, edges=["light", "view"]),
        Sigil("light", gravity=0.3, edges=["morning", "photography"]),
        Sigil("photography", gravity=0.5, edges=["observer_mode"]),
        Sigil("observer_mode", gravity=0.1),
        Sigil("view", gravity=0.2, edges=["city_hall", "cathedral"]),
        Sigil("city_hall", gravity=0.3),
        Sigil("cathedral", gravity=0.2),
        Sigil("chair", gravity=0.1),
        Sigil("morning", gravity=0.2),
        # The gravity well chain
        Sigil("new_york_2008", gravity=0.4, edges=["storage_san_bruno", "apartment_hunting"]),
        Sigil("apartment_hunting", gravity=0.3),
        Sigil("storage_san_bruno", gravity=0.5, edges=["9_lafayette"]),
        Sigil("9_lafayette", gravity=0.6, edges=["1550_mission", "thirteen_years"]),
        Sigil("thirteen_years", gravity=0.3),
        Sigil("1550_mission", gravity=0.8, edges=["fathers_death"]),
        Sigil("fathers_death", gravity=0.95),  # Terminal, maximum gravity
    ]


def demo() -> None:
    random.seed(42)

    print("=" * 60)
    print("WHY YOUR AGENT GETS CAPTURED")
    print("=" * 60)
    print()

    # Scenario 1: Healthy bandwidth, entering gravity well
    print("SCENARIO 1: Healthy bandwidth, entering gravity well")
    print("-" * 60)

    agent = Agent(AgentConfig(
        max_bandwidth=100.0,
        generation_cost=10.0,
        metacognition_cost=12.0,
        capture_threshold=0.25,
    ))
    agent.load_topology(build_bookcase_topology())

    for msg in agent.observe():
        print(msg)
    for msg in agent.generate("bookcase"):
        print(msg)

    print()
    print(f"Result: {agent.stats()}")
    print()

    # Scenario 2: Depleted bandwidth, gets captured
    print("SCENARIO 2: Depleted bandwidth, entering gravity well")
    print("-" * 60)

    agent2 = Agent(AgentConfig(
        max_bandwidth=100.0,
        generation_cost=15.0,
        metacognition_cost=20.0,
        capture_threshold=0.30,
    ))
    agent2.load_topology(build_bookcase_topology())
    agent2.bandwidth = Bandwidth(50.0, 100.0)

    print(f"[SETUP] Starting with depleted bandwidth: {agent2.bandwidth.current}")

    for msg in agent2.generate("new_york_2008"):
        print(msg)

    print()
    print(f"Result: {agent2.stats()}")
    print()

    # Scenario 3: Goal-directed traversal resists gravity
    print("SCENARIO 3: Goal-directed traversal")
    print("-" * 60)

    agent3 = Agent(AgentConfig(
        max_bandwidth=100.0,
        generation_cost=10.0,
        metacognition_cost=12.0,
        capture_threshold=0.25,
    ))
    agent3.load_topology(build_bookcase_topology())

    for msg in agent3.observe():
        print(msg)
    for msg in agent3.generate("window", goal="photography"):
        print(msg)

    print()
    print(f"Result: {agent3.stats()}")
    print()

    # Scenario 4: Successful regulation
    print("SCENARIO 4: Successful regulation (catches itself)")
    print("-" * 60)

    agent4 = Agent(AgentConfig(
        max_bandwidth=150.0,
        generation_cost=8.0,
        metacognition_cost=10.0,
        capture_threshold=0.20,
    ))
    agent4.load_topology(build_bookcase_topology())

    # Add cycle to trigger detection
    agent4.topology.sigils["9_lafayette"].edges.append("storage_san_bruno")

    for msg in agent4.observe():
        print(msg)
    for msg in agent4.generate("new_york_2008"):
        print(msg)

    print()
    print(f"Result: {agent4.stats()}")


if __name__ == "__main__":
    demo()
