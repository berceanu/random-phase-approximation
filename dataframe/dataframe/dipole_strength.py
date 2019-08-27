import logging
import pathlib

import pandas as pd
import signac as sg
from dataframe import df_path, proton_number
from mypackage import code_api
from mypackage.talys.api import u_factor

pd.options.display.max_rows = 10

logger = logging.getLogger(__name__)

code = code_api.NameMapping()


def read(file_path):
    """Reads dataframe from file.

    Examples
    --------
    >>> fp = pathlib.Path('/home/berceanu/Development/random-phase-approximation/'
    ...                   'projects/rpa/workspace/2f20928c33ff7bdd58cb1833c1df8012/ftes_lorvec.out')
    >>> df = read(fp)

            strength_function_fm
    excitation_energy
    0.00             0.000000
    0.01             0.063958
    """
    df = pd.read_csv(
        file_path,
        delim_whitespace=True,
        comment="#",
        skip_blank_lines=True,
        header=None,
        names=["excitation_energy", "strength_function_fm"],
    ).set_index("excitation_energy")
    return df


def main():
    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".." / ".." / "projects" / "rpa"
    rpa = sg.get_project(root=rpa_root)

    logger.info("rpa project: %s" % rpa.root_directory())

    model = {"zero": "QRPA", "finite": "FTRPA"}

    dataframes = []
    for job in rpa.find_jobs({"proton_number": proton_number}):
        temp = "finite" if job.sp.temperature > 0 else "zero"
        fname = job.fn(code.out_file(temp, "isovector", "lorentzian"))
        df = read(fname)

        df2 = pd.concat(
            [df],
            keys=[
                (proton_number, job.sp.neutron_number, model[temp], job.sp.temperature)
            ],
            names=["proton_number", "neutron_number", "model", "temperature"],
        ).reset_index()

        dataframes.append(df2)

    df = (
        pd.concat(dataframes)
        .astype({"model": "category"})
        .assign(
            mass_number=lambda x: x.proton_number + x.neutron_number,
            strength_function_mb=lambda x: x.strength_function_fm * u_factor,
        )
        .set_index(["neutron_number", "temperature"])
        .sort_index(level=["neutron_number", "temperature"])
    )

    df.to_hdf(df_path, "computed_dipole_strengths", format="table")


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
