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
zz = kernel(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
zz /= np.max(zz)

# I'm choosing the discrete colourmaps just for fun, but the continuous ones work great as well
cmap = tol_colors.YlOrBr
# cmap = tol_colors.iridescent # I like this one a lot too
cf = ax.contourf(xx, yy, zz, levels=10, cmap=cmap)
pub_style.colourbar(cf, ax, label='Density')

# If you don't like the look of the pub_style.colourbar, you can try something like this.
# This does get you something that looks closer to the default spines, which I will admit
# does have it's own charm of being more homogenous looking.
# But I feel like colourbars look odd when the ticks portrude into the colours.
# cbar = fig.colorbar(cf)
# cbar.set_label('Density')
# cbar.ax.tick_params(which="both", direction="inout")

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel("Body mass (g)")
ax.set_ylabel("Bill depth (mm)")

fig.savefig("plots-gallery/penguins_kde.svg")
# pub_style.show()