import signac
import itertools as it

pr = signac.init_project('schema_test')

for val in (5, 6):
    pr.open_job({'a':1, 'b':2, 'c':3, 'd':4, 'e':val}).init()
    pr.open_job({'a':2, 'b':1, 'c':3, 'd':4, 'e':val}).init()


keys = ('a', 'b')
for key, group in pr.groupby(keys):
    gr1, gr2 = it.tee(group)
    statepoints = []
    for job in gr1:
        sp = job.sp()
        for k in keys:
            sp.pop(k, None)
        statepoints.append(sp)
    const_sp = dict(set.intersection(*(set(d.items()) for d in statepoints)))
    print(f"{keys} = {key}, sp = {const_sp}")
    # do something with gr2

# ('a', 'b') = (1, 2), sp = {'d': 4, 'c': 3}
# ('a', 'b') = (2, 1), sp = {'d': 4, 'c': 3}
