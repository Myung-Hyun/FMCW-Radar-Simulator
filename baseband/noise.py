import numpy as np


class BasebandNoise:
    """
    Baseband Noise Model

    Includes:
        - AWGN (thermal noise)
        - Clutter floor
    """

    def __init__(self, snr_db=None, noise_power=None):
        """
        Choose one:
            snr_db → relative noise
            noise_power → absolute noise
        """
        self.snr_db = snr_db
        self.noise_power = noise_power

    def awgn(self, signal):
        """
        Add complex AWGN.

        SNR 정의:
            SNR = signal_power / noise_power
        """
        sig_power = np.mean(np.abs(signal)**2)

        if self.noise_power is None:
            snr_linear = 10**(self.snr_db / 10)
            noise_power = sig_power / snr_linear
        else:
            noise_power = self.noise_power

        noise = (
            np.sqrt(noise_power/2) *
            (np.random.randn(*signal.shape) +
             1j*np.random.randn(*signal.shape))
        )

        return signal + noise

    def clutter_floor(self, signal, level_db=-40):
        """
        Add stationary clutter background.

        모델:
            constant amplitude complex background
        """
        sig_power = np.mean(np.abs(signal)**2)
        clutter_power = sig_power * 10**(level_db / 10)

        clutter = (
            np.sqrt(clutter_power/2) *
            (np.random.randn(*signal.shape) +
             1j*np.random.randn(*signal.shape))
        )

        return signal + clutter
