def validate_radar_config(cfg):
    """
    Validate physical consistency of radar parameters.
    """

    assert cfg.bandwidth > 0
    assert cfg.chirp_duration > 0
    assert cfg.num_samples > 0
    assert cfg.num_chirps > 0
    assert cfg.sampling_rate > 0

    if cfg.sampling_rate * cfg.chirp_duration < cfg.num_samples:
        raise ValueError(
            "Sampling rate too low for number of samples."
        )
