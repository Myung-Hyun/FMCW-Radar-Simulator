import numpy as np


class BasebandCalibration:
    """
    Baseband Imperfection Model

    Models hardware non-idealities:
        - IQ imbalance
        - phase offset
        - gain mismatch
    """

    @staticmethod
    def iq_imbalance(iq, gain_mismatch=0.05, phase_error_deg=5):
        """
        Apply IQ imbalance.

        Parameters
        ----------
        gain_mismatch : relative gain difference
        phase_error_deg : phase error between I and Q
        """

        phase_error = np.deg2rad(phase_error_deg)

        I = np.real(iq)
        Q = np.imag(iq)

        I_new = (1 + gain_mismatch) * I
        Q_new = (1 - gain_mismatch) * (
            Q * np.cos(phase_error) +
            I * np.sin(phase_error)
        )

        return I_new + 1j * Q_new

    @staticmethod
    def dc_offset(iq, offset=0.01):
        """
        DC offset from LO leakage.
        """
        return iq + offset

    @staticmethod
    def phase_noise(iq, std=0.01):
        """
        Random phase jitter.
        """
        phase = np.random.randn(*iq.shape) * std
        return iq * np.exp(1j * phase)
