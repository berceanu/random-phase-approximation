import pathlib
import signac as sg
import logging
import pandas as pd
from dataframe import df_path, proton_number
from mypackage.talys.api import TalysAPI
from mypackage.talys.data import read_cross_section, read_astrorate

logger = logging.getLogger(__name__)

pd.options.display.max_rows = 10
pd.options.display.max_columns = 10


# | *proton_number | *neutron_number | *mass_number | *temperature |
#     | **model |
#         | *neutron_energy | **cross_section | **capture_rate |


def get_neutron_capture_rate(*, proj, protons=proton_number, api=TalysAPI()):
    dataframes = list()
    for job in proj.find_jobs(dict(proton_number=protons, astro="y")):
        df = api.read_neutron_capture_rate(job)\
                .set_index("talys_temperature")

        temperature = job.sp.temperature if ("temperature" in proj.detect_schema()) else 0.0
        df2 = pd.concat(
            [df],
            keys=[
                (protons, job.sp.neutron_number, temperature)
            ],
            names=["proton_number", "neutron_number", "temperature"],
        ).reset_index()
        dataframes.append(df2)

    big_df = pd.concat(dataframes)
    index = big_df.columns.tolist()
    index.remove('capture_rate')
    big_df = big_df.set_index(index).sort_index()

    return big_df


def get_cross_section(*, proj, protons=proton_number, api=TalysAPI()):
    dataframes = list()
    for job in proj.find_jobs(dict(proton_number=protons, astro="n")):
        fpath = job.fn(api.cross_section_fn())
        df = read_cross_section(fpath)
        df = df.rename(columns=dict(energy="neutron_energy", xs="cross_section"))\
               .set_index("neutron_energy")

        temperature = job.sp.temperature if ("temperature" in proj.detect_schema()) else 0.0
        df2 = pd.concat(
            [df],
            keys=[
                (protons, job.sp.neutron_number, temperature)
            ],
            names=["proton_number", "neutron_number", "temperature"],
        ).reset_index()
        dataframes.append(df2)

    big_df = pd.concat(dataframes)
    index = big_df.columns.tolist()
    index.remove('cross_section')
    big_df = big_df.set_index(index).sort_index()

    return big_df


if __name__ == '__main__':
    module_path = pathlib.Path(__file__).absolute().parent

    talys_root = module_path / ".." / ".." / "projects" / "talys"
    hfb_qrpa_root = module_path / ".." / ".." / "projects" / "talys" / "hfb_qrpa"

    talys = sg.get_project(root=talys_root)
    hfb_qrpa = sg.get_project(root=hfb_qrpa_root)

    logger.info("talys project: %s" % talys.root_directory())
    logger.info("hfb_qrpa project: %s" % hfb_qrpa.root_directory())

    xs_left = get_cross_section(proj=talys)
    xs_right = get_cross_section(proj=hfb_qrpa)

    xs_df = xs_left.merge(
        xs_right,
        left_index=True,
        right_index=True,
        how="left",
        suffixes=("_yifei", "_talys"),
    ).reset_index(level="neutron_energy")

    rate_left = get_neutron_capture_rate(proj=talys)
    rate_right = get_neutron_capture_rate(proj=hfb_qrpa)

    rate_df = rate_left.merge(
        rate_right,
        left_index=True,
        right_index=True,
        how="left",
        suffixes=("_yifei", "_talys"),
    ).reset_index(level="talys_temperature")

    # xs_df.index
    # names = ['proton_number', 'neutron_number', 'temperature'], length = 14696)
    # 14696/4/11 = 334 -> length of neutron_energy
    # rate_df.index
    # names = ['proton_number', 'neutron_number', 'temperature'], length = 1320)
    # 1320/4/11 = 30  -> length of talys_temperature

    # 334 * 30 = 10020

    df = xs_df.merge(
        rate_df,
        left_index=True,
        right_index=True,
        how="left",
        # suffixes=("_yifei", "_talys"),
    )#.reset_index(level="talys_temperature")


    # for temperature, talys_jobs in talys_proj.find_jobs(
    #     {"proton_number": 50, "astro": "y"}
    # ).groupby("temperature"):

    #     cols = ["mass_number", "capture_rate"]
    #     rate_df = pd.DataFrame(columns=cols)
    #     rate_hfb_df = pd.DataFrame(columns=cols)

    #     for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.neutron_number):
    #         df = talys_api.read_neutron_capture_rate(talys_job)
    #         #  find closest temperature to the job's temperature
    #         closest_df = df.iloc[(df["T9"] - temperature).abs().argsort()[:1]]
    #         row = {
    #             "mass_number": talys_job.sp.proton_number
    #             + talys_job.sp.neutron_number
    #             - 1,
    #             "capture_rate": closest_df.iloc[0, 1],
    #         }
    #         rate_df.loc[len(rate_df)] = row

    #         # add HFB+QRPA data
    #         hfb_qrpa_job = next(
    #             iter(
    #                 hfb_qrpa_proj.find_jobs(
    #                     filter=dict(
    #                         astro="y",
    #                         neutron_number=talys_job.sp.neutron_number,
    #                         proton_number=50,
    #                     )
    #                 )
    #             )
    #         )
    #         df = talys_api.read_neutron_capture_rate(hfb_qrpa_job)
    #         #  find closest temperature to the job's temperature
    #         closest_df = df.iloc[(df["T9"] - temperature).abs().argsort()[:1]]
    #         row = {
    #             "mass_number": 50 + talys_job.sp.neutron_number - 1,
    #             "capture_rate": closest_df.iloc[0, 1],
    #         }
    #         rate_hfb_df.loc[len(rate_df)] = row

    # neutron capture rate vs temperature @ fixed mass number #
    # for neutron_number, talys_jobs in talys_proj.find_jobs(
    #     {"proton_number": 50, "astro": "y"}
    # ).groupby("neutron_number"):

    #     rate_df = pd.DataFrame()

    #     for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.temperature):
    #         df = talys_api.read_neutron_capture_rate(talys_job)
    #         #  find closest temperature to the job's temperature
    #         closest_df = df.iloc[
    #             (df["T9"] - talys_job.sp.temperature).abs().argsort()[:1]
    #         ]
    #         rate_df = rate_df.append(closest_df)

    #     # add HFB+QRPA data
    #     hfb_qrpa_job = next(
    #         iter(
    #             hfb_qrpa_proj.find_jobs(
    #                 filter=dict(
    #                     astro="y", neutron_number=neutron_number, proton_number=50
    #                 )
    #             )
    #         )
    #     )
    #     df = talys_api.read_neutron_capture_rate(hfb_qrpa_job)
    #     rate_hfb_df = df[df.index.isin(rate_df.index)]
