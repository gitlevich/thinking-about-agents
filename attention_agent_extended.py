"""
Attention-Based Agent Architecture (Extended)

Adds:
- Sigils as callable contexts (stack-based zoom)
- Goal precipitation from preference gradients

Author: Vladimir Gitlevich
Developed in conversation with Claude.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Generator
from collections import defaultdict
import random


class Mode(Enum):
    OBSERVER = auto()
    AGENT = auto()


@dataclass
class Sigil:
    """
    A sigil is a label on a door.
    
    Opaque from outside (just a label with gravity).
    Contains an entire world inside (interior topology).
    Entering = pushing current context, zooming into interior.
    """
    label: str
    gravity: float
    edges: list[str] = field(default_factory=list)  # Lateral edges (same scale)
    interior: Optional[dict] = None  # Another topology inside (vertical edge)
    entry_cost: float = 20.0  # Bandwidth cost to enter
    
    def __hash__(self):
        return hash(self.label)
    
    @property
    def is_enterable(self) -> bool:
        return self.interior is not None


@dataclass
class Context:
    """A frame on the context stack."""
    topology: dict[str, Sigil]
    position: str
    trajectory: list[str]
    momentum: float
    goal: Optional[str]


@dataclass
class CollapseTracker:
    """Tracks attention patterns for goal precipitation."""
    visit_count: defaultdict = field(default_factory=lambda: defaultdict(int))
    dwell_time: defaultdict = field(default_factory=lambda: defaultdict(float))
    total_attention: float = 0.0
    
    def record_visit(self, sigil: str, duration: float = 1.0):
        self.visit_count[sigil] += 1
        self.dwell_time[sigil] += duration
        self.total_attention += duration
    
    def salience(self, sigil: str) -> float:
        """How much attention has been drawn here relative to total."""
        if self.total_attention == 0:
            return 0.0
        return self.dwell_time[sigil] / self.total_attention
    
    def top_attractors(self, n: int = 3) -> list[tuple[str, float]]:
        """Return the n most attended-to sigils."""
        items = [(s, self.salience(s)) for s in self.visit_count]
        return sorted(items, key=lambda x: -x[1])[:n]


class AttentionAgent:
    """
    Agent with:
    - Observer/agent modes
    - Bandwidth as resource
    - Capture detection and regulation
    - Stack-based sigil entry (context zoom)
    - Goal precipitation from collapse patterns
    """
    
    def __init__(
        self,
        max_bandwidth: float = 100.0,
        generation_cost: float = 5.0,
        metacognition_cost: float = 10.0,
        recovery_rate: float = 20.0,
        capture_threshold: float = 0.3,
        crystallization_threshold: float = 0.4,  # Salience needed to precipitate goal
    ):
        self.max_bandwidth = max_bandwidth
        self.bandwidth = max_bandwidth
        self.generation_cost = generation_cost
        self.metacognition_cost = metacognition_cost
        self.recovery_rate = recovery_rate
        self.capture_threshold = capture_threshold
        self.crystallization_threshold = crystallization_threshold
        
        self.mode = Mode.OBSERVER
        self.topology: dict[str, Sigil] = {}
        
        # Stack for sigil entry
        self.context_stack: list[Context] = []
        
        # Current traversal state
        self.trajectory: list[str] = []
        self.momentum: float = 0.0
        self.goal: Optional[str] = None
        
        # Goal precipitation
        self.collapse_tracker = CollapseTracker()
        self.precipitated_goals: list[str] = []
        
        # Metrics
        self.sigils_entered = 0
        self.sigils_exited = 0
        self.goals_precipitated = 0
        self.captures_detected = 0
        self.forced_returns = 0
    
    def build_topology(self, sigils: list[Sigil]):
        for sigil in sigils:
            self.topology[sigil.label] = sigil
    
    @property
    def stack_depth(self) -> int:
        return len(self.context_stack)
    
    @property
    def bandwidth_ratio(self) -> float:
        return self.bandwidth / self.max_bandwidth
    
    @property
    def can_regulate(self) -> bool:
        return self.bandwidth_ratio > self.capture_threshold
    
    def observe(self) -> Generator[str, None, None]:
        """Observer mode. Recover bandwidth. Check for goal precipitation."""
        self.mode = Mode.OBSERVER
        self.trajectory = []
        self.momentum = 0.0
        
        self.bandwidth = min(self.max_bandwidth, self.bandwidth + self.recovery_rate)
        
        # Check for goal precipitation
        precipitated = self._check_precipitation()
        
        depth_indicator = f" [depth: {self.stack_depth}]" if self.stack_depth > 0 else ""
        yield f"[OBSERVER]{depth_indicator} Bandwidth: {self.bandwidth:.1f}/{self.max_bandwidth}"
        
        if precipitated:
            yield f"[PRECIPITATED] Goal crystallized from attention: '{precipitated}'"
    
    def _check_precipitation(self) -> Optional[str]:
        """Check if any sigil has accumulated enough attention to become a goal."""
        for sigil, salience in self.collapse_tracker.top_attractors(1):
            if salience >= self.crystallization_threshold and sigil not in self.precipitated_goals:
                self.precipitated_goals.append(sigil)
                self.goals_precipitated += 1
                return sigil
        return None
    
    def _detect_capture_signals(self) -> list[str]:
        signals = []
        
        if len(self.trajectory) != len(set(self.trajectory)):
            signals.append("circular_traversal")
        
        if len(self.trajectory) > 5 and self.goal is None:
            signals.append("goalless_drift")
        
        if self.momentum > 0.7 and self.goal is None:
            signals.append("high_momentum_no_goal")
        
        if self.trajectory:
            current = self.trajectory[-1]
            if current in self.topology and self.topology[current].gravity > 0.8:
                signals.append("gravity_well")
        
        return signals
    
    def _regulate(self, signals: list[str]) -> bool:
        if not signals:
            return False
        
        self.bandwidth -= self.metacognition_cost
        
        if not self.can_regulate:
            return False
        
        severity = len(signals)
        if severity >= 2:
            self.captures_detected += 1
            return True
        
        return False
    
    def enter_sigil(self, sigil: Sigil) -> Generator[str, None, None]:
        """Push current context, zoom into sigil's interior."""
        if not sigil.is_enterable:
            yield f"[BLOCKED] Sigil '{sigil.label}' has no interior"
            return
        
        # Cost increases with depth
        depth_multiplier = 1.0 + (self.stack_depth * 0.5)
        actual_cost = sigil.entry_cost * depth_multiplier
        
        if self.bandwidth < actual_cost:
            yield f"[BLOCKED] Insufficient bandwidth to enter '{sigil.label}' (need {actual_cost:.1f}, have {self.bandwidth:.1f})"
            return
        
        # Pay entry cost
        self.bandwidth -= actual_cost
        
        # Push current context
        self.context_stack.append(Context(
            topology=self.topology,
            position=sigil.label,
            trajectory=self.trajectory.copy(),
            momentum=self.momentum,
            goal=self.goal,
        ))
        
        # Zoom into interior
        self.topology = {s.label: s for s in sigil.interior}
        self.trajectory = []
        self.momentum = 0.0
        self.goal = None
        
        self.sigils_entered += 1
        
        yield f"[ENTER] Pushed context, entering '{sigil.label}' [depth: {self.stack_depth}] (cost: {actual_cost:.1f}) | Bandwidth: {self.bandwidth:.1f}"
    
    def exit_sigil(self) -> Generator[str, None, None]:
        """Pop context, return to previous scale."""
        if not self.context_stack:
            yield f"[BLOCKED] No context to pop (already at root)"
            return
        
        context = self.context_stack.pop()
        
        self.topology = context.topology
        self.trajectory = context.trajectory
        self.momentum = context.momentum
        self.goal = context.goal
        
        self.sigils_exited += 1
        
        yield f"[EXIT] Popped context, returned to '{context.position}' [depth: {self.stack_depth}]"
    
    def generate(
        self,
        start: str,
        goal: Optional[str] = None,
        allow_entry: bool = True,
    ) -> Generator[str, None, None]:
        """
        Traverse topology from start.
        If allow_entry, may enter sigils that have interiors.
        """
        if start not in self.topology:
            yield f"[ERROR] Unknown sigil: {start}"
            return
        
        self.mode = Mode.AGENT
        self.trajectory = []
        self.momentum = 0.0
        self.goal = goal
        
        current = start
        
        while True:
            self.bandwidth -= self.generation_cost
            self.trajectory.append(current)
            sigil = self.topology[current]
            
            # Record for collapse tracking
            self.collapse_tracker.record_visit(current, duration=1.0 + sigil.gravity)
            
            depth_indicator = f" [depth: {self.stack_depth}]" if self.stack_depth > 0 else ""
            yield f"[AGENT]{depth_indicator} -> {current} (gravity: {sigil.gravity:.2f}) | Bandwidth: {self.bandwidth:.1f}"
            
            # Check for capture
            signals = self._detect_capture_signals()
            if signals:
                yield f"[META] Capture signals: {signals}"
                if self._regulate(signals):
                    self.forced_returns += 1
                    yield f"[REGULATOR] Hard interrupt."
                    yield from self.observe()
                    return
            
            # Decision point: enter sigil, continue laterally, or converge
            
            # Option 1: Enter sigil if enterable and we have bandwidth
            if allow_entry and sigil.is_enterable:
                depth_multiplier = 1.0 + (self.stack_depth * 0.5)
                actual_cost = sigil.entry_cost * depth_multiplier
                if self.bandwidth >= actual_cost:
                    # High gravity sigils are more likely to pull us in
                    if random.random() < sigil.gravity:
                        yield from self.enter_sigil(sigil)
                        # Start traversing interior
                        interior_start = list(self.topology.keys())[0]
                        yield from self.generate(interior_start, allow_entry=True)
                        # After returning from interior, exit back
                        yield from self.exit_sigil()
                        yield from self.observe()
                        return
            
            # Option 2: Terminal - converge
            if not sigil.edges:
                yield f"[CONVERGED] Terminal: {current}"
                yield from self.observe()
                return
            
            # Option 3: Goal reached
            if goal and current == goal:
                yield f"[GOAL] Reached: {goal}"
                yield from self.observe()
                return
            
            # Option 4: Continue laterally
            candidates = [e for e in sigil.edges if e in self.topology]
            if not candidates:
                yield f"[DEAD END] No traversable edges"
                yield from self.observe()
                return
            
            if goal and goal in candidates:
                current = goal
                self.momentum *= 0.8
            else:
                weights = [self.topology[c].gravity for c in candidates]
                total = sum(weights) or 1
                weights = [w/total for w in weights]
                current = random.choices(candidates, weights=weights)[0]
                self.momentum += 0.2
            
            if self.bandwidth <= 0:
                yield f"[EXHAUSTED] Bandwidth depleted."
                # Unwind stack if we're deep
                while self.context_stack:
                    yield from self.exit_sigil()
                self.forced_returns += 1
                self.bandwidth = self.recovery_rate
                yield from self.observe()
                return
    
    def wander(self, steps: int = 10) -> Generator[str, None, None]:
        """
        Undirected attention. Let preference gradients guide.
        Used for goal precipitation.
        """
        yield f"[WANDER] Undirected observation for {steps} steps"
        
        if not self.topology:
            yield f"[ERROR] No topology"
            return
        
        current = random.choice(list(self.topology.keys()))
        
        for _ in range(steps):
            if current not in self.topology:
                break
            
            sigil = self.topology[current]
            self.collapse_tracker.record_visit(current, duration=1.0 + sigil.gravity)
            
            yield f"[WANDER] ... {current} (gravity: {sigil.gravity:.2f})"
            
            if not sigil.edges:
                current = random.choice(list(self.topology.keys()))
            else:
                candidates = [e for e in sigil.edges if e in self.topology]
                if candidates:
                    weights = [self.topology[c].gravity for c in candidates]
                    total = sum(weights) or 1
                    weights = [w/total for w in weights]
                    current = random.choices(candidates, weights=weights)[0]
                else:
                    current = random.choice(list(self.topology.keys()))
        
        yield from self.observe()
    
    def stats(self) -> str:
        attractors = self.collapse_tracker.top_attractors(3)
        attractor_str = ", ".join(f"{s}:{sal:.2f}" for s, sal in attractors)
        return (
            f"Entered: {self.sigils_entered} | Exited: {self.sigils_exited} | "
            f"Goals precipitated: {self.goals_precipitated} | "
            f"Top attractors: [{attractor_str}]"
        )


