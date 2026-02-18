import numpy as np


class RadarSensor:
    """
    FMCW Radar sensor model.

    Orchestrates signal chain:
        TX waveform → propagation → mixer → ADC

    Each component must implement:
        waveform.generate() -> tx_signal
        channel.propagate(tx_signal, target_states) -> rx_signal
        mixer.mix(tx_signal, rx_signal) -> beat_signal
        adc.sample(analog_signal) -> digital_samples
    """

    def __init__(self, waveform, channel, mixer, adc):
        self.waveform = waveform
        self.channel = channel
        self.mixer = mixer
        self.adc = adc

    def capture(self, target_states):
        """
        Perform one radar measurement frame.

        Parameters
        ----------
        target_states : list[dict]
            Each dict must contain:
                range : float
                velocity : float
                rcs : float

        Returns
        -------
        np.ndarray
            Complex baseband samples [Nc, Ns]
        """

        # 1) Transmit waveform
        tx_signal = self.waveform.generate()

        # 2) Propagation & reflection
        rx_signal = self.channel.propagate(tx_signal, target_states)

        # 3) Beat signal generation
        beat_signal = self.mixer.mix(tx_signal, rx_signal)

        # 4) ADC sampling
        samples = self.adc.sample(beat_signal)

        return samples

    def __repr__(self):
        return (
            f"RadarSensor("
            f"waveform={self.waveform.__class__.__name__}, "
            f"channel={self.channel.__class__.__name__}, "
            f"mixer={self.mixer.__class__.__name__}, "
            f"adc={self.adc.__class__.__name__})"
        )
