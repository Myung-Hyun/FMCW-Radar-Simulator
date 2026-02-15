import numpy as np

from radar_dsp_library.core.window import hann_window
from radar_dsp_library.range.range_fft import range_fft
from radar_dsp_library.doppler.doppler_fft import doppler_fft
from radar_dsp_library.doppler.velocity_axis import VelocityAxis
from radar_dsp_library.range.range_axis import RangeAxis


class RDMPipeline:
    """
    Beat signal -> Range-Doppler Map

    Input
    -----
    beat_matrix : ndarray [Nc, Ns]

    Output
    ------
    rdm : ndarray [Nc, Ns] (magnitude)
    range_axis : ndarray [Ns]
    velocity_axis : ndarray [Nc]
    """

    def __init__(self, fc, bandwidth, chirp_duration, num_chirps, num_samples, fs):
        self.fc = fc
        self.B = bandwidth
        self.Tc = chirp_duration
        self.Nc = num_chirps
        self.Ns = num_samples
        self.fs = fs

        # Axes helpers
        self.range_axis_gen = RangeAxis(
            fc=self.fc,
            bandwidth=self.B,
            chirp_duration=self.Tc,
            num_samples=self.Ns,
            sampling_rate=self.fs
        )
        self.vel_axis_gen = VelocityAxis(
            fc=self.fc,
            chirp_interval=self.Tc,
            n_fft=self.Nc
        )

    def run(self, beat_matrix):
        """
        Full RDM processing.
        """
        assert beat_matrix.shape == (self.Nc, self.Ns)

        # Windowing
        win_r = hann_window(self.Ns)
        win_d = hann_window(self.Nc)

        x = beat_matrix * win_r[None, :]
        x = x * win_d[:, None]

        # Range FFT (along fast-time axis)
        rng_fft = range_fft(x, axis=1, shift=False)

        # Doppler FFT (along slow-time axis)
        rdm_c = doppler_fft(rng_fft, axis=0, shift=True)

        rdm = np.abs(rdm_c)

        range_axis = self.range_axis_gen.generate(shift=False)
        velocity_axis = self.vel_axis_gen.generate(shift=True)

        return rdm, range_axis, velocity_axis
