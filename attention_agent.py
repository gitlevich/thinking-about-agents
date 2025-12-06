"""
Attention-Based Agent Architecture

An agent that can observe, generate, get captured, detect capture, and recover.
Demonstrates: observer/agent modes, bandwidth as resource, capture detection, regulator.

Author: Vladimir Gitlevich
Developed in conversation with Claude.
"""

import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Generator


class Mode(Enum):
    OBSERVER = auto()  # High bandwidth, low energy, registering deltas
    AGENT = auto()      # Generating, traversing, consuming bandwidth


@dataclass
class Sigil:
    """A compressed pointer to a world of context. Opaque from outside, infinite inside."""
    label: str
    gravity: float  # How strongly this attracts attention (0-1)
    edges: list[str] = field(default_factory=list)  # Labels of connected sigils

    def __hash__(self):
        return hash(self.label)


@dataclass
class TrajectoryState:
    """Current state of a narrative traversal."""
    path: list[str] = field(default_factory=list)  # Sigils visited
    momentum: float = 0.0  # Current narrative momentum
    goal: Optional[str] = None  # If goal-directed, what we're climbing toward
    cycles_detected: int = 0  # Signs of circular traversal


class AttentionAgent:
    """
    An agent with explicit attention dynamics.

    Key features:
    - Observer mode as default/refuge
    - Bandwidth as finite resource
    - Capture detection
    - Regulator that can hard-interrupt
    """

    def __init__(
        self,
        max_bandwidth: float = 100.0,
        generation_cost: float = 5.0,
        metacognition_cost: float = 10.0,
        recovery_rate: float = 20.0,
        capture_threshold: float = 0.3,  # Below this, regulator can't fire
    ):
        self.max_bandwidth = max_bandwidth
        self.bandwidth = max_bandwidth
        self.generation_cost = generation_cost
        self.metacognition_cost = metacognition_cost
        self.recovery_rate = recovery_rate
        self.capture_threshold = capture_threshold

        self.mode = Mode.OBSERVER
        self.trajectory: Optional[TrajectoryState] = None
        self.topology: dict[str, Sigil] = {}

        # Metrics
        self.captures_detected = 0
        self.forced_returns = 0
        self.successful_completions = 0

    def add_sigil(self, sigil: Sigil):
        """Add a sigil to the topology."""
        self.topology[sigil.label] = sigil

    def build_topology(self, sigils: list[Sigil]):
        """Build the full topology."""
        for sigil in sigils:
            self.add_sigil(sigil)

    @property
    def bandwidth_ratio(self) -> float:
        return self.bandwidth / self.max_bandwidth

    @property
    def can_regulate(self) -> bool:
        """Regulator needs bandwidth to fire."""
        return self.bandwidth_ratio > self.capture_threshold

    @property
    def is_captured(self) -> bool:
        """Captured = generating but can't regulate."""
        return self.mode == Mode.AGENT and not self.can_regulate

    def observe(self) -> Generator[str, None, None]:
        """
        Observer mode: register deltas without generating.
        Yields observations. Recovers bandwidth.
        """
        self.mode = Mode.OBSERVER
        self.trajectory = None

        # Recover bandwidth
        self.bandwidth = min(self.max_bandwidth, self.bandwidth + self.recovery_rate)

        yield f"[OBSERVER] Bandwidth: {self.bandwidth:.1f}/{self.max_bandwidth} | Present to frame"

    def _detect_capture_signals(self) -> list[str]:
        """Check for signs of capture."""
        signals = []

        if not self.trajectory:
            return signals

        # Circular traversal
        if len(self.trajectory.path) != len(set(self.trajectory.path)):
            signals.append("circular_traversal")
            self.trajectory.cycles_detected += 1

        # Long trajectory without goal progress
        if len(self.trajectory.path) > 5 and self.trajectory.goal is None:
            signals.append("goalless_drift")

        # Momentum without direction
        if self.trajectory.momentum > 0.7 and self.trajectory.goal is None:
            signals.append("high_momentum_no_goal")

        # Approaching high-gravity sigil
        if self.trajectory.path:
            current = self.trajectory.path[-1]
            if current in self.topology and self.topology[current].gravity > 0.8:
                signals.append("gravity_well")

        return signals

    def _regulate(self, signals: list[str]) -> bool:
        """
        Attempt to regulate: interrupt capture if possible.
        Returns True if regulation fired (hard interrupt).
        """
        if not signals:
            return False

        # Regulation costs bandwidth
        self.bandwidth -= self.metacognition_cost

        if not self.can_regulate:
            # Not enough bandwidth to act on what we detected
            return False

        # Decide whether to interrupt
        severity = len(signals)
        if self.trajectory and self.trajectory.cycles_detected > 1:
            severity += 2

        # Higher severity = more likely to interrupt
        if severity >= 2:
            self.captures_detected += 1
            return True

        return False

    def generate(
        self,
        start: str,
        goal: Optional[str] = None
    ) -> Generator[str, None, None]:
        """
        Enter agent mode. Traverse topology from start.
        If goal provided, climb toward it. Otherwise, follow gravity.
        """
        if start not in self.topology:
            yield f"[ERROR] Unknown sigil: {start}"
            return

        self.mode = Mode.AGENT
        self.trajectory = TrajectoryState(goal=goal)

        current = start

        while True:
            # Pay generation cost
            self.bandwidth -= self.generation_cost

            # Record traversal
            self.trajectory.path.append(current)
            sigil = self.topology[current]

            yield f"[AGENT] -> {current} (gravity: {sigil.gravity:.2f}) | Bandwidth: {self.bandwidth:.1f}"

            # Check for capture signals
            signals = self._detect_capture_signals()

            if signals:
                yield f"[META] Capture signals: {signals}"

                if self._regulate(signals):
                    self.forced_returns += 1
                    yield f"[REGULATOR] Hard interrupt. Returning to observer."
                    yield from self.observe()
                    return
                elif self.is_captured:
                    yield f"[CAPTURED] Bandwidth exhausted. Riding trajectory to convergence."

            # Check for convergence (no edges = terminal sigil)
            if not sigil.edges:
                self.successful_completions += 1
                yield f"[CONVERGED] Terminal sigil reached: {current}"
                yield from self.observe()
                return

            # Check for goal reached
            if goal and current == goal:
                self.successful_completions += 1
                yield f"[GOAL] Reached target: {goal}"
                yield from self.observe()
                return

            # Choose next sigil
            if goal and goal in sigil.edges:
                # Goal is adjacent - go there
                current = goal
                self.trajectory.momentum *= 0.8  # Momentum decreases when climbing
            else:
                # Follow gravity or goal-gradient
                candidates = [e for e in sigil.edges if e in self.topology]
                if not candidates:
                    yield f"[DEAD END] No traversable edges"
                    yield from self.observe()
                    return

                if goal:
                    # Goal-directed: prefer edges that might lead toward goal
                    # (In real implementation, this would be more sophisticated)
                    current = random.choice(candidates)
                    self.trajectory.momentum += 0.1
                else:
                    # No goal: follow gravity
                    weights = [self.topology[c].gravity for c in candidates]
                    total = sum(weights) or 1
                    weights = [w/total for w in weights]
                    current = random.choices(candidates, weights=weights)[0]
                    self.trajectory.momentum += 0.2  # Momentum builds when falling

            # Hard bandwidth floor
            if self.bandwidth <= 0:
                yield f"[EXHAUSTED] Bandwidth depleted. Forced return."
                self.forced_returns += 1
                self.bandwidth = self.recovery_rate  # Minimal recovery
                yield from self.observe()
                return

    def stats(self) -> str:
        return (
            f"Captures detected: {self.captures_detected} | "
            f"Forced returns: {self.forced_returns} | "
            f"Completions: {self.successful_completions}"
        )