# --- Demo Topologies ---

def build_his_hands_interior() -> list[Sigil]:
    """Interior of 'his_hands' sigil. Deeper memory."""
    return [
        Sigil("texture", gravity=0.4, edges=["warmth", "stillness"]),
        Sigil("warmth", gravity=0.5, edges=["last_touch"]),
        Sigil("stillness", gravity=0.6, edges=["last_touch"]),
        Sigil("last_touch", gravity=0.9, edges=[]),
    ]


def build_fathers_death_interior() -> list[Sigil]:
    """The interior of the 'fathers_death' sigil. Seven months of structure."""
    return [
        Sigil("diagnosis", gravity=0.7, edges=["first_week", "doctors"]),
        Sigil("first_week", gravity=0.5, edges=["apartment_setup", "phone_calls"]),
        Sigil("doctors", gravity=0.4, edges=["appointments", "prognosis"]),
        Sigil("appointments", gravity=0.3, edges=[]),
        Sigil("prognosis", gravity=0.6, edges=["conversations"]),
        Sigil("apartment_setup", gravity=0.4, edges=["his_room", "equipment"]),
        Sigil("his_room", gravity=0.7, edges=["light_in_room", "his_hands"]),
        Sigil("light_in_room", gravity=0.5, edges=[]),
        # his_hands is enterable - deeper level
        Sigil("his_hands", gravity=0.9, edges=[],
              interior=build_his_hands_interior(), entry_cost=20.0),
        Sigil("equipment", gravity=0.3, edges=[]),
        Sigil("phone_calls", gravity=0.4, edges=["conversations"]),
        Sigil("conversations", gravity=0.7, edges=["last_words"]),
        Sigil("last_words", gravity=0.95, edges=[]),
    ]


