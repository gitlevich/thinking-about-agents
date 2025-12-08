# src/framework/examples/street_walk.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from framework.al import Agent, History, Frame, Regulator as BaseRegulator, Intervention

from framework.examples.street_camera import (
    StreetHunter,
    SafetyFirst,
    SelfCare,
    light,
    crowd,
    threat,
    subject_interest,
    distance,
    energy,
    anxiety,
    overload,
    creative_hunger,
    SHOOT,
    WALK_ON,
    CROSS_STREET,
)


@dataclass
class Spot:
    name: str
    light_val: float
    crowd_val: float
    threat_val: float
    subject_val: float
    distance_val: float


def build_frame_for_step(
        spot: Spot,
        energy_val: float,
        anxiety_val: float,
        overload_val: float,
        hunger_val: float,
) -> Frame:
    return (
        Frame()
        .see(light, spot.light_val)
        .see(crowd, spot.crowd_val)
        .see(threat, spot.threat_val)
        .see(subject_interest, spot.subject_val)
        .see(distance, spot.distance_val)
        .see(energy, energy_val)
        .see(anxiety, anxiety_val)
        .see(overload, overload_val)
        .see(creative_hunger, hunger_val)
    )


def clamp01(x: float) -> float:
    return max(0.0, min(10.0, x))


class StreetRegulator(BaseRegulator):
    """
    Higher-scale agent watching telemetry and intervening.

    Uses:
      - strain = 0.6 * anxiety + 0.4 * overload
      - energy
    """

    def decide(self, telemetry: Frame) -> Intervention:
        e = telemetry.view(energy, 5.0)
        a = telemetry.view(anxiety, 0.0)
        o = telemetry.view(overload, 0.0)

        strain = 0.6 * a + 0.4 * o

        # Hard stop: very strained or almost no energy.
        if strain > 8.0 or e < 2.0:
            return Intervention.ASK_HUMAN  # "go home / talk to human"

        # Soften: getting strained or tired.
        if strain > 6.0 or e < 3.0:
            return Intervention.SHRINK_FRAME

        return Intervention.CONTINUE


def simulate_walk() -> None:
    # A simple path: quiet side street -> busy corner -> alley -> plaza -> bus stop -> golden light
    walk: List[Spot] = [
        Spot("quiet side street", light_val=5.0, crowd_val=1.0, threat_val=1.0, subject_val=3.0, distance_val=3.0),
        Spot("small café corner", light_val=6.0, crowd_val=4.0, threat_val=2.0, subject_val=6.0, distance_val=4.0),
        Spot("sketchy alley", light_val=3.0, crowd_val=2.0, threat_val=7.0, subject_val=8.0, distance_val=7.0),
        Spot("busy crosswalk", light_val=8.0, crowd_val=8.0, threat_val=5.0, subject_val=9.0, distance_val=5.0),
        Spot("bus stop crowd", light_val=5.0, crowd_val=7.0, threat_val=4.0, subject_val=6.0, distance_val=4.0),
        Spot("golden light corner", light_val=9.0, crowd_val=3.0, threat_val=3.0, subject_val=9.0, distance_val=4.0),
    ]

    hunter = StreetHunter()
    safety = SafetyFirst()
    care = SelfCare()

    agent = Agent("street_me").with_sigils(hunter, safety, care)
    history = History(agent=agent)

    regulator = StreetRegulator(name="street_regulator")

    # Initial proprioception
    energy_val = 7.0
    anxiety_val = 3.0
    overload_val = 2.0
    hunger_val = 6.0

    options = [SHOOT, WALK_ON, CROSS_STREET]

    print("=== Long walk with regulator ===\n")
    print(f"initial weights: hunter={hunter.weight:.2f}, safety={safety.weight:.2f}, care={care.weight:.2f}\n")

    for i, spot in enumerate(walk, start=1):
        frame = build_frame_for_step(
            spot=spot,
            energy_val=energy_val,
            anxiety_val=anxiety_val,
            overload_val=overload_val,
            hunger_val=hunger_val,
        )

        choice, score = agent.choose(frame, options)
        history.record(frame, choice, score)

        print(
            f"step {i}: {spot.name:20s} "
            f"-> {choice.label:11s} score={score:5.2f} "
            f"E={energy_val:4.1f} A={anxiety_val:4.1f} "
            f"O={overload_val:4.1f} H={hunger_val:4.1f}  "
            f"[weights: H={hunter.weight:.2f} S={safety.weight:.2f} C={care.weight:.2f}]"
        )

        # crude proprioception dynamics for next step
        if choice.label == "shoot":
            hunger_val -= 3.0
            energy_val -= 1.0 + 0.1 * spot.crowd_val
            anxiety_val += 0.3 * spot.threat_val
            overload_val += 0.2 * spot.crowd_val + 0.2 * spot.threat_val
        elif choice.label == "cross_street":
            hunger_val += 1.0
            energy_val -= 0.5
            anxiety_val -= 0.8
            overload_val -= 0.7
        else:  # walk_on
            hunger_val += 0.3 * spot.subject_val
            energy_val -= 0.3
            anxiety_val -= 0.3
            overload_val -= 0.2

        energy_val = clamp01(energy_val)
        anxiety_val = clamp01(anxiety_val)
        overload_val = clamp01(overload_val)
        hunger_val = clamp01(hunger_val)

        # --- Regulator step: look at telemetry and maybe intervene ---
        telemetry = Frame().see(energy, energy_val).see(anxiety, anxiety_val).see(overload, overload_val)
        intervention = regulator.decide(telemetry)

        if intervention == Intervention.SHRINK_FRAME:
            # turn down hunter a bit, turn up self-care
            hunter.weight = max(0.0, hunter.weight - 0.5)
            care.weight += 0.5
            print(f"  regulator: SHRINK_FRAME -> hunter={hunter.weight:.2f}, care={care.weight:.2f}")
        elif intervention in (Intervention.ASK_HUMAN, Intervention.PAUSE, Intervention.RESET_SIGILS):
            print(f"  regulator: {intervention.name} -> stopping walk")
            break
        # CONTINUE: do nothing

    print("\nFinal telemetry:")
    print(
        f"  energy={energy_val:.1f} anxiety={anxiety_val:.1f} "
        f"overload={overload_val:.1f} hunger={hunger_val:.1f}"
    )

    print("\nNarrative (choices):", [c.choice.label for c in history.collapses])


if __name__ == "__main__":
    simulate_walk()
