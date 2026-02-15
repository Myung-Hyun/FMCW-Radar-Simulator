import numpy as np


class Target:
    """
    Simple point target model.

    Parameters
    ----------
    range_m : float
        Initial range [m]
    velocity_mps : float
        Radial velocity [m/s] (+ away, - approaching)
    rcs : float
        Reflectivity scale
    """

    def __init__(self, range_m, velocity_mps, rcs=1.0):
        self.r0 = range_m
        self.v = velocity_mps
        self.rcs = rcs


class SignalGenerator:
    """
    FMCW beat signal generator in complex baseband domain.

    Physical model:
        - Linear FMCW chirp
        - Time delay tau = 2R/c
        - Doppler shift from radial velocity
        - Beat frequency ~ slope * tau + Doppler term
    """

    C = 299792458.0  # speed of light [m/s]

    def __init__(self, fc, bandwidth, chirp_duration, num_chirps, num_samples, fs, targets, snr_db=None):
        self.fc = fc
        self.B = bandwidth
        self.Tc = chirp_duration
        self.Nc = num_chirps
        self.Ns = num_samples
        self.fs = fs
        self.targets = targets
        self.snr_db = snr_db

        self.lambda_ = self.C / self.fc
        self.slope = self.B / self.Tc  # Hz/s

        # fast-time axis within one chirp
        self.t_fast = np.arange(self.Ns) / self.fs
        # slow-time axis across chirps
        self.t_slow = np.arange(self.Nc) * self.Tc

    def generate(self):
        """
        Generate beat signal matrix [Nc, Ns] (complex64).
        """
        beat = np.zeros((self.Nc, self.Ns), dtype=np.complex128)

        for tgt in self.targets:
            beat += self._target_beat(tgt)

        if self.snr_db is not None:
            beat = self._add_awgn(beat, self.snr_db)

        return beat.astype(np.complex64)

    def _target_beat(self, tgt: Target):
        """
        Beat signal for one target.

        R(t) = R0 + v * t_slow
        tau(t) = 2R(t)/c
        f_b(t) ≈ slope * tau(t)  (range term)
        f_d = 2v/lambda         (doppler term)
        """
        # Range per chirp (slow-time)
        R = tgt.r0 + tgt.v * self.t_slow[:, None]  # [Nc, 1]
        tau = 2.0 * R / self.C                     # [Nc, 1]

        # Beat frequency components
        f_range = self.slope * tau                 # [Nc, 1]
        f_doppler = (2.0 * tgt.v / self.lambda_)   # scalar

        # Phase accumulation
        # fast-time phase from beat freq + slow-time doppler progression
        phase_fast = 2.0 * np.pi * f_range * self.t_fast[None, :]  # [Nc, Ns]
        phase_dopp = 2.0 * np.pi * f_doppler * self.t_slow[:, None]  # [Nc, 1]

        sig = tgt.rcs * np.exp(1j * (phase_fast + phase_dopp))
        return sig

    @staticmethod
    def _add_awgn(x, snr_db):
        """
        Add complex AWGN to achieve target SNR (per sample).
        """
        power = np.mean(np.abs(x) ** 2)
        snr_lin = 10 ** (snr_db / 10.0)
        noise_power = power / snr_lin
        noise = (np.random.randn(*x.shape) + 1j * np.random.randn(*x.shape)) * np.sqrt(noise_power / 2.0)
        return x + noise
