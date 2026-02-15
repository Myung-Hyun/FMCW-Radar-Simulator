# 📡 FMCW Radar Signal Processing Simulator (Baseband Domain)

## 1. Project Overview

This project implements a full FMCW radar signal processing pipeline in the complex baseband domain.

The goal is to:

- Understand the physical meaning of FMCW radar signals
- Simulate range and velocity estimation from first principles
- Connect RF physics → DSP → perception-level measurements
- Build an extensible research-grade simulation framework
- Provide reproducible experiments for radar algorithm development

This simulator focuses on **signal-level correctness**, not visualization.

---

## 2. System Model

We simulate a monostatic FMCW radar observing point targets.

### Transmit signal (chirp)

$$
s_{tx}(t) = \exp\left(j 2\pi \left(f_c t + \frac{S}{2} t^2 \right)\right)
$$

Where:

- $f_c$ : carrier frequency
- $S = \frac{B}{T_c}$ : chirp slope
- $B$ : bandwidth
- $T_c$ : chirp duration

---

### Received signal from target i

$$
s_{rx,i}(t) = A_i \exp\left(j 2\pi \left(f_c (t - \tau_i) + \frac{S}{2} (t - \tau_i)^2 \right)\right)
$$

Where:

- $\tau_i = \frac{2R_i}{c}$ : round-trip delay
- $R_i$ : target range
- $A_i$ : amplitude (includes RCS & path loss)

---

### Dechirped (mixed) baseband signal

After mixing TX and RX:

$$
s_{bb}(t) = \sum_i A_i \exp\left(j 2\pi (f_{b,i} t + f_{D,i} t)\right)
$$

Where:

- $f_{b,i} = \frac{2 S R_i}{c}$ : beat frequency (range information)
- $f_{D,i} = \frac{2 v_i}{\lambda}$ : Doppler frequency

---

## 3. Processing Pipeline

### Step 1 — ADC Sampling

- Sample dechirped signal
- Output complex IQ samples
- Domain: fast-time × slow-time

---

### Step 2 — Range FFT

Transforms beat frequency → range.

$$
R_k = FFT_{range}(s_{bb})
$$

Output:
- Range profile per chirp

---

### Step 3 — Doppler FFT

Transforms slow-time phase change → velocity.

$$
RDM = FFT_{doppler}(R_k)
$$

Output:
- Range-Doppler Map (RDM)

---

### Step 4 — Detection (CFAR placeholder)

Detect peaks from RDM.

Output:
- Target measurements

---

## 4. Simulation Assumptions

- Ideal linear chirp
- Point target model
- Far-field assumption
- No antenna pattern
- No mutual coupling
- Additive white Gaussian noise (AWGN)

Noise model:

$$
n \sim \mathcal{CN}(0, \sigma^2)
$$

---

## 5. Output Data

The simulator produces:

- Complex IQ samples
- Range profiles
- Range-Doppler Map
- Ground truth target parameters

All intermediate signals are saved for debugging.

---

## 6. Project Structure

```
radar_sim/
│
├── config/
│   └── radar_params.py
│
├── signal/
│   ├── chirp_generator.py
│   ├── target_model.py
│   └── channel_model.py
│
├── processing/
│   ├── range_fft.py
│   ├── doppler_fft.py
│   └── rdm.py
│
├── experiments/
│   └── single_target_demo.py
│
└── README.md
```

---

## 7. Example Experiment

Single target simulation:

- Range: 30 m
- Velocity: 5 m/s
- SNR: 20 dB

Expected outcome:

- Single peak in RDM
- Correct range bin
- Correct Doppler bin

---

## 8. Learning Goals

This project demonstrates:

- Physical origin of beat frequency
- Phase-based Doppler estimation
- Baseband signal representation
- Radar measurement formation

The simulator is designed for extension to:

- MIMO processing
- Angle estimation (DOA)
- Clutter modeling
- Tracking integration

---

## 9. Requirements

- Python 3.9+
- NumPy
- SciPy
- Matplotlib

---

## 10. License

MIT License
