from dataclasses import dataclass
from .radar_config import RadarConfig
from .target_config import TargetScenario


@dataclass
class SimulationConfig:
    """
    Top-level simulation configuration.
    """

    radar: RadarConfig
    scenario: TargetScenario

    frame_time: float = 0.05
    enable_noise: bool = True
    enable_clutter: bool = False
