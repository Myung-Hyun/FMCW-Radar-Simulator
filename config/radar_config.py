from dataclasses import dataclass, field


@dataclass
class RadarConfig:
    """
    FMCW radar specification-driven configuration.

    This class defines physical radar parameters and
    automatically derives secondary parameters used
    throughout simulation and DSP pipeline.
    """

    # === Primary physical specs ===
    fc: float = 77e9                # Carrier frequency [Hz]
    bandwidth: float = 1e9          # Chirp bandwidth [Hz]
    chirp_duration: float = 60e-6   # Chirp duration [s]

    num_chirps: int = 128           # Chirps per frame
    num_samples: int = 256          # ADC samples per chirp
    sampling_rate: float = 5e6      # ADC sampling rate [Hz]

    snr_db: float | None = 20.0     # AWGN SNR

    # === Derived parameters (auto computed) ===
    slope: float = field(init=False)
    wavelength: float = field(init=False)
    range_resolution: float = field(init=False)
    max_range: float = field(init=False)
    velocity_resolution: float = field(init=False)

    SPEED_OF_LIGHT = 3e8

    def __post_init__(self):
        self._compute_derived()

    def _compute_derived(self):
        """
        Compute derived radar physics parameters.
        """

        self.slope = self.bandwidth / self.chirp_duration

        self.wavelength = self.SPEED_OF_LIGHT / self.fc

        self.range_resolution = (
            self.SPEED_OF_LIGHT / (2 * self.bandwidth)
        )

        self.max_range = (
            self.SPEED_OF_LIGHT * self.sampling_rate
        ) / (2 * self.slope)

        self.velocity_resolution = (
            self.wavelength / (2 * self.num_chirps * self.chirp_duration)
        )
