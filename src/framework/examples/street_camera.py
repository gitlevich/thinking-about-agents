# examples/street_camera.py
from __future__ import annotations

from dataclasses import dataclass

from framework.al import (
    Contrast,
    Resolution,
    Frame,
    Choice,
    Sigil,
    Agent,
    History,
)

# World-side contrasts
light = Contrast("light", "quality of light 0–10", Resolution.COARSE)
crowd = Contrast("crowd", "how many people around 0–10", Resolution.COARSE)
threat = Contrast("threat", "perceived threat 0–10", Resolution.COARSE)
subject_interest = Contrast("subject_interest", "how interesting the subject is 0–10", Resolution.COARSE)
distance = Contrast("distance", "how close I must get 0–10", Resolution.COARSE)

# I-side / proprioception / telemetry
energy = Contrast("energy", "current energy 0–10", Resolution.COARSE, is_self=True)
anxiety = Contrast("anxiety", "street anxiety 0–10", Resolution.COARSE, is_self=True)
overload = Contrast("overload", "sensory / cognitive overload 0–10", Resolution.COARSE, is_self=True)
creative_hunger = Contrast("creative_hunger", "need to make an image 0–10", Resolution.COARSE, is_self=True)


@dataclass
class Scene:
    desc: str


# Choices at this scale
SHOOT = Choice("shoot", payload=Scene("raise camera and take the shot"))
WALK_ON = Choice("walk_on", payload=Scene("keep walking, no shot"))
CROSS_STREET = Choice("cross_street", payload=Scene("cross street, maybe re-approach"))


class StreetHunter(Sigil):
    """
    Wants strong subject + good light, especially when creative hunger is high.
    """

    def __init__(self) -> None:
        super().__init__("street_hunter", "make compelling street images", weight=1.0)

    def score(self, frame: Frame, choice: Choice) -> float:
        if choice.label == "walk_on":
            base = -1.0
        elif choice.label == "shoot":
            base = 1.0
        elif choice.label == "cross_street":
            base = 0.0
        else:
            base = 0.0

        s = frame.view(subject_interest, 0.0)
        l = frame.view(light, 0.0)
        hunger = frame.view(creative_hunger, 0.0)

        score = base

        if choice.label == "shoot":
            score += 0.4 * s
            score += 0.2 * l
            score += 0.3 * hunger

        if choice.label == "walk_on":
            # walking past a strong scene is painful for this sigil
            score -= 0.3 * s
            score -= 0.2 * hunger

        if choice.label == "cross_street":
            # neutral, slightly positive if subject is interesting
            score += 0.1 * s

        return score


class SafetyFirst(Sigil):
    """
    Cares about perceived threat and distance needed to get the shot.
    """

    def __init__(self) -> None:
        super().__init__("safety_first", "stay physically safe", weight=1.0)

    def score(self, frame: Frame, choice: Choice) -> float:
        t = frame.view(threat, 0.0)
        d = frame.view(distance, 0.0)

        # default: fine to do nothing
        if choice.label == "walk_on":
            score = 2.0
        else:
            score = 0.0

        danger = 0.6 * t + 0.4 * d

        if choice.label == "shoot":
            score -= 1.5 * danger
        if choice.label == "cross_street":
            # crossing away from danger is good, towards danger is bad.
            score += 0.5
            score -= 0.5 * danger

        return score


class SelfCare(Sigil):
    """
    Reads proprioception as telemetry:
    backs off if anxiety/overload are high and energy is low.
    """

    def __init__(self) -> None:
        super().__init__("self_care", "protect attention and nervous system", weight=1.0)

    def score(self, frame: Frame, choice: Choice) -> float:
        e = frame.view(energy, 5.0)
        a = frame.view(anxiety, 0.0)
        o = frame.view(overload, 0.0)

        # simple scalar "strain"
        strain = 0.6 * a + 0.4 * o

        if choice.label == "walk_on":
            score = 0.5 * strain  # the more strained, the more walk_on is attractive
        else:
            score = 0.0

        if choice.label == "shoot":
            # if energy is low and strain high, penalize shooting
            if e < 4.0 and strain > 4.0:
                score -= 4.0
            # if energy high and strain low, small positive
            if e > 6.0 and strain < 3.0:
                score += 1.0

        if choice.label == "cross_street":
            # mild reset: good when strain is moderate
            if 3.0 <= strain <= 6.0:
                score += 1.0

        return score

    def learn(self, frame: Frame, choice: Choice) -> None:
        # toy adaptation: if we choose walk_on repeatedly at high strain,
        # lower future creative_hunger in state (as if giving up a bit).
        if choice.label == "walk_on":
            a = frame.view(anxiety, 0.0)
            o = frame.view(overload, 0.0)
            if a + o > 8.0:
                self.state["burnout"] = self.state.get("burnout", 0.0) + 0.1
        else:
            # any non-avoidant choice slightly reduces burnout
            burnout = self.state.get("burnout", 0.0)
            burnout = max(0.0, burnout - 0.05)
            self.state["burnout"] = burnout


def build_frame(
        *,
        light_val: float,
        crowd_val: float,
        threat_val: float,
        subject_val: float,
        distance_val: float,
        energy_val: float,
        anxiety_val: float,
        overload_val: float,
        hunger_val: float,
) -> Frame:
    return (
        Frame()
        .see(light, light_val)
        .see(crowd, crowd_val)
        .see(threat, threat_val)
        .see(subject_interest, subject_val)
        .see(distance, distance_val)
        .see(energy, energy_val)
        .see(anxiety, anxiety_val)
        .see(overload, overload_val)
        .see(creative_hunger, hunger_val)
    )


def run_scenario(label: str, frame: Frame) -> None:
    hunter = StreetHunter()
    safety = SafetyFirst()
    care = SelfCare()

    agent = Agent("street_me").with_sigils(hunter, safety, care)
    history = History(agent=agent)

    options = [SHOOT, WALK_ON, CROSS_STREET]

    choice, score = agent.choose(frame, options)
    history.record(frame, choice, score)

    print(label)
    print(" goal_hint:", agent.goal_hint)
    print(" frame   :", frame)
    print(" options :", options)
    print(" chosen  :", choice, "score:", score)
    print(" self_care_state:", care.state)
    print(" narrative:", history.narrative)
    print()


if __name__ == "__main__":
    # Same world, two different internal states.

    # World: beautiful but sketchy scene.
    base_kwargs = dict(
        light_val=8.0,
        crowd_val=3.0,
        threat_val=6.0,      # feels a bit sketchy
        subject_val=9.0,     # very interesting subject
        distance_val=7.0,    # need to get quite close
        hunger_val=8.0,      # really want an image
    )

    # Version 1: calm, resourced day.
    frame_calm = build_frame(
        **base_kwargs,
        energy_val=7.0,
        anxiety_val=2.0,
        overload_val=1.0,
    )

    # Version 2: fried, anxious day.
    frame_fried = build_frame(
        **base_kwargs,
        energy_val=3.0,
        anxiety_val=7.0,
        overload_val=6.0,
    )

    run_scenario("Calm day", frame_calm)
    run_scenario("Fried day", frame_fried)
