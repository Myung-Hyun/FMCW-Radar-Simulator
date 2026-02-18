import numpy as np


class Target:
    """
    Point target in radar scene.

    Parameters
    ----------
    range_m : float
        Initial range [m]
    velocity_mps : float
        Radial velocity [m/s]
    rcs : float
        Radar cross section scale
    phase : float
        Initial phase [rad]
    """

    def __init__(self, range_m, velocity_mps, rcs=1.0, phase=0.0):
        self.range = float(range_m)
        self.velocity = float(velocity_mps)
        self.rcs = float(rcs)
        self.phase = float(phase)

    def propagate(self, dt):
        """
        Update target state after dt seconds.
        Constant velocity model.
        """
        self.range += self.velocity * dt

    def get_state(self):
        """
        Return physical state used by signal generator.
        """
        return {
            "range": self.range,
            "velocity": self.velocity,
            "rcs": self.rcs,
            "phase": self.phase,
        }
