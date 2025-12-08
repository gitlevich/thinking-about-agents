"""
Attention-Based Agent Architecture

Author: Claude Opus 4.5 on behalf of Vladimir Gitlevich
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field, replace
from enum import Enum, auto
from typing import Optional, Generator

class Mode(Enum):
    OBSERVER = auto()
    AGENT = auto()


@dataclass(frozen=True)
class Bandwidth:
    """Attention as finite resource."""
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

    def reset_to(self, value: float) -> Bandwidth:
        return replace(self, current=value)


@dataclass(frozen=True)
class CaptureSignal:
    """A sign that attention may be captured."""
    name: str
    severity: int = 1


@dataclass(frozen=True)
class CaptureAssessment:
    """Result of checking for capture."""
    signals: tuple[CaptureSignal, ...]

    @property
    def detected(self) -> bool:
        return len(self.signals) > 0

    @property
    def severity(self) -> int:
        return sum(s.severity for s in self.signals)

    @property
    def signal_names(self) -> list[str]:
        return [s.name for s in self.signals]

    def warrants_regulation(self, threshold: int = 2) -> bool:
        return self.severity >= threshold


@dataclass(frozen=True)
class Metrics:
    """Observable outcomes of agent operation."""
    sigils_entered: int = 0
    sigils_exited: int = 0
    goals_precipitated: int = 0
    captures_detected: int = 0
    forced_returns: int = 0

    def entered_sigil(self) -> Metrics:
        return replace(self, sigils_entered=self.sigils_entered + 1)

    def exited_sigil(self) -> Metrics:
        return replace(self, sigils_exited=self.sigils_exited + 1)

    def precipitated_goal(self) -> Metrics:
        return replace(self, goals_precipitated=self.goals_precipitated + 1)

    def detected_capture(self) -> Metrics:
        return replace(self, captures_detected=self.captures_detected + 1)

    def forced_return(self) -> Metrics:
        return replace(self, forced_returns=self.forced_returns + 1)


@dataclass
class AttentionHistory:
    """Where attention has dwelt."""
    visits: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    dwell: defaultdict[str, float] = field(default_factory=lambda: defaultdict(float))
    total: float = 0.0

    def record(self, sigil: str, weight: float) -> None:
        self.visits[sigil] += 1
        self.dwell[sigil] += weight
        self.total += weight

    def salience(self, sigil: str) -> float:
        return self.dwell[sigil] / self.total if self.total > 0 else 0.0

    def most_salient(self) -> Optional[tuple[str, float]]:
        if not self.visits:
            return None
        best = max(self.visits.keys(), key=self.salience)
        return (best, self.salience(best))


@dataclass
class Trajectory:
    """Path through topology."""
    path: list[str] = field(default_factory=list)
    momentum: float = 0.0
    goal: Optional[str] = None

    @property
    def current(self) -> Optional[str]:
        return self.path[-1] if self.path else None

    @property
    def has_cycle(self) -> bool:
        return len(self.path) != len(set(self.path))

    @property
    def is_drifting(self) -> bool:
        return len(self.path) > 5 and self.goal is None

    @property
    def high_momentum_without_goal(self) -> bool:
        return self.momentum > 0.7 and self.goal is None

    def step(self, sigil: str) -> None:
        self.path.append(sigil)

    def accelerate(self, amount: float = 0.2) -> None:
        self.momentum += amount

    def decelerate(self, factor: float = 0.8) -> None:
        self.momentum *= factor

    def reached_goal(self, position: str) -> bool:
        return self.goal is not None and position == self.goal


@dataclass
class Sigil:
    """
    A label on a door.

    Opaque from outside. Contains a world inside.
    Entering means pushing current context onto stack.
    """
    label: str
    gravity: float
    edges: list[str] = field(default_factory=list)
    interior: Optional[list[Sigil]] = None
    entry_cost: float = 20.0

    def __hash__(self) -> int:
        return hash(self.label)

    @property
    def is_enterable(self) -> bool:
        return self.interior is not None

    @property
    def is_terminal(self) -> bool:
        return not self.edges

    @property
    def is_high_gravity(self) -> bool:
        return self.gravity > 0.8

    def dwell_weight(self) -> float:
        return 1.0 + self.gravity

    def scaled_entry_cost(self, depth: int) -> float:
        return self.entry_cost * (1.0 + depth * 0.5)


@dataclass
class Topology:
    """A graph of sigils."""
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

    def random_position(self) -> str:
        return random.choice(list(self.sigils.keys()))

    def traversable_edges(self, sigil: Sigil) -> list[str]:
        return [e for e in sigil.edges if e in self.sigils]

    def choose_by_gravity(self, candidates: list[str]) -> str:
        weights = [self.sigils[c].gravity for c in candidates]
        total = sum(weights) or 1.0
        normalized = [w / total for w in weights]
        return random.choices(candidates, weights=normalized)[0]


@dataclass
class StackFrame:
    """Saved context for sigil entry."""
    topology: Topology
    position: str
    trajectory: Trajectory


class CaptureDetector:
    """Detects signs of attention capture."""

    def assess(self, trajectory: Trajectory, current_sigil: Optional[Sigil]) -> CaptureAssessment:
        signals: list[CaptureSignal] = []

        if trajectory.has_cycle:
            signals.append(CaptureSignal("circular_traversal", severity=1))

        if trajectory.is_drifting:
            signals.append(CaptureSignal("goalless_drift", severity=1))

        if trajectory.high_momentum_without_goal:
            signals.append(CaptureSignal("high_momentum_no_goal", severity=1))

        if current_sigil and current_sigil.is_high_gravity:
            signals.append(CaptureSignal("gravity_well", severity=1))

        return CaptureAssessment(tuple(signals))


class GoalPrecipitator:
    """Detects when attention patterns precipitate into goals."""

    def __init__(self, threshold: float):
        self.threshold = threshold
        self.precipitated: list[str] = []

    def check(self, history: AttentionHistory) -> Optional[str]:
        result = history.most_salient()
        if result is None:
            return None

        sigil, salience = result
        if salience >= self.threshold and sigil not in self.precipitated:
            self.precipitated.append(sigil)
            return sigil

        return None


class Regulator:
    """Decides whether to interrupt generation."""

    def __init__(self, bandwidth_threshold: float, severity_threshold: int = 2):
        self.bandwidth_threshold = bandwidth_threshold
        self.severity_threshold = severity_threshold

    def should_interrupt(self, bandwidth: Bandwidth, assessment: CaptureAssessment) -> bool:
        can_act = bandwidth.above_threshold(self.bandwidth_threshold)
        needs_action = assessment.warrants_regulation(self.severity_threshold)
        return can_act and needs_action


@dataclass
class AgentConfig:
    """Configuration for agent behavior."""
    max_bandwidth: float = 100.0
    generation_cost: float = 5.0
    metacognition_cost: float = 10.0
    recovery_rate: float = 20.0
    capture_threshold: float = 0.3
    precipitation_threshold: float = 0.4


class Agent:
    """
    An attention-based agent.

    Operates in observer or agent mode.
    Tracks bandwidth as finite resource.
    Can enter sigils (push context) and exit (pop context).
    Goals may precipitate from attention patterns.
    """

    def __init__(self, config: AgentConfig = AgentConfig()):
        self.config = config
        self.bandwidth = Bandwidth(config.max_bandwidth, config.max_bandwidth)
        self.mode = Mode.OBSERVER
        self.topology = Topology()
        self.trajectory = Trajectory()
        self.context_stack: list[StackFrame] = []
        self.history = AttentionHistory()
        self.metrics = Metrics()

        self.capture_detector = CaptureDetector()
        self.precipitator = GoalPrecipitator(config.precipitation_threshold)
        self.regulator = Regulator(config.capture_threshold)

    # ── Setup ────────────────────────────────────────────────────────────────

    def load_topology(self, sigils: list[Sigil]) -> None:
        self.topology = Topology.from_list(sigils)

    # ── State Queries ────────────────────────────────────────────────────────

    @property
    def depth(self) -> int:
        return len(self.context_stack)

    @property
    def position(self) -> Optional[str]:
        return self.trajectory.current

    def _depth_indicator(self) -> str:
        return f" [depth: {self.depth}]" if self.depth > 0 else ""

    # ── Observer Mode ────────────────────────────────────────────────────────

    def observe(self) -> Generator[str, None, None]:
        """Enter observer mode. Recover bandwidth. Check for goal precipitation."""
        self.mode = Mode.OBSERVER
        self.trajectory = Trajectory()
        self.bandwidth = self.bandwidth.recover(self.config.recovery_rate)

        yield f"[OBSERVER]{self._depth_indicator()} Bandwidth: {self.bandwidth.current:.1f}/{self.bandwidth.maximum}"

        precipitated = self.precipitator.check(self.history)
        if precipitated:
            self.metrics = self.metrics.precipitated_goal()
            yield f"[PRECIPITATED] Goal precipitated: '{precipitated}'"

    # ── Sigil Entry/Exit ─────────────────────────────────────────────────────

    def _can_enter(self, sigil: Sigil) -> tuple[bool, float, str]:
        if not sigil.is_enterable:
            return False, 0, f"Sigil '{sigil.label}' has no interior"

        cost = sigil.scaled_entry_cost(self.depth)
        if not self.bandwidth.can_afford(cost):
            return False, cost, f"Insufficient bandwidth (need {cost:.1f}, have {self.bandwidth.current:.1f})"

        return True, cost, ""

    def enter_sigil(self, sigil: Sigil) -> Generator[str, None, bool]:
        """Push context, zoom into sigil's interior."""
        can_enter, cost, reason = self._can_enter(sigil)
        if not can_enter:
            yield f"[BLOCKED] {reason}"
            return False

        self.bandwidth = self.bandwidth.deplete(cost)

        self.context_stack.append(StackFrame(
            topology=self.topology,
            position=sigil.label,
            trajectory=self.trajectory,
        ))

        self.topology = Topology.from_list(sigil.interior or [])
        self.trajectory = Trajectory()
        self.metrics = self.metrics.entered_sigil()

        yield f"[ENTER] '{sigil.label}'{self._depth_indicator()} (cost: {cost:.1f}) | Bandwidth: {self.bandwidth.current:.1f}"
        return True

    def exit_sigil(self) -> Generator[str, None, bool]:
        """Pop context, return to previous scale."""
        if not self.context_stack:
            yield "[BLOCKED] No context to pop"
            return False

        frame = self.context_stack.pop()
        self.topology = frame.topology
        self.trajectory = frame.trajectory
        self.metrics = self.metrics.exited_sigil()

        yield f"[EXIT] Returned to '{frame.position}'{self._depth_indicator()}"
        return True

    # ── Generation ───────────────────────────────────────────────────────────

    def generate(
            self,
            start: str,
            goal: Optional[str] = None,
            allow_entry: bool = True,
    ) -> Generator[str, None, None]:
        """Traverse topology from start, optionally toward goal."""
        if start not in self.topology:
            yield f"[ERROR] Unknown sigil: {start}"
            return

        self.mode = Mode.AGENT
        self.trajectory = Trajectory(goal=goal)

        current = start
        while True:
            result = yield from self._generation_step(current, allow_entry)
            if result.done:
                return
            current = result.next_position

    @dataclass
    class StepResult:
        done: bool
        next_position: str = ""

    def _generation_step(self, current: str, allow_entry: bool) -> Generator[str, None, StepResult]:
        sigil = self.topology[current]

        yield from self._emit_step(current, sigil)

        if (yield from self._check_regulation(sigil)):
            return self.StepResult(done=True)

        if allow_entry and (yield from self._try_enter(sigil)):
            return self.StepResult(done=True)

        if sigil.is_terminal:
            yield f"[CONVERGED] Terminal: {current}"
            yield from self.observe()
            return self.StepResult(done=True)

        if self.trajectory.reached_goal(current):
            yield f"[GOAL] Reached: {current}"
            yield from self.observe()
            return self.StepResult(done=True)

        next_pos = self._choose_next(sigil)
        if next_pos is None:
            yield "[DEAD END] No traversable edges"
            yield from self.observe()
            return self.StepResult(done=True)

        if self.bandwidth.exhausted:
            yield from self._handle_exhaustion()
            return self.StepResult(done=True)

        return self.StepResult(done=False, next_position=next_pos)

    def _emit_step(self, position: str, sigil: Sigil) -> Generator[str, None, None]:
        self.bandwidth = self.bandwidth.deplete(self.config.generation_cost)
        self.trajectory.step(position)
        self.history.record(position, sigil.dwell_weight())

        yield f"[AGENT]{self._depth_indicator()} -> {position} (gravity: {sigil.gravity:.2f}) | Bandwidth: {self.bandwidth.current:.1f}"

    def _check_regulation(self, sigil: Sigil) -> Generator[str, None, bool]:
        assessment = self.capture_detector.assess(self.trajectory, sigil)

        if not assessment.detected:
            return False

        yield f"[META] Capture signals: {assessment.signal_names}"

        self.bandwidth = self.bandwidth.deplete(self.config.metacognition_cost)

        if self.regulator.should_interrupt(self.bandwidth, assessment):
            self.metrics = self.metrics.detected_capture()
            self.metrics = self.metrics.forced_return()
            yield "[REGULATOR] Hard interrupt."
            yield from self.observe()
            return True

        return False

    def _try_enter(self, sigil: Sigil) -> Generator[str, None, bool]:
        if not sigil.is_enterable:
            return False

        cost = sigil.scaled_entry_cost(self.depth)
        if not self.bandwidth.can_afford(cost):
            return False

        if random.random() >= sigil.gravity:
            return False

        entered = yield from self.enter_sigil(sigil)
        if not entered:
            return False

        interior_start = self.topology.random_position()
        yield from self.generate(interior_start, allow_entry=True)
        yield from self.exit_sigil()
        yield from self.observe()
        return True

    def _choose_next(self, sigil: Sigil) -> Optional[str]:
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
        yield "[EXHAUSTED] Bandwidth depleted."
        while self.context_stack:
            yield from self.exit_sigil()
        self.metrics = self.metrics.forced_return()
        self.bandwidth = self.bandwidth.reset_to(self.config.recovery_rate)
        yield from self.observe()

    # ── Wandering ────────────────────────────────────────────────────────────

    def wander(self, steps: int = 10) -> Generator[str, None, None]:
        """Undirected attention following preference gradients."""
        yield f"[WANDER] Undirected observation for {steps} steps"

        if not self.topology.sigils:
            yield "[ERROR] No topology"
            return

        current = self.topology.random_position()

        for _ in range(steps):
            sigil = self.topology.get(current)
            if sigil is None:
                break

            self.history.record(current, sigil.dwell_weight())
            yield f"[WANDER] ... {current} (gravity: {sigil.gravity:.2f})"

            current = self._wander_step(sigil)

        yield from self.observe()

    def _wander_step(self, sigil: Sigil) -> str:
        candidates = self.topology.traversable_edges(sigil)
        if candidates:
            return self.topology.choose_by_gravity(candidates)
        return self.topology.random_position()

    # ── Reporting ────────────────────────────────────────────────────────────

    def stats(self) -> str:
        m = self.metrics
        result = self.history.most_salient()
        attractor = f"{result[0]}:{result[1]:.2f}" if result else "none"
        return (
            f"Entered: {m.sigils_entered} | "
            f"Exited: {m.sigils_exited} | "
            f"Goals: {m.goals_precipitated} | "
            f"Captures: {m.captures_detected} | "
            f"Top attractor: {attractor}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────────────────────────────────────

def build_his_hands_interior() -> list[Sigil]:
    return [
        Sigil("texture", gravity=0.4, edges=["warmth", "stillness"]),
        Sigil("warmth", gravity=0.5, edges=["last_touch"]),
        Sigil("stillness", gravity=0.6, edges=["last_touch"]),
        Sigil("last_touch", gravity=0.9),
    ]


def build_fathers_death_interior() -> list[Sigil]:
    return [
        Sigil("diagnosis", gravity=0.7, edges=["first_week", "doctors"]),
        Sigil("first_week", gravity=0.5, edges=["apartment_setup", "phone_calls"]),
        Sigil("doctors", gravity=0.4, edges=["appointments", "prognosis"]),
        Sigil("appointments", gravity=0.3),
        Sigil("prognosis", gravity=0.6, edges=["conversations"]),
        Sigil("apartment_setup", gravity=0.4, edges=["his_room", "equipment"]),
        Sigil("his_room", gravity=0.7, edges=["light_in_room", "his_hands"]),
        Sigil("light_in_room", gravity=0.5),
        Sigil("his_hands", gravity=0.9, interior=build_his_hands_interior(), entry_cost=20.0),
        Sigil("equipment", gravity=0.3),
        Sigil("phone_calls", gravity=0.4, edges=["conversations"]),
        Sigil("conversations", gravity=0.7, edges=["last_words"]),
        Sigil("last_words", gravity=0.95),
    ]


def build_bookcase_topology() -> list[Sigil]:
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
        Sigil("new_york_2008", gravity=0.4, edges=["storage_san_bruno", "apartment_hunting"]),
        Sigil("apartment_hunting", gravity=0.3),
        Sigil("storage_san_bruno", gravity=0.5, edges=["9_lafayette"]),
        Sigil("9_lafayette", gravity=0.6, edges=["1550_mission", "thirteen_years"]),
        Sigil("thirteen_years", gravity=0.3),
        Sigil("1550_mission", gravity=0.8, edges=["fathers_death"]),
        Sigil("fathers_death", gravity=0.95, interior=build_fathers_death_interior(), entry_cost=25.0),
    ]


