import pathlib
import signac as sg
import logging
import pandas as pd
from dataash5 import proton_number, df_path
from mypackage.talys.api import TalysAPI

logger = logging.getLogger(__name__)

pd.options.display.max_rows = 20
pd.options.display.max_columns = 10

my_astroT = 0.0001


def get_neutron_capture_rate(*, proj, protons=proton_number, api=TalysAPI()):
    dataframes = list()
    for job in proj.find_jobs(dict(proton_number=protons, astro="y")):
        ncr = api.read_neutron_capture_rate(job)

        ncr = ncr.loc[(ncr["talys_temperature"] - my_astroT).abs().argsort()].head(1)

        ncr = ncr.rename(columns={"talys_temperature": "astroT"}).set_index("astroT")

        full_df = pd.concat(
            [ncr],
            keys=[(protons, job.sp.neutron_number)],
            names=["proton_number", "neutron_number"],
        ).reset_index()
        dataframes.append(full_df)

    big_df = pd.concat(dataframes)
    index = big_df.columns.tolist()
    index.remove("capture_rate")
    big_df = big_df.set_index(index).sort_index()

    return big_df


def main():
    module_path = pathlib.Path(__file__).absolute().parent
    talys_root = module_path / ".." / ".." / "projects" / "talys"
    talys = sg.get_project(root=talys_root)
    logger.info("talys project: %s" % talys.root_directory())

    rate_df = get_neutron_capture_rate(proj=talys)

    return rate_df.reset_index()


if __name__ == "__main__":
    df = main()
    df.to_hdf(df_path, "capture_rate", format="table")
