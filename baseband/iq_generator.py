import numpy as np


class IQGenerator:
    """
    Baseband IQ Signal Generator

    Converts real or complex analog signal into IQ representation.

    In FMCW radar after dechirp:
        beat(t) is already complex baseband.
    But this module keeps a clean interface for DSP input.

    역할:
        - I/Q separation
        - complex baseband normalization
    """

    @staticmethod
    def from_complex(signal):
        """
        Ensure signal is complex baseband format.

        Parameters
        ----------
        signal : ndarray
            complex input signal

        Returns
        -------
        iq : ndarray (complex)
        """
        return signal.astype(np.complex128)

    @staticmethod
    def from_real(signal):
        """
        Convert real-valued signal to complex IQ.

        Q = Hilbert transform approximation (simplified).
        """
        analytic = np.fft.ifft(
            np.fft.fft(signal) * 2
        )
        return analytic

    @staticmethod
    def normalize(iq):
        """
        Normalize signal power.
        """
        power = np.mean(np.abs(iq)**2) + 1e-12
        return iq / np.sqrt(power)
