from dataclasses import dataclass
from typing import List


@dataclass
class Target:
    """
    Single radar target definition.
    """

    range_m: float
    velocity_mps: float
    angle_rad: float
    rcs: float = 1.0


@dataclass
class TargetScenario:
    """
    Collection of targets for simulation.
    """

    targets: List[Target]
