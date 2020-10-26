# File: noise_bandpass.py
# Aim: A demo of noise bandpass

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
noise = np.random.randn(length)
white_fig = plot_signal(noise)
white_fig.savefig('WhiteNoise.png')

# %%
band = [e * 2 / sample_rate for e in [5, 15]]
b, a = signal_tool.butter(8, band, 'bandpass')
bandpass = signal_tool.filtfilt(b, a, noise)
band_fig = plot_signal(bandpass)
band_fig.savefig('BanPassNoise.png')

# %%
