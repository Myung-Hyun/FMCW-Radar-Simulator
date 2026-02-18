import numpy as np


class RadarChannel:
    """
    Propagation channel model.

    Applies for each target:
        - time delay
        - Doppler shift
        - attenuation

    Multi-target signals are summed.
    """

    C = 299792458.0

    def __init__(self, sample_rate, carrier_freq):
        self.fs = sample_rate
        self.fc = carrier_freq
        self.lambda_ = self.C / self.fc

    def propagate(self, tx_signal, target_states):
        """
        Apply channel effects for multiple targets.

        Parameters
        ----------
        tx_signal : complex ndarray
        target_states : list of dict
            {range, velocity, rcs}

        Returns
        -------
        complex ndarray
            Summed received signal
        """

        rx_total = np.zeros_like(tx_signal, dtype=np.complex128)

        for state in target_states:
            R = state["range"]
            v = state["velocity"]
            rcs = state["rcs"]

            delay = 2 * R / self.C
            doppler = 2 * v / self.lambda_
            amplitude = rcs

            rx_total += self._apply_single(
                tx_signal,
                delay,
                doppler,
                amplitude
            )

        return rx_total

    def _apply_single(self, tx_signal, delay, doppler_freq, amplitude):
        """
        Single target channel response.
        (기존 apply 내용 그대로)
        """

        num_samples = len(tx_signal)
        t = np.arange(num_samples) / self.fs

        delay_samples = int(delay * self.fs)
        delayed = np.roll(tx_signal, delay_samples)

        doppler_phase = np.exp(1j * 2 * np.pi * doppler_freq * t)

        rx_signal = amplitude * delayed * doppler_phase
        return rx_signal
