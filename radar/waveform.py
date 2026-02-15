import numpy as np


class FMCWWaveform:
    """
    FMCW Radar Transmit Waveform Generator

    This class generates a complex exponential FMCW chirp signal.

    Signal model (RF model):
        s(t) = exp(j * 2π * (f_c * t + 0.5 * S * t^2))

    where:
        f_c : carrier frequency
        S   : chirp slope = B / T_chirp
    """

    def __init__(self, fc, bandwidth, chirp_duration, sample_rate):
        self.fc = fc
        self.bandwidth = bandwidth
        self.T = chirp_duration
        self.fs = sample_rate

        self.slope = bandwidth / chirp_duration
        self.num_samples = int(self.T * self.fs)

    def time_axis(self):
        """Generate time axis for one chirp."""
        return np.arange(self.num_samples) / self.fs

    def generate(self):
        """Generate complex FMCW transmit signal."""
        t = self.time_axis()

        phase = 2 * np.pi * (
            self.fc * t + 0.5 * self.slope * t**2
        )

        tx_signal = np.exp(1j * phase)
        return tx_signal
