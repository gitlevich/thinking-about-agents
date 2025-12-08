from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.framework.al import (
    Contrast,
    Resolution,
    Frame,
    Choice,
    Sigil,
    Agent,
    History,
)


# Contrasts for "this block of time"
energy = Contrast("energy", "current energy 1–10", Resolution.COARSE, is_self=True)
minutes = Contrast("minutes", "minutes available", Resolution.COARSE)
context = Contrast("context", "where I am / what this block is", Resolution.COARSE)


@dataclass
class Task:
    name: str
    importance: int    # 1–10
    effort: int        # minutes
    fun: int           # 1–10
    deadline_soon: bool


tasks: List[Task] = [
    Task("do_taxes", importance=10, effort=90, fun=1, deadline_soon=True),
    Task("answer_email", importance=5, effort=15, fun=2, deadline_soon=False),
    Task("write_al_notes", importance=8, effort=45, fun=9, deadline_soon=False),
]


class ResponsibleAdult(Sigil):
    """
    Stateless sigil: favors important + urgent tasks that fit this block.
    """

    def __init__(self) -> None:
        super().__init__("responsible_adult", "honor deadlines and importance", 1.0)

    def score(self, frame: Frame, choice: Choice) -> float:
        t: Task = choice.payload
        mins = frame.view(minutes, 60)

        if t.effort > mins:
            return -100.0

        score = 0.0
        score += 3.0 * t.importance
        if t.deadline_soon:
            score += 5.0
        return score


class ArtistChild(Sigil):
    """
    Stateless sigil: favors fun tasks that match current energy.
    """

    def __init__(self) -> None:
        super().__init__("artist_child", "follow interest and energy", 1.0)

    def score(self, frame: Frame, choice: Choice) -> float:
        t: Task = choice.payload
        e = frame.view(energy, 5)
        mins = frame.view(minutes, 60)

        if t.effort > mins:
            return -100.0

        score = 0.0
        score += 2.0 * t.fun

        # penalize things too heavy for current energy
        if t.effort > e * 15:
            score -= 5.0

        return score


def run(agent: Agent, label: str) -> None:
    block = (
        Frame()
        .see(energy, 4)                      # a bit tired
        .see(minutes, 50)                    # 50 minutes
        .see(context, "at desk, afternoon")  # coarse context
    )

    choices = [Choice(t.name, payload=t) for t in tasks]
    history = History(agent=agent)

    chosen, score = agent.choose(block, choices)
    history.record(block, chosen, score)

    print(label)
    print(" goal_hint:", agent.goal_hint)
    print(" frame   :", block)
    print(" choices :", choices)
    print(" chosen  :", chosen, "score:", score)
    print(" narrative:", history.narrative)
    print()


if __name__ == "__main__":
    adult = Agent("me_adult").with_sigils(ResponsibleAdult())
    child = Agent("me_child").with_sigils(ArtistChild())

    run(adult, "Adult mode")
    run(child, "Artist mode")
