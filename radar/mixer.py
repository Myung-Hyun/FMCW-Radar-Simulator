import numpy as np


class Mixer:
    """
    FMCW Dechirp Mixer

    Baseband generation by mixing:
        beat(t) = tx(t) * conj(rx(t))
    """

    @staticmethod
    def mix(tx_signal, rx_signal):
        """
        Perform dechirping (homodyne mixing).
        """
        return tx_signal * np.conj(rx_signal)
