import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use('dark_background')  # Dark theme for matplotlib

class DDSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DDS Table Entry Demo")
        self.root.configure(bg='#2b2b2b')  # Dark background

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TScale', background='#2b2b2b')

        self.table_entries = tk.IntVar(value=19)

        # Slider
        self.slider = ttk.Scale(root, from_=4, to=64, orient='horizontal',
                                variable=self.table_entries, command=self.update_plot)
        self.slider.pack(fill='x', padx=10, pady=5)

        self.label = ttk.Label(root, text=f"Table Entries: {self.table_entries.get()}")
        self.label.pack()

        # Matplotlib figure and canvas
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 5), facecolor='#2b2b2b')
        self.fig.subplots_adjust(hspace=0.4)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.update_plot()

    def update_plot(self, *args):
        entries = int(self.table_entries.get())
        self.label.config(text=f"Table Entries: {entries}")

        N = 128
        phase = np.linspace(0, 2 * np.pi, N, endpoint=False)
        ideal_wave = np.sin(phase)

        lut_phase = np.linspace(0, 2 * np.pi, entries, endpoint=False)
        lut = np.sin(lut_phase)

        lut_indices = np.floor((phase / (2 * np.pi)) * entries).astype(int)
        quantized_wave = lut[lut_indices]

        error_signal = ideal_wave - quantized_wave
        rmse = np.sqrt(np.mean(error_signal**2))

        # Update plots
        self.ax1.clear()
        self.ax1.plot(phase, quantized_wave, label='Quantized', drawstyle='steps-post')
        self.ax1.plot(phase, ideal_wave, label='Ideal', linestyle='--', alpha=0.6)
        self.ax1.set_title("DDS Output vs Ideal Sine", color='white')
        self.ax1.set_ylabel("Magnitude")
        self.ax1.set_xlabel("Phase [rad]")
        self.ax1.grid(True, linestyle='--', alpha=0.3)
        self.ax1.legend()

        self.ax2.clear()
        self.ax2.plot(phase, error_signal, color='orange')
        self.ax2.set_title(f"Error Signal (RMSE: {rmse:.5f})", color='white')
        self.ax2.set_ylabel("Error")
        self.ax2.set_xlabel("Phase [rad]")
        self.ax2.grid(True, linestyle='--', alpha=0.3)

        for ax in (self.ax1, self.ax2):
            ax.set_facecolor('#2b2b2b')
            ax.tick_params(colors='white')
            ax.yaxis.label.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.title.set_color('white')

        self.canvas.draw()

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DDSApp(root)
    root.mainloop()
