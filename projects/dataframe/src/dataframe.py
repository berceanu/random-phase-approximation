import pandas as pd
import signac as sg

from mypackage import code_api
from mypackage import util

import logging
logger = logging.getLogger(__name__)

code = code_api.NameMapping()

rpa = sg.get_project(root="../rpa")
dataframe = sg.get_project(root="./")

logger.info("rpa project: %s" % rpa.root_directory())
logger.info("agg project: %s" % dataframe.root_directory())


# fn = job.fn(code_mapping.out_file(temp, skalvec, lorexc))
# df = pd.read_csv(
#     fn,
#     delim_whitespace=True,
#     comment="#",
#     skip_blank_lines=True,
#     header=None,
#     names=["energy", "transition_strength"],
# )
# df = df[(df.energy >= minEnergy) & (df.energy <= maxEnergy)]  # MeV
#
#
#
# for (z, n), group in rpa.groupby(("proton_number", "neutron_number")):
#     logger.info("(Z, N) =  (%s, %s)" % (z, n))
#
#     atomic_symbol, mass_number = util.get_nucleus(z, n, joined=False)
#
#     gr1, gr2 = it.tee(group)
#
#     statepoints = []
#     origin = {}
#     for job in gr1:
#         origin[f"T = {job.sp.temperature} MeV".replace(".", "_")] = str(job)
#         sp = job.sp._as_dict()
#         statepoints.append(sp)
#     const_sp = dict(set.intersection(*(set(d.items()) for d in statepoints)))


if __name__ == "__main__":
    logging.basicConfig(
        filename="project.log",
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("==RUN STARTED==")
    main()
    logger.info("==RUN FINISHED==")