def build_bookcase_topology_extended() -> list[Sigil]:
    """Extended topology with enterable sigils."""
    return [
        Sigil("room", gravity=0.1, edges=["bookcase", "window", "chair"]),
        Sigil("bookcase", gravity=0.3, edges=["new_york_2008", "books", "wood"]),
        Sigil("books", gravity=0.2, edges=["reading", "shelf"]),
        Sigil("reading", gravity=0.2, edges=[]),
        Sigil("wood", gravity=0.1, edges=[]),
        Sigil("shelf", gravity=0.1, edges=[]),
        Sigil("window", gravity=0.2, edges=["light", "view"]),
        Sigil("light", gravity=0.3, edges=["morning", "photography"]),
        Sigil("photography", gravity=0.5, edges=["observer_mode"]),
        Sigil("observer_mode", gravity=0.1, edges=[]),
        Sigil("view", gravity=0.2, edges=["city_hall", "cathedral"]),
        Sigil("city_hall", gravity=0.3, edges=[]),
        Sigil("cathedral", gravity=0.2, edges=[]),
        Sigil("chair", gravity=0.1, edges=[]),
        Sigil("morning", gravity=0.2, edges=[]),
        Sigil("new_york_2008", gravity=0.4, edges=["storage_san_bruno", "apartment_hunting"]),
        Sigil("apartment_hunting", gravity=0.3, edges=[]),
        Sigil("storage_san_bruno", gravity=0.5, edges=["9_lafayette"]),
        Sigil("9_lafayette", gravity=0.6, edges=["1550_mission", "thirteen_years"]),
        Sigil("thirteen_years", gravity=0.3, edges=[]),
        Sigil("1550_mission", gravity=0.8, edges=["fathers_death"]),
        # Father's death is now enterable - contains seven months
        Sigil("fathers_death", gravity=0.95, edges=[],
              interior=build_fathers_death_interior(), entry_cost=25.0),
    ]


