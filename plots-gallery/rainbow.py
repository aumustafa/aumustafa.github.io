import numpy as np
import pub_style

# Newer wheel, in front of the seed beam
# Formatted as Nd wheel angle: integration time
files = {
    271: 3, 281: 4, 291: 6, 301: 8, 311: 12, 321: 16, 331: 20, 341: 25,
    351: 35, 1: 45, 11: 60, 21: 80, 31: 100, 41: 130, 51: 180, 61: 220,
    71: 260, 81: 350, 91: 450, 101: 600, 111: 800, 121: 1000, 131: 2000,
    141: 2000, 151: 2000, 161: 2000, 166: 2000,
}

folder = '/Users/abdullah/Documents/ACMELab/August 11/New ND4wheel'


# Load all spectra for a files={angle: exposure_ms} dict.
# All the data was taken with the same spectrometer so we'll load the wavelengths
# from the first file.
# And we'll construct intenstiy_matrix to have the shape (n_wavelengths, n_files).

angle_keys = list(files.keys())
first_angle, first_time = angle_keys[0], files[angle_keys[0]]
wavelengths = np.loadtxt(f'{folder}/{first_angle}deg_{first_time}ms.csv', delimiter=',', skiprows=1)[:, 0]

n_points = len(wavelengths)
n_files = len(files)
intensity_matrix = np.empty((n_points, n_files))

for i, (angle, time) in enumerate(files.items()):
    f = np.loadtxt(f'{folder}/{angle}deg_{time}ms.csv', delimiter=',', skiprows=1)
    assert np.array_equal(f[:, 0], wavelengths), f"Wavelength mismatch at {angle}deg_{time}ms"
    counts = f[:, 2]
    dark = f[:, 1]
    intensity_matrix[:, i] = (counts - dark) / time


pub_style.use(serif=True, custom_preamble=r'\usepackage{fouriernc}', colours='rainbow_PuRd_r', N=len(files))
fig, ax = pub_style.new_figure(despine=True, minor_ticks=True)

for i, angle in enumerate(files.keys()):
    ax.semilogy(wavelengths, intensity_matrix[:, i], label=f'{angle}')

ax.set_xlim(400, 1000)
ax.set_ylim(1e-2, 2e4)
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Intensity')
ax.set_title('Nd Wheel Calibration')

fig.savefig('plots-gallery/rainbow')
# pub_style.show()