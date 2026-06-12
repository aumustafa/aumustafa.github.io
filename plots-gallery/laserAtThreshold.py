import numpy as np
import pub_style

y = np.linspace(0.5, 1.5, 1000)

q_sat = 1e10

q = 0.5 * q_sat * (y - 1) + 0.5 * q_sat * np.sqrt((y - 1) ** 2 + 4 * y / q_sat)

pub_style.use(preamble='serif')
fig, ax = pub_style.new_figure(despine=False, minor_ticks=True)

ax.set_xlabel(r'$g_0 / g_t$')
ax.set_ylabel(r'$\log\bar{q}_\nu$')
ax.set_xlim(0.5, 1.5)
ax.plot(y, np.log10(q), 'k')
fig.savefig('laserAtThreshold')
