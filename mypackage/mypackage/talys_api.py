"""
This module contains functions for generating TALYS database files.
It also stores the common filenames / paths used when running TALYS.
"""

import pandas as pd
import re
import os
import math
import numpy as np
from collections import OrderedDict
import pathlib
from dataclasses import dataclass
import logging
from . import util
from jinja2 import Environment, PackageLoader

# pass folder containing the template
loader = PackageLoader("mypackage", "templates")
env = Environment(loader=loader)

logger = logging.getLogger(__name__)

# move this file to talys/api submodule


class ConfigurationSyntaxError(Exception):
    pass


@dataclass
class TalysAPI:
    input_fn = "input.txt"
    input_template_fn = "input.j2"
    energy_fn = "energy.in"
    output_fn = "output.txt"
    binary_fn = pathlib.PosixPath("~/bin/talys").expanduser()
    hfb_path = pathlib.PosixPath("~/src/talys/structure/gamma/hfb/").expanduser()
    backup_hfb_path = pathlib.Path(str(hfb_path).replace("talys", "backup_talys"))
    stderr_fn = "stderr.txt"
    cross_section_fn = "xs000000.tot"
    cross_section_png_fn = "xsec.png"

    @property
    def run_command(self) -> str:
        """Construct the TALYS command to be ran."""
        assert self.binary_fn.is_file(), f"{self.binary_fn} not found!"

        return (
            f"{self.binary_fn} < {self.input_fn} > {self.output_fn} 2> {self.stderr_fn}"
        )


# todo refactor functions below into TalysAPI methods


def database_file_path(job, api=TalysAPI()):
    """Return path to job's nucleus data file in TALYS database."""
    element, _ = util.split_element_mass(job)
    database_file = api.hfb_path / f"{element}.psf"

    assert database_file.is_file(), f"{database_file} not found!"
    return database_file


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
        v6 = np.linspace(0.5, 30.0, 296)

        my_v = np.empty(
            v1.size + v2.size + v3.size + v4.size + v5.size + v6.size, dtype=np.float64
        )
        np.concatenate((v1, v2, v3, v4, v5, v6), out=my_v)
    else:
        if digits is None:
            digits = 1

        my_v, step = np.linspace(0.1, 30.0, 300, retstep=True)
        assert math.isclose(step, 0.1), f"step {step} is not 0.1!"

    return my_v.round(digits)


def energy_file(job, api=TalysAPI()):
    """Generate TALYS energy input file."""
    file_path = pathlib.Path(job.fn(api.energy_fn))
    np.savetxt(file_path, energy_values(job, log=True), fmt="%.3f", newline=os.linesep)
    logger.info("Wrote %s" % file_path)


def input_file(job, api=TalysAPI()):
    """Generate TALYS input file."""
    element, mass = util.split_element_mass(job)
    # we hit the element with N - 1 with 1 neutron
    input_contents = env.get_template(api.input_template_fn).render(
        element=element, mass=mass - 1, energy_fname=api.energy_fn, astro=job.sp.astro
    )
    util.write_contents_to(job.fn(api.input_fn), input_contents)


def cast_to(to_type, iterable):
    return (to_type(val) for val in iterable)


def z_from_fname(fname):
    fn = os.path.basename(fname)
    Z = int("".join(filter(lambda c: not c.isalpha(), fn)))
    return Z


α = 7.297352570e-03  # fine structure constant
u_factor = 10 * 16 * math.pi ** 3 * α / 9  # 4.022 mb / (e^2 * fm^2)


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


def fn_to_dict(fname):
    with open(fname) as f:
        contents = f.read()
    logger.info("Read %s" % fname)

    new_line = re.compile(r"\n[\s\r]+?\n")
    blocks = new_line.split(contents)

    assert blocks[-1].strip() == "", "Last line not empty!"
    assert len(blocks[:-1]) == 82, "Not right number of blocks!"
    # there is a gap from A = 170 to A = 178 for Z = 50

    z_fn = z_from_fname(fname)
    ond = OrderedDict()  # ordered_nested_dict
    ond[z_fn] = OrderedDict()

    for blk in blocks[:-1]:  # except last line
        block = blk.splitlines()

        nucleus_header = block[0].split()
        Z, A = cast_to(int, nucleus_header[1::2])
        if (nucleus_header[0::2] != ["Z=", "A="]) or (Z != z_fn):
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


def dict_to_fn(ordered_nested_dict, fname):
    ond = ordered_nested_dict

    assert len(ond.keys()) == 1, "More than one Z present in dict!"

    z_fn = z_from_fname(fname)
    assert list(ond.keys())[0] == z_fn, "Z from dict and file does not match!"

    col_header = f"  U[MeV]  fE1[mb/MeV]"

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
