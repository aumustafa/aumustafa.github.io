import numpy as np
import pub_style, tol_colors # Going to be a little more bespoke and import tol_colours as well
from scipy.special import eval_genlaguerre, sph_harm
from math import factorial

# Derivation is not too hard! Try it out yourself ;-> 
def ψ(n, l, m, r, theta, phi):
    a0 = 1 # Everything in Bohr, convert to SI if you would like
    rho = 2 * r / (n * a0)
    norm_radial = np.sqrt((2 / (n * a0))**3 * factorial(n - l - 1) / (2 * n * factorial(n + l)))
    laguerre = eval_genlaguerre(n - l - 1, 2 * l + 1, rho)
    R_nl = norm_radial * np.exp(-rho / 2) * (rho**l) * laguerre
    Y_lm = sph_harm(m, l, phi, theta)
    return R_nl * Y_lm

# We're gonna slice in the X-Z vertical plane (Y = 0)
x_coords = np.linspace(-30, 30, 400)
z_coords = np.linspace(-30, 30, 400)
X, Z = np.meshgrid(x_coords, z_coords)

# R = radial, Θ = polar, Φ = azimutal
R = np.sqrt(X**2 + Z**2)
Θ = np.arctan2(np.sqrt(X**2), Z)
Φ = np.where(X >= 0, 0, np.pi)

quantum_numbers = [(3, 1, 0), (3, 2, 0), (4, 3, 0), (4, 3, 1)]

pub_style.use(serif=True)
fig, axes = pub_style.new_figure(2, 2, ratio=0.9, width_mm=100, minor_ticks=True, despine=False, sharex=True, sharey=True)

for (n, l, m), ax in zip(quantum_numbers, axes.flat):
    density = np.abs(ψ(n, l, m, R, Θ, Φ))**2
    ax.set_title(fr'$\psi_{{{n}{l}{m}}} = R_{{{n}{l}}}Y_{{{l}{m}}}$')
    ax.pcolormesh(X, Z, density, shading='auto', rasterized=True, cmap=tol_colors.rainbow)
# This is a great example where pub_style forwards kwargs to matplotlib
# The rasterized=True makes the output file sizes nice and small, which speeds up the code A LOT


axes.flat[0].set_ylabel(r'$z$ ($a_0$)')
axes.flat[2].set_ylabel(r'$z$ ($a_0$)')
axes.flat[2].set_xlabel(r'$x$ ($a_0$)')
axes.flat[3].set_xlabel(r'$x$ ($a_0$)')
pub_style.label_panels(axes) # Adds in the (a), (b), (c), and (d)
# fig.savefig('plots-gallery/wavefuncs') # Default save as PDF
pub_style.show() # Equivalent to plt.show()