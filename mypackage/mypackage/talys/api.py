"""
This module contains functions for generating TALYS database files.
It also stores the common filenames / paths used when running TALYS.
"""

import logging
import math
import os
import pathlib
import re
from collections import OrderedDict
from dataclasses import dataclass
from contextlib import contextmanager
import pkg_resources

import numpy as np
import pandas as pd
from jinja2 import Environment, PackageLoader

from mypackage.talys import data
from mypackage import util

# pass folder containing the template
loader = PackageLoader("mypackage.talys")
env = Environment(loader=loader)

logger = logging.getLogger(__name__)


class ConfigurationSyntaxError(Exception):
    pass


@dataclass
class TalysAPI:
    """
    Examples
    --------
    >>> import signac

    >>> pr = signac.init_project('example')
    >>> job = pr.open_job({'proton_number': 20, 'neutron_number': 20})

    >>> talys_api = TalysAPI()

    >>> talys_api.run_command
    '/home/berceanu/bin/talys < input.txt > output.txt 2> stderr.txt'

    >>> print(talys_api.database_file_path(job))
    /home/berceanu/src/talys/structure/gamma/hfb/Ca.psf

    >>> print(talys_api.template_photon_strength_function_path(job))
    /home/berceanu/Development/random-phase-approximation/mypackage/mypackage/talys/database/structure/gamma/hfb/Ca.psf

    >>> print(talys_api.database_file_backup_path(job))
    /home/berceanu/src/talys/structure/gamma/hfb/Ca_d94bb7f1e9fb6c1c5d6cc61c61b6e47d.bck
    """

    input_fn = "input.txt"
    input_template_fn = "input.j2"
    energy_fn = "n0-20.grid"
    output_fn = "output.txt"
    binary_fn = pathlib.Path.home() / "bin" / "talys"
    hfb_path = pathlib.Path.home() / "src" / "talys" / "structure" / "gamma" / "hfb"
    backup_hfb_path = pathlib.Path(
        pkg_resources.resource_filename(
            "mypackage", "talys/database/structure/gamma/hfb"
        )
    )
    stderr_fn = "stderr.txt"
    astrorate_fn = "astrorate.g"
    cross_section_png_fn = "xsec.png"

    def cross_section_fn(self, job=None) -> str:
        """TALYS output filename for cross section data."""
        return "xs000000.tot"

    @property
    def run_command(self) -> str:
        """Construct the TALYS command to be ran."""
        assert self.binary_fn.is_file(), f"{self.binary_fn} not found!"

        return (
            f"{self.binary_fn} < {self.input_fn} > {self.output_fn} 2> {self.stderr_fn}"
        )

    def read_neutron_capture_rate(self, job):
        df = data.read_astrorate(job.fn(self.astrorate_fn))
        df = df.drop(columns=["MACS"]).rename(
            columns=dict(Rate="capture_rate", T="talys_temperature")
        )
        return df

    def database_file_path(self, job):
        """Return path to job's nucleus data file in TALYS database."""
        path = self.hfb_path / psf_fn(job)
        assert path.is_file(), f"{path} not found!"
        return path

    def database_file_backup_path(self, job):
        db_fn_path = self.database_file_path(job)
        path = db_fn_path.parent / (db_fn_path.stem + "_%s.bck" % job.id)
        return path

    def template_photon_strength_function_path(self, job):
        fname = self.database_file_path(job).name
        path = self.backup_hfb_path / fname
        return path

    @contextmanager
    def replaced_database_file(self, job):
        if list(self.hfb_path.glob("*.bck")):
            raise AssertionError("Found previous backup files!")

        db_fn_path = self.database_file_path(job)

        template_psf_path = self.template_photon_strength_function_path(job)
        if not util.areidentical(template_psf_path, db_fn_path):
            raise AssertionError("TALYS photon strength function file corrupt!")

        # Backup TALYS database file (eg Sn.psf to Sn_<job._id>.bck)
        db_fn_bck_path = self.database_file_backup_path(job)
        util.copy_file(source=db_fn_path, destination=db_fn_bck_path)

        # Replace TALYS database file (eg Sn.psf) with the job's .psf file.
        util.copy_file(
            source=job.fn(job.doc["photon_strength_function"]),
            destination=db_fn_path,
            exist_ok=True,
        )
        try:
            yield
        finally:
            # Restore original TALYS database file (eg Sn.psf) from backup.
            util.copy_file(source=db_fn_bck_path, destination=db_fn_path, exist_ok=True)

            # Delete TALYS database file backup (eg. Sn_<job._id>.bck).
            os.remove(db_fn_bck_path)
            logger.info("Removed %s" % db_fn_bck_path)

    def input_file(self, job):
        """Generate TALYS input file."""
        atomic_symbol, mass_number = util.get_nucleus(
            job.sp.proton_number, job.sp.neutron_number, joined=False
        )

        # we hit the element with N - 1 with 1 neutron
        input_contents = env.get_template(self.input_template_fn).render(
            element=atomic_symbol,
            mass=mass_number - 1,
            energy_fname=self.energy_fn,
            astro=job.sp.astro,
        )
        util.write_contents_to(job.fn(self.input_fn), input_contents)

    def energy_file(self, job):
        """Generate TALYS energy input file."""
        file_path = pathlib.Path(job.fn(self.energy_fn))
        np.savetxt(
            file_path, energy_values(job, log=True), fmt="%.3f", newline=os.linesep
        )
        logger.info("Wrote %s" % file_path)


