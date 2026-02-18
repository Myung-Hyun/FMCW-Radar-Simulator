from dataclasses import dataclass
from typing import List

# from .signal_generator import SignalGenerator, Target
from radar.radar_sensor import RadarSensor
from radar.waveform import FMCWWaveform
from radar.channel import RadarChannel
from radar.mixer import Mixer
from radar.adc import ADC


from .rdm_pipeline import RDMPipeline

from config.radar_config import RadarConfig
from config.target_config import Target, TargetScenario
from config.simulation_config import SimulationConfig



class SimulationRunner:
    """
    Orchestrates:
        Targets -> Beat Signal -> RDM
    """

    def __init__(self, cfg: RadarConfig, targets: List[Target]):
        self.cfg = cfg
        self.targets = targets

        # self.generator = SignalGenerator(
        #     fc=cfg.fc,
        #     bandwidth=cfg.bandwidth,
        #     chirp_duration=cfg.chirp_duration,
        #     num_chirps=cfg.num_chirps,
        #     num_samples=cfg.num_samples,
        #     fs=cfg.sampling_rate,
        #     targets=targets,
        #     snr_db=cfg.snr_db
        # )

        # 2. Radar 구성
        waveform = FMCWWaveform(...)
        channel = RadarChannel(...)
        mixer = Mixer(...)
        adc = ADC(...)

        sensor = RadarSensor(waveform, channel, mixer, adc)
        noise = AWGN(snr_db=20)


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
