import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from matplotlib import rcParams


# matplotlib settings
min_exp = tuple(rcParams['axes.formatter.limits'])[0]
y_formatter = ScalarFormatter(useMathText=True)
y_formatter.set_powerlimits((min_exp, 5))



x = np.arange(0, 1, .01)



fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(6, 6))

ax1.plot(x * 1e5 + 1e10, x * 100000)
ax1.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax1.yaxis.set_major_formatter(y_formatter)

ax2.plot(x * 1e5, x * 1e-4)
ax2.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

ax3.plot(-x * 1e5 - 1e10, -x * 1e-5 - 1e-10)
ax3.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax3.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

ax4.plot(-x * 1e5, -x * 1e-4)
ax4.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax4.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

fig.subplots_adjust(wspace=0.7, hspace=0.6)

fig.savefig('test.png')