def energy_values(job, log=False, digits=None):
    """Generate TALYS neutron energy input file contents."""
    if log:
        if digits is None:
            digits = 3

        v1 = np.linspace(0.001, 0.01, 10)
        v2 = np.linspace(0.015, 0.03, 4)
        v3 = np.linspace(0.04, 0.2, 17)
        v4 = np.linspace(0.22, 0.3, 5)
        v5 = np.linspace(0.35, 0.4, 2)
        v6 = np.linspace(0.5, 20.0, 296)

        my_v = np.empty(
            v1.size + v2.size + v3.size + v4.size + v5.size + v6.size, dtype=np.float64
        )
        np.concatenate((v1, v2, v3, v4, v5, v6), out=my_v)
    else:
        if digits is None:
            digits = 1

        my_v, step = np.linspace(0.1, 20.0, 300, retstep=True)
        assert math.isclose(step, 0.1), f"step {step} is not 0.1!"

    return my_v.round(digits)


def cast_to(to_type, iterable):
    return (to_type(val) for val in iterable)


def psf_fn(job):
    """Gets the job's associated photon strength function file name."""
    atomic_symbol, _ = util.get_nucleus(
        job.sp.proton_number, job.sp.neutron_number, joined=False
    )
    return "%s.psf" % atomic_symbol


alpha = 7.297352570e-03  # fine structure constant
u_factor = 10 * 16 * math.pi ** 3 * alpha / 9  # 4.022 mb / (e^2 * fm^2)


# see src/temp/sum_rule.ipynb


def lorvec_to_df(fname, Z, A, unit_factor=u_factor):  # mb / (e^2 * fm^2)
    df_lorvec = pd.read_csv(
        fname,
        delim_whitespace=True,
        comment="#",
        skip_blank_lines=True,
        header=None,
        names=["U", "fE1"],
    )
    logger.info("Read %s" % fname)

    # multiply by constant to convert e^2*fm^2 to mb
    df_lorvec["fE1"] = df_lorvec["fE1"].apply(lambda row: row * unit_factor)  # mb/MeV

    df_lorvec = df_lorvec[(df_lorvec.U >= 0.1) & (df_lorvec.U <= 30)]  # MeV

    every_10 = df_lorvec.iloc[::10, :]
    every_10.reset_index(drop=True, inplace=True)

    df = every_10.T
    df2 = pd.concat([df], keys=[A], names=["A"])
    df3 = pd.concat([df2], keys=[Z], names=["Z"])
    return df3


