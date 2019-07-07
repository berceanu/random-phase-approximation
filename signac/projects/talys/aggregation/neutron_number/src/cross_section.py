#!/usr/bin/env python3
import logging
from collections import defaultdict

import mypackage.talys_api as api
import mypackage.talys_data as data
import mypackage.talys_plotting as plotting
import mypackage.util as util
import pandas as pd
import signac
from cycler import cycler
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

line_colors = ["C0", "C1", "C2", "C3"]
line_styles = ["-", "--", ":", "-."]

# todo move to plotting module in mypackage

cyl = cycler(color=line_colors) + cycler(linestyle=line_styles)

loop_cy_iter = cyl()

STYLE = defaultdict(lambda: next(loop_cy_iter))

logger = logging.getLogger(__name__)
logfname = "project.log"

talys_api = api.TalysAPI()


def main():
    proj = signac.init_project("proj")
    logger.info("current project: %s" % proj.workspace())

    talys_proj = signac.get_project(root="../../")
    logger.info("talys project: %s" % talys_proj.workspace())

    hfb_qrpa_proj = signac.get_project(root="../../hfb_qrpa/")
    logger.info("hfb+qrpa project: %s" % hfb_qrpa_proj.workspace())

    # cross section vs energy @ fixed mass number
    for neutron_number, talys_jobs in talys_proj.find_jobs(
        {"proton_number": 50, "astro": "n"}
    ).groupby("neutron_number"):

        job = proj.open_job(
            {"proton_number": 50, "neutron_number": neutron_number}
        ).init()

        fig = Figure(figsize=(6.4, 6.4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        atomic_symbol, mass_number = util.get_nucleus(50, neutron_number, joined=False)
        text = r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (
            mass_number - 1,
            atomic_symbol,
            mass_number,
            atomic_symbol,
        )

        for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.temperature):
            cross_section = data.read_cross_section(
                talys_job.fn(talys_api.cross_section_fn)
            )

            plotting.plot_cross_section(
                ax,
                cross_section["energy"],
                cross_section["compound"],
                color=STYLE[str(talys_job.sp.temperature)]["color"],
                linestyle=STYLE[str(talys_job.sp.temperature)]["linestyle"],
                label=f"T={talys_job.sp.temperature}",
                text=text,
            )

        # add HFB+QRPA data
        hfb_qrpa_job = next(
            iter(
                hfb_qrpa_proj.find_jobs(
                    filter=dict(
                        astro="n", neutron_number=neutron_number, proton_number=50
                    )
                )
            )
        )

        cross_section = data.read_cross_section(
            hfb_qrpa_job.fn(talys_api.cross_section_fn)
        )

        plotting.plot_cross_section(
            ax,
            cross_section["energy"],
            cross_section["compound"],
            color="black",
            linestyle="-",
            label=f"HFB-QRPA",
            text=text,
        )

        png_fn = "cross_section_all_T.png"
        canvas.print_png(job.fn(png_fn))
        logger.info("Saved %s" % job.fn(png_fn))

    # neutron capture rate vs temperature @ fixed mass number
    for neutron_number, talys_jobs in talys_proj.find_jobs(
        {"proton_number": 50, "astro": "y"}
    ).groupby("neutron_number"):

        job = next(
            iter(
                proj.find_jobs(
                    filter=dict(neutron_number=neutron_number, proton_number=50)
                )
            )
        )

        atomic_symbol, mass_number = util.get_nucleus(50, neutron_number, joined=False)
        text = r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (
            mass_number - 1,
            atomic_symbol,
            mass_number,
            atomic_symbol,
        )

        rate_df = pd.DataFrame()

        for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.temperature):
            df = api.read_neutron_capture_rate(talys_job)
            #  find closest temperature to the job's temperature
            closest_df = df.iloc[
                (df["T9"] - talys_job.sp.temperature).abs().argsort()[:1]
            ]
            rate_df = rate_df.append(closest_df)

        # add HFB+QRPA data
        hfb_qrpa_job = next(
            iter(
                hfb_qrpa_proj.find_jobs(
                    filter=dict(
                        astro="y", neutron_number=neutron_number, proton_number=50
                    )
                )
            )
        )
        df = api.read_neutron_capture_rate(hfb_qrpa_job)
        rate_hfb_df = df[df.index.isin(rate_df.index)]

        fig = Figure(figsize=(6.4, 6.4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        plotting.plot_capture_rate_vs_temp(
            ax,
            rate_df.iloc[:, 0],
            rate_df.iloc[:, 1],
            label="T-dep. RPA",
            color="C0",
            title=text,
        )
        plotting.plot_capture_rate_vs_temp(
            ax,
            rate_hfb_df.iloc[:, 0],
            rate_hfb_df.iloc[:, 1],
            label="HFB+QRPA",
            color="black",
        )

        png_fn = "capture_rate_v_T.png"
        canvas.print_png(job.fn(png_fn))
        logger.info("Saved %s" % job.fn(png_fn))


if __name__ == "__main__":
    logging.basicConfig(
        filename=logfname,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("==INIT STARTED==")
    main()
    logger.info("==INIT FINISHED==")