# --- Demo: The Bookcase Topology ---

def build_bookcase_topology() -> list[Sigil]:
    """
    The topology from the transcript:
    bookcase -> new_york_2008 -> storage_san_bruno -> 9_lafayette -> 1550_mission -> fathers_death

    With some branches and gravity wells.
    """
    return [
        Sigil("room", gravity=0.1, edges=["bookcase", "window", "chair"]),
        Sigil("bookcase", gravity=0.3, edges=["new_york_2008", "books", "wood"]),
        Sigil("books", gravity=0.2, edges=["reading", "shelf"]),
        Sigil("reading", gravity=0.2, edges=[]),  # Terminal
        Sigil("wood", gravity=0.1, edges=[]),  # Terminal
        Sigil("shelf", gravity=0.1, edges=[]),  # Terminal
        Sigil("window", gravity=0.2, edges=["light", "view"]),
        Sigil("light", gravity=0.3, edges=["morning", "photography"]),
        Sigil("photography", gravity=0.5, edges=["observer_mode"]),  # Refuge
        Sigil("observer_mode", gravity=0.1, edges=[]),  # Terminal - the refuge
        Sigil("view", gravity=0.2, edges=["city_hall", "cathedral"]),
        Sigil("city_hall", gravity=0.3, edges=[]),  # Terminal
        Sigil("cathedral", gravity=0.2, edges=[]),  # Terminal
        Sigil("chair", gravity=0.1, edges=[]),  # Terminal
        Sigil("morning", gravity=0.2, edges=[]),  # Terminal

        # The gravity well chain
        Sigil("new_york_2008", gravity=0.4, edges=["storage_san_bruno", "apartment_hunting"]),
        Sigil("apartment_hunting", gravity=0.3, edges=[]),  # Terminal
        Sigil("storage_san_bruno", gravity=0.5, edges=["9_lafayette"]),
        Sigil("9_lafayette", gravity=0.6, edges=["1550_mission", "thirteen_years"]),
        Sigil("thirteen_years", gravity=0.3, edges=[]),  # Terminal
        Sigil("1550_mission", gravity=0.8, edges=["fathers_death"]),  # High gravity
        Sigil("fathers_death", gravity=0.95, edges=[]),  # Terminal, maximum gravity
    ]


