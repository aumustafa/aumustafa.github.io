import pub_style
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
import tol_colors

pub_style.use()

df = sns.load_dataset("penguins").dropna()
x = df["body_mass_g"].values
y = df["bill_depth_mm"].values

fig, ax = pub_style.new_figure(ratio=1.0)

xmin, xmax = 2200, 6800
ymin, ymax = 10, 25
xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
kernel = gaussian_kde(np.vstack([x, y]))
zz = kernel(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape) * 10000

cmap = tol_colors.iridescent
cf = ax.contourf(xx, yy, zz, levels=100, cmap=cmap)
# cbar = fig.colorbar(cf)
# cbar.set_label('Density')
# cbar.ax.tick_params(which="both", direction="inout")

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel("Body mass (g)")
ax.set_ylabel("Bill depth (mm)")

fig.savefig("penguins_kde.svg")
# pub_style.show()