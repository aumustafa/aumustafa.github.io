import numpy as np
import pub_style

X = np.linspace(0, 10, 1000)
Y = np.sin(X)

pub_style.use()
fig, ax = pub_style.new_figure(width_mm=56)
ax.plot(X, Y)
fig.savefig("plots-gallery/simplest.pdf")