import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="DDS Table Entry Demo")

# UI
st.title("🌀 Direct Digital Synthesizer (DDS) Demo - Tal and Yuval")
table_entries = st.slider("Number of LUT Entries", min_value=4, max_value=64, value=19)

# DDS waveform generation
N = 128
phase = np.linspace(0, 2 * np.pi, N, endpoint=False)
ideal_wave = np.sin(phase)

lut_phase = np.linspace(0, 2 * np.pi, table_entries, endpoint=False)
lut = np.sin(lut_phase)
lut_indices = np.floor((phase / (2 * np.pi)) * table_entries).astype(int)
quantized_wave = lut[lut_indices]

# FFT and log mag
fft_vals = np.fft.fft(quantized_wave)
fft_mag = np.abs(fft_vals)
log_fft_mag = np.log10(fft_mag + 1e-6)  # avoid log(0)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Top plot: quantized waveform vs ideal
ax1.plot(phase, quantized_wave, label='Quantized', drawstyle='steps-post')
ax1.plot(phase, ideal_wave, label='Ideal', linestyle='--', alpha=0.7)
ax1.set_title("Quantized DDS Output vs Ideal Sine Wave")
ax1.set_ylabel("Amplitude")
ax1.set_xlabel("Phase (rad)")
ax1.legend()
ax1.grid(True)

# Bottom plot: log10(magnitude) of FFT
ax2.plot(log_fft_mag[:N//2], color='blue')
ax2.set_title("Spectral Content (log10 of FFT magnitude)")
ax2.set_ylabel("log10(mag)")
ax2.set_xlabel("Frequency Bin")
ax2.grid(True)

st.pyplot(fig)