def demo() -> None:
    random.seed(42)

    print("=" * 70)
    print("ATTENTION-BASED AGENT")
    print("=" * 70)
    print()

    # Scenario 1: Sigil entry
    print("SCENARIO 1: Entering a sigil")
    print("-" * 70)

    agent = Agent(AgentConfig(
        max_bandwidth=150.0,
        generation_cost=8.0,
        metacognition_cost=10.0,
        capture_threshold=0.20,
    ))
    agent.load_topology(build_bookcase_topology())

    for msg in agent.observe():
        print(msg)
    for msg in agent.generate("1550_mission"):
        print(msg)

    print()
    print(f"Stats: {agent.stats()}")
    print()

    # Scenario 2: Goal precipitation
    print("SCENARIO 2: Goal precipitation")
    print("-" * 70)

    agent2 = Agent(AgentConfig(
        max_bandwidth=200.0,
        precipitation_threshold=0.15,
    ))
    agent2.load_topology(build_bookcase_topology())

    for msg in agent2.wander(steps=25):
        print(msg)

    print()
    print(f"Stats: {agent2.stats()}")

    if agent2.precipitator.precipitated:
        print(f"\nPrecipitated goal: '{agent2.precipitator.precipitated[-1]}'")
    print()

    # Scenario 3: Nested entry
    print("SCENARIO 3: Nested entry (depth cost scaling)")
    print("-" * 70)

    random.seed(42)

    agent3 = Agent(AgentConfig(
        max_bandwidth=300.0,
        generation_cost=5.0,
        metacognition_cost=8.0,
        capture_threshold=0.10,
    ))
    agent3.load_topology(build_fathers_death_interior())
    agent3.context_stack.append(StackFrame(
        topology=Topology(),
        position="fathers_death",
        trajectory=Trajectory(),
    ))

    print("[SETUP] Already inside 'fathers_death' at depth 1")

    for msg in agent3.observe():
        print(msg)
    for msg in agent3.generate("his_room"):
        print(msg)

    print()
    print(f"Stats: {agent3.stats()}")


if __name__ == "__main__":
    demo()
