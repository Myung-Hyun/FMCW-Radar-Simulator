import numpy as np


class RadarChannel:
    """
    Propagation channel model.

    Applies:
        - time delay
        - Doppler shift
        - attenuation
    """

    def __init__(self, sample_rate):
        self.fs = sample_rate

    def apply(self, tx_signal, delay, doppler_freq, amplitude):
        """
        Apply channel effects to transmitted signal.

        Parameters
        ----------
        tx_signal : complex ndarray
        delay : seconds
        doppler_freq : Hz
        amplitude : scaling factor
        """

        num_samples = len(tx_signal)
        t = np.arange(num_samples) / self.fs

        # Delay → sample shift
        delay_samples = int(delay * self.fs)
        delayed = np.roll(tx_signal, delay_samples)

        # Doppler → phase rotation
        doppler_phase = np.exp(1j * 2 * np.pi * doppler_freq * t)

        rx_signal = amplitude * delayed * doppler_phase
        return rx_signal