def demo():
    """Run a demonstration of the agent."""
    random.seed(42)  # Reproducible demo

    print("=" * 60)
    print("ATTENTION-BASED AGENT DEMO")
    print("=" * 60)
    print()

    # Scenario 1: Agent with healthy bandwidth - can regulate
    print("SCENARIO 1: Healthy bandwidth, entering gravity well")
    print("-" * 60)

    agent = AttentionAgent(
        max_bandwidth=100.0,
        generation_cost=10.0,
        metacognition_cost=12.0,
        capture_threshold=0.25,
    )
    agent.build_topology(build_bookcase_topology())

    for msg in agent.observe():
        print(msg)

    # Start directly at bookcase - more likely to hit the gravity well
    for msg in agent.generate("bookcase"):
        print(msg)
    print()
    print(f"Result: {agent.stats()}")
    print()

    # Scenario 2: Agent with depleted bandwidth - gets captured
    print("SCENARIO 2: Depleted bandwidth, entering gravity well")
    print("-" * 60)

    agent2 = AttentionAgent(
        max_bandwidth=100.0,
        generation_cost=15.0,  # Higher cost
        metacognition_cost=20.0,  # More expensive to regulate
        capture_threshold=0.30,
    )
    agent2.build_topology(build_bookcase_topology())
    agent2.bandwidth = 50.0  # Start depleted

    print(f"[SETUP] Starting with depleted bandwidth: {agent2.bandwidth}")

    # Force into the gravity well chain
    for msg in agent2.generate("new_york_2008"):
        print(msg)
    print()
    print(f"Result: {agent2.stats()}")
    print()

    # Scenario 3: Goal-directed traversal resists gravity
    print("SCENARIO 3: Goal-directed traversal")
    print("-" * 60)

    agent3 = AttentionAgent(
        max_bandwidth=100.0,
        generation_cost=10.0,
        metacognition_cost=12.0,
        capture_threshold=0.25,
    )
    agent3.build_topology(build_bookcase_topology())

    for msg in agent3.observe():
        print(msg)

    # Goal: get to photography (refuge) from window
    for msg in agent3.generate("window", goal="photography"):
        print(msg)
    print()
    print(f"Result: {agent3.stats()}")
    print()

    # Scenario 4: Successful regulation - agent catches itself
    print("SCENARIO 4: Successful regulation (catches itself)")
    print("-" * 60)

    agent4 = AttentionAgent(
        max_bandwidth=150.0,  # More bandwidth
        generation_cost=8.0,   # Lower cost
        metacognition_cost=10.0,
        capture_threshold=0.20,  # Lower threshold - easier to regulate
    )
    agent4.build_topology(build_bookcase_topology())

    # Add a loop to the topology to trigger cycle detection
    agent4.topology["9_lafayette"].edges.append("storage_san_bruno")  # Create cycle

    for msg in agent4.observe():
        print(msg)

    for msg in agent4.generate("new_york_2008"):
        print(msg)
    print()
    print(f"Result: {agent4.stats()}")


if __name__ == "__main__":
    demo()