def fn_to_dict(fname, proton_number):
    with open(fname) as f:
        contents = f.read()
    logger.info("Read %s" % fname)

    new_line = re.compile(r"\n[\s\r]+?\n")
    blocks = new_line.split(contents)

    assert blocks[-1].strip() == "", "Last line not empty!"
    assert len(blocks[:-1]) > 0, "Not right number of blocks!"
    # there is a gap from A = 170 to A = 178 for Z = 50

    ond = OrderedDict()  # ordered_nested_dict
    ond[proton_number] = OrderedDict()

    for blk in blocks[:-1]:  # except last line
        block = blk.splitlines()

        nucleus_header = block[0].split()
        Z, A = cast_to(int, nucleus_header[1::2])
        if (nucleus_header[0::2] != ["Z=", "A="]) or (Z != proton_number):
            raise ConfigurationSyntaxError("Wrong header inside %s!" % fname)

        col_header = block[1].split()
        if col_header[:2] != ["U[MeV]", "fE1[mb/MeV]"]:
            raise ConfigurationSyntaxError("Wrong header inside %s!" % fname)

        columns = (row.split() for row in block[2:])
        c1_vals, c2_vals = zip(*columns)

        d = OrderedDict()
        d[A] = OrderedDict(
            U=tuple(cast_to(float, c1_vals)), fE1=tuple(cast_to(float, c2_vals))
        )
        ond[Z].update(d)

    return ond


def dict_to_fn(ordered_nested_dict, fname, proton_number):
    ond = ordered_nested_dict

    assert len(ond.keys()) == 1, "More than one Z present in dict!"

    assert list(ond.keys())[0] == proton_number, "Z from dict and file does not match!"

    col_header = "  U[MeV]  fE1[mb/MeV]"

    with open(fname, "w") as f:
        for Z in ond.keys():
            for A in ond[Z].keys():
                nucleus_header = f" Z={Z:4d} A={A:4d}"
                f.write(f"{nucleus_header}\n")
                f.write(f"{col_header}\n")
                for U, fE1 in zip(ond[Z][A]["U"], ond[Z][A]["fE1"]):
                    f.write("{:9.3f}   {:.3E}\n".format(U, fE1))
                f.write(" \n")

    logger.info("Wrote %s" % fname)


def df_to_dict(df):
    if isinstance(df.index, pd.MultiIndex):
        mydf = df.T.copy()
    else:
        mydf = df.copy()

    ond = OrderedDict()  # ordered_nested_dict
    for Z, A, data_col in mydf.columns:
        if Z not in ond.keys():
            ond[Z] = OrderedDict()
        if A not in ond[Z].keys():
            ond[Z][A] = OrderedDict()
        ond[Z][A][data_col] = tuple(mydf[Z][A][data_col].values)
    return ond


def dict_to_df(ordered_nested_dict):
    reform = {
        (firstKey, secondKey, thirdKey): values
        for firstKey, middleDict in ordered_nested_dict.items()
        for secondKey, innerdict in middleDict.items()
        for thirdKey, values in innerdict.items()
    }
    df = pd.DataFrame(reform)
    df = df.T  # transpose
    df.index.names = ["Z", "A", None]
    return df.T  # transpose back


def atomic_mass_numbers(talys):
    if not isinstance(talys, pd.MultiIndex):
        df = talys.T.copy()
    else:
        df = talys.copy()
    return df.index.levels[1].values


def replace_table(Z, A, talys, lorvec):
    transpose = False
    if not isinstance(talys.index, pd.MultiIndex):
        df1 = talys.T.copy()
        transpose = True
    else:
        df1 = talys.copy()
    if not isinstance(lorvec.index, pd.MultiIndex):
        df2 = lorvec.T.copy()
    else:
        df2 = lorvec.copy()
    df1.loc[(Z, A, ["U", "fE1"]), :] = df2.loc[(Z, A, ["U", "fE1"]), :]
    logger.info('Replaced loc[({}, {}, ["U", "fE1"]), :]'.format(Z, A))

    return df1.T if transpose else df1


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
