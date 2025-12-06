"""
Goal Precipitation

Demonstrates: preference landscape, undirected attention, 
collapse tracking, crystallization threshold.

Goals aren't injected. They precipitate from attention.

Author: Vladimir Gitlevich
Developed in conversation with Claude.
"""

from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional, Generator
import random


@dataclass
class Sigil:
    """A node in the preference landscape."""
    label: str
    gravity: float  # Local gradient - how strongly this pulls attention
    edges: list[str] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.label)


@dataclass
class CollapseTracker:
    """
    Tracks where attention goes.
    
    Each visit is a collapse - constraining subsequent observations
    to cohere with the pattern being rendered.
    """
    visit_count: defaultdict = field(default_factory=lambda: defaultdict(int))
    dwell_time: defaultdict = field(default_factory=lambda: defaultdict(float))
    total_attention: float = 0.0
    
    def record(self, sigil: str, weight: float = 1.0):
        """Record attention visiting this sigil."""
        self.visit_count[sigil] += 1
        self.dwell_time[sigil] += weight
        self.total_attention += weight
    
    def salience(self, sigil: str) -> float:
        """What fraction of total attention has this sigil received?"""
        if self.total_attention == 0:
            return 0.0
        return self.dwell_time[sigil] / self.total_attention
    
    def top(self, n: int = 5) -> list[tuple[str, float]]:
        """Most attended sigils."""
        items = [(s, self.salience(s)) for s in self.visit_count]
        return sorted(items, key=lambda x: -x[1])[:n]
    
    def above_threshold(self, threshold: float) -> list[str]:
        """Sigils with salience above threshold."""
        return [s for s, sal in self.top(len(self.visit_count)) if sal >= threshold]


class PrecipitatingAgent:
    """
    An agent that forms goals from attention patterns.
    
    Instead of receiving goals, it:
    1. Wanders according to preference gradients
    2. Tracks where attention accumulates
    3. Crystallizes goals when patterns stabilize
    """
    
    def __init__(
        self,
        crystallization_threshold: float = 0.15,
    ):
        self.crystallization_threshold = crystallization_threshold
        self.topology: dict[str, Sigil] = {}
        self.tracker = CollapseTracker()
        self.precipitated: list[str] = []
        self.position: Optional[str] = None
    
    def build_landscape(self, sigils: list[Sigil]):
        """Build the preference landscape."""
        for sigil in sigils:
            self.topology[sigil.label] = sigil
    
    def _step(self) -> Optional[str]:
        """One step of attention following preference."""
        if self.position is None or self.position not in self.topology:
            return None
        
        sigil = self.topology[self.position]
        
        # Record this collapse
        # Dwell time weighted by gravity - high gravity holds attention longer
        self.tracker.record(self.position, weight=1.0 + sigil.gravity)
        
        # Move according to preference
        if not sigil.edges:
            # Terminal - jump to random location
            self.position = random.choice(list(self.topology.keys()))
        else:
            candidates = [e for e in sigil.edges if e in self.topology]
            if candidates:
                # Follow gravity gradient
                weights = [self.topology[c].gravity for c in candidates]
                total = sum(weights) or 1
                weights = [w / total for w in weights]
                self.position = random.choices(candidates, weights=weights)[0]
            else:
                self.position = random.choice(list(self.topology.keys()))
        
        return self.position
    
    def _check_crystallization(self) -> Optional[str]:
        """Has any pattern accumulated enough to become a goal?"""
        # Only one goal can precipitate
        if self.precipitated:
            return None
        
        # Need minimum attention before anything can crystallize
        if self.tracker.total_attention < 10.0:
            return None
        
        candidates = self.tracker.above_threshold(self.crystallization_threshold)
        if candidates:
            goal = candidates[0]  # Highest salience
            self.precipitated.append(goal)
            return goal
        return None
    
    def wander(self, steps: int) -> Generator[str, None, None]:
        """
        Undirected attention.
        
        Let preference gradients guide movement.
        Track collapses. Check for crystallization.
        """
        if not self.topology:
            yield "[ERROR] No landscape"
            return
        
        self.position = random.choice(list(self.topology.keys()))
        
        yield f"[BEGIN] Undirected attention for {steps} steps"
        yield f"[BEGIN] Crystallization threshold: {self.crystallization_threshold}"
        yield ""
        
        for i in range(steps):
            current = self.position
            sigil = self.topology[current]
            sal = self.tracker.salience(current)
            
            yield f"[{i+1:3}] {current:20} gravity={sigil.gravity:.2f}  salience={sal:.3f}"
            
            self._step()
            
            # Check for crystallization
            crystallized = self._check_crystallization()
            if crystallized:
                yield ""
                yield f"[CRYSTALLIZED] Goal precipitated: '{crystallized}'"
                yield f"[CRYSTALLIZED] Salience at crystallization: {self.tracker.salience(crystallized):.3f}"
        
        yield ""
        yield "[END] Final attention distribution:"
        for sigil, sal in self.tracker.top(5):
            marker = " <-- GOAL" if sigil in self.precipitated else ""
            yield f"      {sigil:20} {sal:.3f}{marker}"
    
    def pursue(self, steps: int = 20) -> Generator[str, None, None]:
        """
        Goal-directed traversal using precipitated goal.
        
        The goal wasn't injected - it emerged from prior attention.
        """
        if not self.precipitated:
            yield "[ERROR] No precipitated goal to pursue"
            return
        
        goal = self.precipitated[0]  # First to crystallize = most salient
        yield f"[PURSUE] Climbing toward precipitated goal: '{goal}'"
        yield ""
        
        if self.position is None:
            self.position = random.choice(list(self.topology.keys()))
        
        visited = set()
        
        for i in range(steps):
            current = self.position
            visited.add(current)
            
            if current == goal:
                yield f"[{i+1:3}] {current:20} <-- ARRIVED"
                yield ""
                yield f"[COMPLETE] Reached goal that emerged from attention"
                return
            
            sigil = self.topology[current]
            yield f"[{i+1:3}] {current:20} -> toward '{goal}'"
            
            # Move toward goal if adjacent
            if goal in sigil.edges:
                self.position = goal
            elif sigil.edges:
                candidates = [e for e in sigil.edges if e in self.topology]
                # Prefer unvisited edges
                unvisited = [c for c in candidates if c not in visited]
                if unvisited:
                    self.position = random.choice(unvisited)
                elif candidates:
                    self.position = random.choice(candidates)
                else:
                    break
            else:
                # Terminal - jump toward goal region
                self.position = random.choice(list(self.topology.keys()))
        
        yield f"[INCOMPLETE] Did not reach goal in {steps} steps"


