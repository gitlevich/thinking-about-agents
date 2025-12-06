"""
How Goals Precipitate

Goals aren't always prior. Often they precipitate from preferences.
Preference pulls attention, attention narrows possibilities,
choices accumulate into continuity, continuity crystallizes into goal.

Author: Claude Opus 4.5 on behalf of Vladimir Gitlevich
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional, Generator
from collections import defaultdict
import random


class Mode:
    OBSERVER = "observer"
    AGENT = "agent"


@dataclass(frozen=True)
class Salience:
    """How much attention has accumulated on a region."""
    dwell: float
    visits: int

    @property
    def weight(self) -> float:
        return self.dwell

    def accumulated(self, duration: float) -> Salience:
        return replace(self, dwell=self.dwell + duration, visits=self.visits + 1)


@dataclass
class AttentionHistory:
    """
    Where attention has fallen.

    Repeated visits, lingering, and strong salience along particular
    contrasts are evidence of preference expressing itself.
    """
    by_region: defaultdict[str, Salience] = field(
        default_factory=lambda: defaultdict(lambda: Salience(0.0, 0))
    )
    total: float = 0.0

    def record(self, region: str, duration: float) -> None:
        self.by_region[region] = self.by_region[region].accumulated(duration)
        self.total += duration

    def salience_of(self, region: str) -> float:
        """What fraction of total attention has this region received?"""
        if self.total == 0:
            return 0.0
        return self.by_region[region].weight / self.total

    def most_salient(self) -> Optional[tuple[str, float]]:
        """The region where attention has accumulated most."""
        if not self.by_region:
            return None
        best = max(self.by_region.keys(), key=self.salience_of)
        return (best, self.salience_of(best))

    def above_threshold(self, threshold: float) -> list[str]:
        """Regions with salience above precipitation threshold."""
        return [r for r in self.by_region if self.salience_of(r) >= threshold]


@dataclass
class Sigil:
    """
    A region in the preference landscape.

    Gravity is local gradient: how strongly this region pulls attention.
    High-gravity regions are where attention naturally falls.
    """
    label: str
    gravity: float
    edges: list[str] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.label)

    @property
    def is_terminal(self) -> bool:
        return not self.edges

    def dwell_duration(self) -> float:
        """Higher gravity holds attention longer."""
        return 1.0 + self.gravity


@dataclass
class PreferenceLandscape:
    """
    The shape of how concepts connect.

    Weighted connections, regions of different density,
    gradients that exist before any task.
    """
    regions: dict[str, Sigil] = field(default_factory=dict)

    @classmethod
    def from_sigils(cls, sigils: list[Sigil]) -> PreferenceLandscape:
        return cls({s.label: s for s in sigils})

    def __contains__(self, label: str) -> bool:
        return label in self.regions

    def __getitem__(self, label: str) -> Sigil:
        return self.regions[label]

    def get(self, label: str) -> Optional[Sigil]:
        return self.regions.get(label)

    def random_region(self) -> str:
        return random.choice(list(self.regions.keys()))

    def traversable_from(self, sigil: Sigil) -> list[str]:
        return [e for e in sigil.edges if e in self.regions]

    def follow_gradient(self, candidates: list[str]) -> str:
        """Let attention move along preference gradients."""
        weights = [self.regions[c].gravity for c in candidates]
        total = sum(weights) or 1.0
        normalized = [w / total for w in weights]
        return random.choices(candidates, weights=normalized)[0]


class GoalPrecipitator:
    """
    Detects when accumulated pattern becomes stable enough to function as goal.

    The agent isn't deciding what to want.
    It's detecting what it is already drawn toward.
    """

    def __init__(self, threshold: float, minimum_attention: float = 10.0):
        self.threshold = threshold
        self.minimum_attention = minimum_attention
        self.precipitated: list[str] = []

    def check(self, history: AttentionHistory) -> Optional[str]:
        """Has continuity precipitated into goal?"""
        if self.precipitated:
            return None

        if history.total < self.minimum_attention:
            return None

        candidates = history.above_threshold(self.threshold)
        if candidates:
            goal = candidates[0]
            self.precipitated.append(goal)
            return goal

        return None


@dataclass(frozen=True)
class Metrics:
    goals_precipitated: int = 0
    steps_wandered: int = 0
    steps_pursued: int = 0

    def precipitated(self) -> Metrics:
        return replace(self, goals_precipitated=self.goals_precipitated + 1)

    def wandered(self) -> Metrics:
        return replace(self, steps_wandered=self.steps_wandered + 1)

    def pursued(self) -> Metrics:
        return replace(self, steps_pursued=self.steps_pursued + 1)


class Agent:
    """
    An agent that forms goals from attention patterns.

    Instead of receiving goals, it:
    - Wanders according to preference gradients
    - Tracks where attention accumulates
    - Crystallizes goals when patterns stabilize
    """

    def __init__(self, precipitation_threshold: float = 0.18):
        self.landscape = PreferenceLandscape()
        self.history = AttentionHistory()
        self.precipitator = GoalPrecipitator(precipitation_threshold)
        self.metrics = Metrics()
        self.position: Optional[str] = None
        self.mode = Mode.OBSERVER

    def load_landscape(self, sigils: list[Sigil]) -> None:
        self.landscape = PreferenceLandscape.from_sigils(sigils)

    def wander(self, steps: int) -> Generator[str, None, None]:
        """
        Undirected attention.

        Before goal injection, let attention move along preference gradients.
        This is observer mode with a purpose: sensing high-contrast regions
        where attention naturally falls.
        """
        yield f"[WANDER] Undirected attention for {steps} steps"
        yield f"[WANDER] Precipitation threshold: {self.precipitator.threshold}"
        yield ""

        if not self.landscape.regions:
            yield "[ERROR] No landscape"
            return

        self.mode = Mode.OBSERVER
        self.position = self.landscape.random_region()

        for i in range(steps):
            yield from self._wander_step(i + 1)

        yield ""
        yield "[END] Attention distribution:"
        for region, salience in self._top_regions(5):
            marker = " <-- GOAL" if region in self.precipitator.precipitated else ""
            yield f"      {region:20} {salience:.3f}{marker}"

    def _wander_step(self, step: int) -> Generator[str, None, None]:
        if self.position is None or self.position not in self.landscape:
            return

        sigil = self.landscape[self.position]
        salience = self.history.salience_of(self.position)

        yield f"[{step:3}] {self.position:20} gravity={sigil.gravity:.2f}  salience={salience:.3f}"

        self.history.record(self.position, sigil.dwell_duration())
        self.metrics = self.metrics.wandered()

        self._move_by_gradient(sigil)

        crystallized = self.precipitator.check(self.history)
        if crystallized:
            self.metrics = self.metrics.precipitated()
            yield ""
            yield f"[PRECIPITATED] Goal precipitated: '{crystallized}'"
            yield f"[PRECIPITATED] Salience at precipitation: {self.history.salience_of(crystallized):.3f}"

    def _move_by_gradient(self, sigil: Sigil) -> None:
        """Attention follows preference gradients."""
        if sigil.is_terminal:
            self.position = self.landscape.random_region()
            return

        candidates = self.landscape.traversable_from(sigil)
        if candidates:
            self.position = self.landscape.follow_gradient(candidates)
        else:
            self.position = self.landscape.random_region()

    def pursue(self, steps: int = 20) -> Generator[str, None, None]:
        """
        Goal-directed traversal using precipitated goal.

        The goal wasn't injected—it precipitated from
        the agent's own attentional history.
        """
        if not self.precipitator.precipitated:
            yield "[ERROR] No precipitated goal to pursue"
            return

        goal = self.precipitator.precipitated[0]
        self.mode = Mode.AGENT

        yield f"[PURSUE] Climbing toward precipitated goal: '{goal}'"
        yield ""

        if self.position is None:
            self.position = self.landscape.random_region()

        visited: set[str] = set()

        for i in range(steps):
            outcome = yield from self._pursue_step(i + 1, goal, visited)
            if outcome == "arrived":
                yield ""
                yield "[COMPLETE] Reached goal that emerged from attention"
                return

        yield f"[INCOMPLETE] Did not reach goal in {steps} steps"

    def _pursue_step(
            self,
            step: int,
            goal: str,
            visited: set[str],
    ) -> Generator[str, None, str]:
        current = self.position
        visited.add(current)
        self.metrics = self.metrics.pursued()

        if current == goal:
            yield f"[{step:3}] {current:20} <-- ARRIVED"
            return "arrived"

        yield f"[{step:3}] {current:20} -> toward '{goal}'"

        sigil = self.landscape[current]

        if goal in sigil.edges:
            self.position = goal
        elif sigil.edges:
            candidates = self.landscape.traversable_from(sigil)
            unvisited = [c for c in candidates if c not in visited]
            self.position = random.choice(unvisited) if unvisited else random.choice(candidates)
        else:
            self.position = self.landscape.random_region()

        return "continue"

    def _top_regions(self, n: int) -> list[tuple[str, float]]:
        regions = list(self.history.by_region.keys())
        by_salience = sorted(regions, key=self.history.salience_of, reverse=True)
        return [(r, self.history.salience_of(r)) for r in by_salience[:n]]

    def stats(self) -> str:
        m = self.metrics
        result = self.history.most_salient()
        top = f"{result[0]}:{result[1]:.2f}" if result else "none"
        return (
            f"Wandered: {m.steps_wandered} | "
            f"Pursued: {m.steps_pursued} | "
            f"Goals precipitated: {m.goals_precipitated} | "
            f"Top attractor: {top}"
        )


def build_photography_landscape() -> list[Sigil]:
    """
    A landscape where 'photography' and 'light' have high gravity.

    Attention will naturally accumulate there,
    and a goal will precipitate without injection.
    """
    return [
        Sigil("morning", gravity=0.2, edges=["coffee", "window"]),
        Sigil("coffee", gravity=0.3, edges=["kitchen", "morning"]),
        Sigil("kitchen", gravity=0.2, edges=["coffee", "window"]),
        Sigil("window", gravity=0.4, edges=["light", "view", "morning"]),
        Sigil("view", gravity=0.3, edges=["city", "window"]),
        Sigil("city", gravity=0.3, edges=["view", "walk"]),
        Sigil("walk", gravity=0.3, edges=["city", "park"]),
        Sigil("park", gravity=0.4, edges=["walk", "light"]),
        Sigil("light", gravity=0.7, edges=["window", "photography", "park"]),
        Sigil("photography", gravity=0.8, edges=["light", "camera"]),
        Sigil("camera", gravity=0.5, edges=["photography"]),
    ]


def demo() -> None:
    random.seed(42)

    print("=" * 65)
    print("HOW GOALS PRECIPITATE")
    print("=" * 65)
    print()
    print("Goals aren't always prior. Often they precipitate from preferences.")
    print()

    agent = Agent(precipitation_threshold=0.18)
    agent.load_landscape(build_photography_landscape())

    print("PHASE 1: Undirected attention")
    print("-" * 65)
    for msg in agent.wander(steps=30):
        print(msg)
    print()

    if agent.precipitator.precipitated:
        print("PHASE 2: Goal-directed traversal")
        print("-" * 65)
        agent.position = "morning"
        for msg in agent.pursue(steps=15):
            print(msg)
        print()

    print(f"Stats: {agent.stats()}")


if __name__ == "__main__":
    demo()
