import numpy as np
import pub_style, tol_colors
from scipy.special import eval_genlaguerre, sph_harm
from math import factorial

def ψ(n, l, m, r, theta, phi, a0=1.0):
    rho = 2 * r / (n * a0)
    norm_radial = np.sqrt((2 / (n * a0))**3 * factorial(n - l - 1) / (2 * n * factorial(n + l)))
    laguerre = eval_genlaguerre(n - l - 1, 2 * l + 1, rho)
    R_nl = norm_radial * np.exp(-rho / 2) * (rho**l) * laguerre
    Y_lm = sph_harm(m, l, phi, theta)
    return R_nl * Y_lm

# Slice in the X-Z vertical plane (Y = 0)
X = np.linspace(-30, 30, 400)
Z = np.linspace(-30, 30, 400)
XX, ZZ = np.meshgrid(X, Z)

R = np.sqrt(XX**2 + ZZ**2)
THETA = np.arctan2(np.sqrt(XX**2), ZZ)  # Polar angle theta from Z-axis
PHI = np.where(XX >= 0, 0, np.pi)       # Azimuthal angle phi

quantum_numbers = [(3, 1, 0), (3, 2, 0), (4, 3, 0), (4, 3, 1)]

pub_style.use(serif=True)
fig, axes = pub_style.new_figure(2, 2, ratio=1, width_mm=100, minor_ticks=True, despine=False, sharex=True, sharey=True)

for (n, l, m), ax in zip(quantum_numbers, axes.flat):
    density = np.abs(ψ(n, l, m, R, THETA, PHI))**2
    ax.pcolormesh(XX, ZZ, density, shading='auto', rasterized=True, cmap=tol_colors.rainbow)

pub_style.label_panels(axes)
pub_style.show()