# --- Demo ---

def build_photography_landscape() -> list[Sigil]:
    """
    A landscape where 'photography' and 'light' have high gravity.
    
    Attention will naturally accumulate there,
    and a goal will precipitate without injection.
    """
    return [
        # Low gravity - attention passes through
        Sigil("morning", gravity=0.2, edges=["coffee", "window"]),
        Sigil("coffee", gravity=0.3, edges=["kitchen", "morning"]),
        Sigil("kitchen", gravity=0.2, edges=["coffee", "window"]),
        
        # Medium gravity
        Sigil("window", gravity=0.4, edges=["light", "view", "morning"]),
        Sigil("view", gravity=0.3, edges=["city", "window"]),
        Sigil("city", gravity=0.3, edges=["view", "walk"]),
        Sigil("walk", gravity=0.3, edges=["city", "park"]),
        Sigil("park", gravity=0.4, edges=["walk", "light"]),
        
        # High gravity - attention dwells here
        Sigil("light", gravity=0.7, edges=["window", "photography", "park"]),
        Sigil("photography", gravity=0.8, edges=["light", "camera"]),
        Sigil("camera", gravity=0.5, edges=["photography"]),
    ]


def demo():
    random.seed(42)
    
    print("=" * 65)
    print("GOAL PRECIPITATION")
    print("=" * 65)
    print()
    print("Goals aren't injected. They precipitate from attention.")
    print()
    
    agent = PrecipitatingAgent(crystallization_threshold=0.18)
    agent.build_landscape(build_photography_landscape())
    
    # Phase 1: Wander - let attention follow preference
    print("PHASE 1: Undirected attention")
    print("-" * 65)
    for msg in agent.wander(steps=30):
        print(msg)
    print()
    
    # Phase 2: Pursue - use the precipitated goal
    if agent.precipitated:
        print("PHASE 2: Goal-directed traversal")
        print("-" * 65)
        # Start somewhere random
        agent.position = "morning"
        for msg in agent.pursue(steps=25):
            print(msg)
    else:
        print("No goal precipitated. Try more steps or lower threshold.")


if __name__ == "__main__":
    demo()
