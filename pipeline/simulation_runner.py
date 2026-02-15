from dataclasses import dataclass
from typing import List

from .signal_generator import SignalGenerator, Target
from .rdm_pipeline import RDMPipeline


@dataclass
class RadarConfig:
    """
    Centralized radar configuration (spec-driven).
    """
    fc: float = 77e9
    bandwidth: float = 1e9
    chirp_duration: float = 60e-6
    num_chirps: int = 128
    num_samples: int = 256
    sampling_rate: float = 5e6
    snr_db: float | None = 20.0


class SimulationRunner:
    """
    Orchestrates:
        Targets -> Beat Signal -> RDM
    """

    def __init__(self, cfg: RadarConfig, targets: List[Target]):
        self.cfg = cfg
        self.targets = targets

        self.generator = SignalGenerator(
            fc=cfg.fc,
            bandwidth=cfg.bandwidth,
            chirp_duration=cfg.chirp_duration,
            num_chirps=cfg.num_chirps,
            num_samples=cfg.num_samples,
            fs=cfg.sampling_rate,
            targets=targets,
            snr_db=cfg.snr_db
        )

        self.rdm_pipeline = RDMPipeline(
            fc=cfg.fc,
            bandwidth=cfg.bandwidth,
            chirp_duration=cfg.chirp_duration,
            num_chirps=cfg.num_chirps,
            num_samples=cfg.num_samples,
            fs=cfg.sampling_rate
        )

    def run(self):
        """
        Returns
        -------
        rdm : ndarray
        range_axis : ndarray
        velocity_axis : ndarray
        """
        beat = self.generator.generate()
        rdm, r_axis, v_axis = self.rdm_pipeline.run(beat)
        return rdm, r_axis, v_axis
