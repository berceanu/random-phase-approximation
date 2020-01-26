import logging
import pathlib

import pandas as pd
import signac as sg
from dataash5 import df_path, proton_number
from mypackage import code_api

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

    dataframes = []
    for job in rpa.find_jobs({"proton_number": proton_number}):
        temp = "finite" if job.sp.temperature > 0 else "zero"
        fname = job.fn(code.out_file(temp, "isovector", "lorentzian"))
        df = read(fname)

        df2 = pd.concat(
            [df],
            keys=[(proton_number, job.sp.neutron_number, job.sp.temperature)],
            names=["proton_number", "neutron_number", "temperature"],
        ).reset_index()

        dataframes.append(df2)

    df = (
        pd.concat(dataframes)
        .set_index(
            ["proton_number", "neutron_number", "temperature", "excitation_energy"]
        )
        .sort_index()
    )

    return df


if __name__ == "__main__":
    df = main()
    df.to_hdf(df_path, "computed_dipole_strengths", format="table")
