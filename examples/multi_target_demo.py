import numpy as np
import matplotlib.pyplot as plt

from simulator.pipeline.simulation_runner import SimulationRunner, RadarConfig
from simulator.pipeline.signal_generator import Target

from radar_dsp_library.rdm.rdm_visualization import RDMVisualizer

def main():
    cfg = RadarConfig(
        fc=77e9,
        bandwidth=1e9,
        chirp_duration=60e-6,
        num_chirps=128,
        num_samples=256,
        sampling_rate=5e6,
        snr_db=18
    )

    # Multiple targets
    targets = [
        Target(range_m=30.0, velocity_mps=5.0, rcs=1.0),
        Target(range_m=45.0, velocity_mps=-6.0, rcs=0.8),
        Target(range_m=60.0, velocity_mps=2.5, rcs=0.6),
    ]

    runner = SimulationRunner(cfg, targets)

    rdm, range_axis, velocity_axis = runner.run()

    print("Targets:")
    for t in targets:
        print(f"Range={t.r0} m, Velocity={t.v} m/s")

    # plot_rdm(rdm, range_axis, velocity_axis, title="Multi Target RDM")
    viz = RDMVisualizer(log_scale=True)

    viz.plot(rdm, range_axis, velocity_axis)
    viz.plot_range_profile(rdm, range_axis)
    viz.plot_doppler_profile(rdm, velocity_axis)

if __name__ == "__main__":
    main()
