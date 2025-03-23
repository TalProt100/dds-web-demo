import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page config (optional)
st.set_page_config(page_title="Tal and Yuval DDS Project", layout="wide")

st.title("Tal and Yuval DDS Project - for Prof. Yosef Pinhasi")

# Create two tabs in Streamlit
tab1, tab2 = st.tabs(["Accumulator DDS", "LUT-based DDS"])

# --------------------------------------------------------------------
# TAB 1: PHASE ACCUMULATOR DDS
# --------------------------------------------------------------------
with tab1:
    st.subheader("Phase Accumulator DDS")

    freq = st.slider("Frequency (Hz)", min_value=50, max_value=5000, value=1000, step=50, key="acc_freq")
    fs   = st.slider("Sample Rate (Hz)", min_value=8000, max_value=192000, value=48000, step=1000, key="acc_fs")
    n_samp = st.slider("Number of Samples", min_value=32, max_value=1024, value=128, step=32, key="acc_nsamp")

    # DDS definitions
    ACCUM_BITS = 32
    ACCUM_MAX  = 2 ** ACCUM_BITS
    phase_increment = int(freq * (ACCUM_MAX / fs))

    accumulator = 0
    sine_values = []

    for _ in range(n_samp):
        phase = (accumulator / ACCUM_MAX) * 2.0 * np.pi
        sine_values.append(np.sin(phase))
        accumulator = (accumulator + phase_increment) % ACCUM_MAX

    # Final accumulator in binary
    final_accum_bin = format(accumulator, '032b')
    last_phase = (accumulator / ACCUM_MAX) * 2.0 * np.pi

    # Create the figure with 2 subplots: (1) circle, (2) waveform
    fig1, (ax_circle, ax_wave) = plt.subplots(1, 2, figsize=(8, 4))

    # --- Left subplot: Unit circle ---
    circle = plt.Circle((0, 0), 1.0, fill=False, color='blue')
    ax_circle.add_artist(circle)
    ax_circle.axhline(0, color='gray', linewidth=0.5)
    ax_circle.axvline(0, color='gray', linewidth=0.5)
    ax_circle.set_aspect('equal', 'box')
    ax_circle.set_xlim([-1.2, 1.2])
    ax_circle.set_ylim([-1.2, 1.2])
    # Draw a red line showing the final phase angle
    x_end = np.cos(last_phase)
    y_end = np.sin(last_phase)
    ax_circle.plot([0, x_end], [0, y_end], color='red')
    ax_circle.set_title(f"Final Phase: {last_phase:.3f} rad")

    # --- Right subplot: Time-domain waveform ---
    ax_wave.plot(sine_values, color='orange')
    ax_wave.set_title("DDS Output Waveform")
    ax_wave.set_xlabel("Sample")
    ax_wave.set_ylabel("Amplitude")
    ax_wave.grid(True, linestyle='--', alpha=0.5)

    fig1.tight_layout()
    st.pyplot(fig1)

    # Show the accumulator in binary
    st.write(f"Accumulator = `{final_accum_bin}`")

# --------------------------------------------------------------------
# TAB 2: LUT-BASED DDS
# --------------------------------------------------------------------
with tab2:
    st.subheader("LUT-based DDS")

    table_entries = st.slider("Number of LUT Entries", min_value=4, max_value=64, value=19, step=1, key="lut_entries")

    # Generate wave
    N = 128
    phase = np.linspace(0, 2 * np.pi, N, endpoint=False)
    ideal_wave = np.sin(phase)

    lut_phase = np.linspace(0, 2 * np.pi, table_entries, endpoint=False)
    lut = np.sin(lut_phase)
    lut_indices = np.floor((phase / (2 * np.pi)) * table_entries).astype(int)
    quantized_wave = lut[lut_indices]

    # FFT (log magnitude)
    fft_vals = np.fft.fft(quantized_wave)
    fft_mag = np.abs(fft_vals)
    log_fft_mag = np.log10(fft_mag + 1e-6)

    # Create figure with 2 subplots: (1) wave, (2) log-FFT
    fig2, (ax_wave2, ax_fft) = plt.subplots(2, 1, figsize=(6, 6))

    ax_wave2.plot(phase, quantized_wave, label="Quantized", drawstyle='steps-post')
    ax_wave2.plot(phase, ideal_wave, label="Ideal", linestyle='--', alpha=0.7)
    ax_wave2.set_title(f"LUT Quantized Waveform (Entries = {table_entries})")
    ax_wave2.set_xlabel("Phase [rad]")
    ax_wave2.set_ylabel("Amplitude")
    ax_wave2.legend()
    ax_wave2.grid(True)

    ax_fft.plot(log_fft_mag[:N//2], color='blue')
    ax_fft.set_title("Spectral Content (log10 of FFT magnitude)")
    ax_fft.set_xlabel("Frequency Bin")
    ax_fft.set_ylabel("log10(mag)")
    ax_fft.grid(True)

    fig2.tight_layout()
    st.pyplot(fig2)
