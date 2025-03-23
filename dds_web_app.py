import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="DDS Table Entry Demo")

# Title and slider
st.title("🌀 Direct Digital Synthesizer (DDS) Demo")
table_entries = st.slider("Number of LUT Entries", min_value=4, max_value=64, value=19)

# DDS Processing
N = 128
phase = np.linspace(0, 2 * np.pi, N, endpoint=False)
ideal_wave = np.sin(phase)

lut_phase = np.linspace(0, 2 * np.pi, table_entries, endpoint=False)
lut = np.sin(lut_phase)
lut_indices = np.floor((phase / (2 * np.pi)) * table_entries).astype(int)
quantized_wave = lut[lut_indices]

# Error
error_signal = ideal_wave - quantized_wave
rmse = np.sqrt(np.mean(error_signal ** 2))

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
ax1.plot(phase, quantized_wave, label='Quantized', drawstyle='steps-post')
ax1.plot(phase, ideal_wave, label='Ideal', linestyle='--', alpha=0.7)
ax1.set_title("Quantized DDS Output vs Ideal Sine Wave")
ax1.set_ylabel("Amplitude")
ax1.set_xlabel("Phase (rad)")
ax1.legend()
ax1.grid(True)

ax2.plot(phase, error_signal, color='orange')
ax2.set_title(f"Error Signal (RMSE = {rmse:.5f})")
ax2.set_ylabel("Error")
ax2.set_xlabel("Phase (rad)")
ax2.grid(True)

st.pyplot(fig)