def demo():
    random.seed(42)
    
    print("=" * 70)
    print("EXTENDED AGENT: SIGILS AS CONTEXT + GOAL PRECIPITATION")
    print("=" * 70)
    print()
    
    # Scenario 1: Enter a sigil
    print("SCENARIO 1: Entering a sigil (stack-based zoom)")
    print("-" * 70)
    
    agent = AttentionAgent(
        max_bandwidth=150.0,
        generation_cost=8.0,
        metacognition_cost=10.0,
        capture_threshold=0.20,
    )
    agent.build_topology(build_bookcase_topology_extended())
    
    for msg in agent.observe():
        print(msg)
    
    # Start at 1550_mission, likely to hit fathers_death and enter
    for msg in agent.generate("1550_mission", allow_entry=True):
        print(msg)
    
    print()
    print(f"Stats: {agent.stats()}")
    print()
    
    # Scenario 2: Goal precipitation through wandering
    print("SCENARIO 2: Goal precipitation from undirected attention")
    print("-" * 70)
    
    agent2 = AttentionAgent(
        max_bandwidth=200.0,
        crystallization_threshold=0.15,  # Threshold for crystallization
    )
    agent2.build_topology(build_bookcase_topology_extended())
    
    # Wander and let attention accumulate
    for msg in agent2.wander(steps=25):
        print(msg)
    
    print()
    print(f"Stats: {agent2.stats()}")
    
    if agent2.precipitated_goals:
        print(f"\nPrecipitated goal: '{agent2.precipitated_goals[-1]}'")
        print("Goal emerged from attention patterns, not injection.")
    print()
    
    # Scenario 3: Nested sigil entry - depth cost scaling
    print("SCENARIO 3: Nested entry (depth cost scaling)")
    print("-" * 70)
    
    random.seed(42)
    
    agent3 = AttentionAgent(
        max_bandwidth=300.0,
        generation_cost=5.0,
        metacognition_cost=8.0,
        capture_threshold=0.10,
    )
    
    # Build fathers_death interior directly with nested his_hands
    interior_topology = build_fathers_death_interior()
    agent3.build_topology(interior_topology)
    
    # Simulate being at depth 1 already (inside fathers_death)
    agent3.context_stack.append(Context(
        topology={},  # Outer context (placeholder)
        position="fathers_death",
        trajectory=[],
        momentum=0.0,
        goal=None,
    ))
    
    print("[SETUP] Already inside 'fathers_death' at depth 1")
    
    for msg in agent3.observe():
        print(msg)
    
    # Start at his_room - will hit his_hands which is enterable
    for msg in agent3.generate("his_room", allow_entry=True):
        print(msg)
    
    print()
    print(f"Stats: {agent3.stats()}")
    print("Entry cost at depth 1: base * 1.5 = 30.0")
    print("Entry cost at depth 2: base * 2.0 = 40.0")


if __name__ == "__main__":
    demo()
