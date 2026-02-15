import numpy as np

C = 3e8  # speed of light


class RadarTarget:
    """
    Point target model.

    Converts physical target parameters into signal effects:
        - time delay
        - Doppler shift
        - attenuation (RCS-based)
    """

    def __init__(self, range_m, velocity_mps, rcs=1.0):
        self.range = range_m
        self.velocity = velocity_mps
        self.rcs = rcs

    def round_trip_delay(self):
        """Signal propagation delay (two-way)."""
        return 2 * self.range / C

    def doppler_frequency(self, fc):
        """
        Doppler shift for FMCW radar.

        f_d = 2 * v * fc / c
        """
        return 2 * self.velocity * fc / C

    def attenuation(self):
        """
        Simple path loss model.

        amplitude ∝ sqrt(RCS) / R^2
        """
        return np.sqrt(self.rcs) / (self.range**2 + 1e-6)
