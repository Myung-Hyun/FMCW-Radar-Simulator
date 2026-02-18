
import numpy as np
import matplotlib.pyplot as plt

from pipeline.simulation_runner import SimulationRunner, RadarConfig
from pipeline.signal_generator import Target

from dsp.rdm.rdm_visualization import RDMVisualizer

def main():
    # Radar specification
    cfg = RadarConfig(
        fc=77e9,
        bandwidth=1e9,
        chirp_duration=60e-6,
        num_chirps=128,
        num_samples=256,
        sampling_rate=5e6,
        snr_db=25
    )

    # Single target
    targets = [
        Target(
            range_m=40.0,
            velocity_mps=8.0,
            rcs=1.0
        )
    ]

    runner = SimulationRunner(cfg, targets)

    rdm, range_axis, velocity_axis = runner.run()

    print("Expected range:", targets[0].r0, "m")
    print("Expected velocity:", targets[0].v, "m/s")

    # plot_rdm(rdm, range_axis, velocity_axis)
    viz = RDMVisualizer(log_scale=True)

    viz.plot(rdm, range_axis, velocity_axis)
    viz.plot_range_profile(rdm, range_axis)
    viz.plot_doppler_profile(rdm, velocity_axis)


if __name__ == "__main__":
    main()