# File: noise_demo.py
# Aim: A demo of noise generation

# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as signal_tool


# %% ----------------------------------------------------
# Settings
tmin, tmax = 0, 1  # Seconds
sample_rate = 200  # Hz

# Noise parameters
parameter = dict(
    freq=10,  # Center frequency of noise band in Hz
    bandwidth=5,  # Width of noise band in Hz
    energy=1,  # Strongess of the noise signal, V^2
)

# Set style of plotting
plt.style.use('ggplot')

# %% ----------------------------------------------------
# Generate variables
# Signal length
length = sample_rate * (tmax - tmin)

# Noise Width,
# use 'block' window
width = int(1 / parameter['bandwidth'] * sample_rate)

# T axis
T = np.linspace(tmin, tmax, length, endpoint=False)

# Constant PI
PI = np.pi


def plot_signal(signal):
    # Plot signal
    # Wavelet decomposition
    cmin, cmax = 5, length
    cwtmatr = signal_tool.cwt(signal, signal_tool.ricker, range(cmin, cmax))

    # FFT decomposition
    fft = np.fft.fft(signal)

    # Prepare fig
    fig, axes = plt.subplots(3, 1, figsize=(8, 8), dpi=200)

    # Draw time series
    axes[0].plot(T, signal)
    axes[0].set_title('Time Series')

    # Draw wavelets
    axes[1].imshow(cwtmatr, extent=[tmin, tmax, cmin, cmax], cmap='PRGn', aspect='auto',
                   vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    axes[1].set_title('Wavelet Spectrum (ricker)')

    # Draw FFT
    f = sample_rate * T / max(T)
    axes[2].plot(f, fft.real, marker='.', label='Real', alpha=0.5)
    axes[2].plot(f, fft.imag, marker='.', label='Imag', alpha=0.5)
    axes[2].legend()
    axes[2].set_title('FFT Spectrum')

    fig.tight_layout()
    return fig


# %% ----------------------------------------------------
# Generate bandpass random time series
# Random phase
phase = parameter['freq'] * 2 * PI * T
phase_noise = phase + np.random.random(length)

# Random amplitude
noise = np.random.random(length) * 0.1
center = np.random.randint(length-width)
noise[center:center+width] = 1

# Constant amplitude
amplitude = parameter['energy'] * np.ones(length)

# Generate signal
signal_noise = noise * amplitude * np.sin(phase_noise)

noise_fig = plot_signal(signal_noise)
noise_fig.savefig('noise.png')

# %%
