from cycler import cycler
from collections import defaultdict

cyl = cycler(color=['C0', 'C1', 'C2', 'C3']) + cycler(linestyle=['-', '--', ':', '-.'])
loop_cy_iter = cyl()
STYLE = defaultdict(lambda : next(loop_cy_iter))


def foo(**kwargs):
    print(kwargs['color'], kwargs['linestyle'])


for var in (0., 1., 2., 3., 4.):
    foo(**STYLE[var])

print()

for var in (1., 0., 2., 4., 3.):
    foo(**STYLE[var])
