import pandas as pd
import signac as sg

from mypackage import code_api

import logging

logger = logging.getLogger(__name__)

code = code_api.NameMapping()

model = {"zero": "QRPA", "finite": "FTRPA"}


def main():
    rpa = sg.get_project(root="../rpa")
    logger.info("rpa project: %s" % rpa.root_directory())

    dataframes = []
    for job in rpa.find_jobs({"proton_number": 50}):
        temp = "finite" if job.sp.temperature > 0 else "zero"

        print(model[temp], job.sp.neutron_number, job.sp.temperature)
        fname = job.fn(code.out_file(temp, "isovector", "lorentzian"))

        df = pd.read_csv(
            fname,
            delim_whitespace=True,
            comment="#",
            skip_blank_lines=True,
            header=None,
            names=["energy", "strength_function"],
        )

        df.set_index("energy", inplace=True)
        df2 = pd.concat(
            [df],
            keys=[(model[temp], job.sp.neutron_number, job.sp.temperature)],
            names=["model", "neutron_number", "temperature"],
        )

        dataframes.append(df2)

    df = pd.concat(dataframes)
    df.reset_index(inplace=True)

    print(df.head().to_string())
    print(df.tail().to_string())

    df.to_pickle("dataframe.pkl")

    units = dict()
    units["model"] = None
    units["neutron_number"] = None
    units["temperature"] = "[MeV]"

    units["energy"] = "[MeV]"
    units["strength_function"] = "[e${}^{2}$fm${}^{2}$/MeV]"


# for (z, n), group in rpa.groupby(("proton_number", "neutron_number")):
#     logger.info("(Z, N) =  (%s, %s)" % (z, n))
#
#     atomic_symbol, mass_number = util.get_nucleus(z, n, joined=False)
#
#     for job in group:
#         sp = job.sp._as_dict()


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
