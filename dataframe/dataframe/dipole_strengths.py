import logging
import pathlib
from dataframe import df_path, model
import pandas as pd
import signac as sg
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

            strength_function
    energy
    0.00             0.000000
    0.01             0.063958
    """
    df = pd.read_csv(
        file_path,
        delim_whitespace=True,
        comment="#",
        skip_blank_lines=True,
        header=None,
        names=["energy", "strength_function"],
    ).set_index("energy")
    return df


def main():
    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".." / ".." / "projects" / "rpa"
    rpa = sg.get_project(root=rpa_root)

    logger.info("rpa project: %s" % rpa.root_directory())

    dataframes = []
    for job in rpa.find_jobs({"proton_number": 50}):
        temp = "finite" if job.sp.temperature > 0 else "zero"
        fname = job.fn(code.out_file(temp, "isovector", "lorentzian"))
        df = read(fname)

        df2 = pd.concat(
            [df],
            keys=[(model[temp], job.sp.neutron_number, job.sp.temperature)],
            names=["model", "neutron_number", "temperature"],
        ).reset_index()

        dataframes.append(df2)

    df = (
        pd.concat(dataframes)
        .astype({"model": "category"})
        .set_index(["model", "neutron_number", "temperature"])
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
