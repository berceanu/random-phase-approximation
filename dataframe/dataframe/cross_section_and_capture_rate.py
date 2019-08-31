import pathlib
import signac as sg
import logging
import pandas as pd
from dataframe import proton_number, df_path
from mypackage.talys.api import TalysAPI
from mypackage.talys.data import read_cross_section

logger = logging.getLogger(__name__)

pd.options.display.max_rows = 20
pd.options.display.max_columns = 10


def get_neutron_capture_rate(*, proj, protons=proton_number, api=TalysAPI()):
    dataframes = list()
    for job in proj.find_jobs(dict(proton_number=protons, astro="y")):
        ncr = api.read_neutron_capture_rate(job)

        if "temperature" in proj.detect_schema():
            ncr = ncr.loc[
                (ncr["talys_temperature"] - job.sp.temperature).abs().argsort()
            ].head(1)
            ncr.iloc[0, 0] = job.sp.temperature

        ncr = ncr.rename(columns={"talys_temperature": "temperature"}).set_index(
            "temperature"
        )

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


def get_cross_section(*, proj, protons=proton_number, api=TalysAPI()):
    dataframes = list()
    for job in proj.find_jobs(dict(proton_number=protons, astro="n")):
        fpath = job.fn(api.cross_section_fn())
        cs = read_cross_section(fpath)
        cs = cs.rename(
            columns={"energy": "neutron_energy", "xs": "cross_section"}
        ).set_index("neutron_energy")

        temperature = (
            job.sp.temperature if ("temperature" in proj.detect_schema()) else 0.0
        )

        df2 = pd.concat(
            [cs],
            keys=[(protons, job.sp.neutron_number, temperature)],
            names=["proton_number", "neutron_number", "temperature"],
        ).reset_index()
        dataframes.append(df2)

    big_df = pd.concat(dataframes)
    index = big_df.columns.tolist()
    index.remove("cross_section")
    big_df = big_df.set_index(index).sort_index()

    return big_df


def main():
    module_path = pathlib.Path(__file__).absolute().parent

    talys_root = module_path / ".." / ".." / "projects" / "talys"
    hfb_qrpa_root = module_path / ".." / ".." / "projects" / "talys" / "hfb_qrpa"

    talys = sg.get_project(root=talys_root)
    hfb_qrpa = sg.get_project(root=hfb_qrpa_root)

    logger.info("talys project: %s" % talys.root_directory())
    logger.info("hfb_qrpa project: %s" % hfb_qrpa.root_directory())

    xs_left = get_cross_section(proj=talys)
    xs_right = get_cross_section(proj=hfb_qrpa)

    right_suffix = "_talys"
    xs_df = xs_left.join(xs_right, rsuffix=right_suffix)

    rate_left = get_neutron_capture_rate(proj=talys)
    rate_right = get_neutron_capture_rate(proj=hfb_qrpa)

    rate_df = rate_left.join(rate_right, rsuffix=right_suffix)

    df = xs_df.reset_index(level="neutron_energy").join(rate_df)

    return df


if __name__ == "__main__":
    df = main()
    df.to_hdf(df_path, "cross_section_capture_rate", format="table")
