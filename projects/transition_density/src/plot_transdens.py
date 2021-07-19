"""Plot the QRPA neutron and proton transition densities for various isotopes."""
import signac
import pandas as pd
from matplotlib import pyplot, ticker
from figstyle import width, golden_ratio
import numpy as np
import mypackage.util as util
from decimal import Decimal


class Labeloffset:
    def __init__(self, ax, label="", axis="y"):
        self.axis = {"y": ax.yaxis, "x": ax.xaxis}[axis]
        self.label = label
        ax.callbacks.connect(axis + "lim_changed", self.update)
        ax.figure.canvas.draw()
        self.update(None)

    def update(self, lim):
        fmt = self.axis.get_major_formatter()
        self.axis.offsetText.set_visible(False)
        self.axis.set_label_text(self.label + " " + fmt.get_offset())


def read_transition_density(fname):
    df = pd.read_csv(
        fname,
        header=None,
        delim_whitespace=True,
        skip_blank_lines=True,
        comment="#",
        usecols=[0, 2, 3],
        names=["r", "neutron", "proton"],
    )
    return df


LETTERS = ("(a)", "(b)", "(c)", "(d)", "(e)")


def main():
    """Main entry point."""
    project = signac.get_project(search=False)
    print(f"project {project}")

    panel_counter = -1
    for proton_number in (
        50,
        # 58,
    ):
        for neutron_number, group in project.find_jobs(
            {
                "transition_energy": {"$ne": str(round(Decimal(0.42), 2))},
                "proton_number": proton_number,
            }
        ).groupby("neutron_number"):
            jobs = list(sorted(group, key=lambda job: job.sp.transition_energy))
            num_jobs = len(jobs)
            fig, axes = pyplot.subplots(
                nrows=num_jobs, sharex=True, figsize=(width, width / golden_ratio)
            )
            nucleus = util.get_nucleus(proton_number, neutron_number, joined=False)
            # fig.suptitle(r"RQRPA transition densities in %s" % nucleus)
            axes = np.atleast_1d(axes)
            upper_panel = True
            for ax, job in zip(axes, jobs):
                panel_counter += 1
                ax.text(
                    0.05,
                    0.80,
                    f"{LETTERS[panel_counter]} {job.sp.transition_energy} MeV",
                    transform=ax.transAxes,
                )
                if upper_panel:
                    ax.text(
                        0.15,
                        0.15,
                        r"$^{{{}}}${}".format(nucleus[1], nucleus[0]),
                        transform=ax.transAxes,
                    )
                    upper_panel = False
                # ax.text(
                #     0.65,
                #     0.15,
                #     f"{job.sp.transition_energy} MeV",
                #     transform=ax.transAxes,
                # )
                df = read_transition_density(job.fn("ztes_transdens.out"))
                df.proton *= -df.r ** 2
                df.neutron *= -df.r ** 2
                ax.plot(
                    "r",
                    "neutron",
                    color="black",
                    linestyle="solid",
                    data=df,
                    label="neutron",
                )
                ax.plot(
                    "r",
                    "proton",
                    color="black",
                    linestyle="dashed",
                    data=df,
                    label="proton",
                )
                ax.set_xlim(-0.2, 12.2)

                ax.axhline(color="0.5", linestyle="dotted", linewidth=0.5)

                formatter = ticker.ScalarFormatter(useMathText=False)
                formatter.set_powerlimits((-2, 2))
                ax.yaxis.set_major_formatter(formatter)

                _ = Labeloffset(
                    ax, label=r"$r^2\delta \rho$ $[\mathrm{fm^{-1}}]$", axis="y"
                )

            axes[0].legend(handlelength=1)
            axes[-1].set_xlabel(r"$r$ $[\mathrm{fm}]$")

            fig.subplots_adjust(hspace=0.05, bottom=0.14, left=0.16)
            fig.savefig(str(nucleus[1]) + nucleus[0])
            pyplot.close(fig)


if __name__ == "__main__":
    main()
