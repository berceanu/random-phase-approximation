import logging
import os
import pathlib
import re
import shutil
import subprocess

logger = logging.getLogger(__name__)


def match_split(orbital_frac):
    regex = re.compile(r"(?P<orbital>\d+[a-z]+)(?P<frac>\d+/\d+)")
    m = regex.search(orbital_frac)
    return m.group("orbital"), m.group("frac")


def frac_to_html(frac):
    numerator, denominator = frac.split("/")
    return f"<sub>{numerator}&frasl;{denominator}</sub>"


def atomic_symbol_for_z(atomic_number):
    """Determine the symbol for a given proton (atomic) number Z.

    >>> atomic_symbol_for_z(1)
    ' H'
    >>> atomic_symbol_for_z(118)
    'OG'
    >>> atomic_symbol_for_z(53)
    ' I'
    """

    maxz = 118
    assert 0 < atomic_number <= maxz, "Wrong number of protons!"

    periodic_table = (
        "   HHELIBE B C N O FNENAMGALSI P SCLAR K"
        "CASCTI VCRMNFECONICUZNGAGEASSEBRKRRBSR Y"
        "ZRNBMOTCRURHPDAGCDINSNSBTE IXECSBALACEPR"
        "NDPMSMEUGDTBDYHOERTMYBLUHFTA WREOSIRPTAU"
        "HGTLPBBIPOATRNFRRAACTHPA UNPPUAMCMBKCFES"
        "FMMDNOLRRFDBSGBHHSMTDSRGCNNHFLMCLVTSOG"
    )
    assert len(periodic_table) == 2 * maxz + 2, "Error in periodic table!"

    atomic_symbol = periodic_table[2 * atomic_number : 2 * atomic_number + 2]
    assert len(atomic_symbol) == 2, "Error in atomic symbol selection!"

    return atomic_symbol


def get_nucleus(proton_number, neutron_number, joined=True, capitalize=True):
    """Return nuclide symbol, given the proton and neutron numbers.

    >>> get_nucleus(proton_number=50, neutron_number=82)
    '132Sn'
    """
    atomic_symbol = atomic_symbol_for_z(proton_number)

    if capitalize:
        atomic_symbol = atomic_symbol.title()

    mass_number = proton_number + neutron_number  # A = Z + N

    if joined:
        return f"{mass_number}{atomic_symbol}"
    else:
        return atomic_symbol, mass_number


def write_contents_to(file_path, contents):
    """Write ``contents`` to ``file_path``.

    :param file_path: path/to/file
    :param contents: file contents
    """
    file_path = pathlib.Path(file_path)

    with file_path.open("w", encoding="utf-8") as f:
        f.write(contents)
    logger.info("Wrote %s" % file_path)


def areidentical(f1, f2):
    """Return True if the two files are identical."""
    from filecmp import cmp
    import os

    # Not identical if either file is missing.
    if (not os.path.isfile(f1)) or (not os.path.isfile(f2)):
        return False

    return cmp(f1, f2)


def prepend_id(id, fname):
    return f"{id}_{fname}"


def copy_file_with_id(fname, from_job, to_job):
    local_fname = prepend_id(from_job.id, fname)
    shutil.copy(from_job.fn(fname), to_job.fn(local_fname))


def copy_file(source, destination, exist_ok=False):
    """Copy ``source`` to ``destination``.

    :param source: path/to/source/file
    :param destination: path/to/destination/file
    :param exist_ok: Overwrite destination if it already exists
    """
    source = pathlib.Path(source)
    destination = pathlib.Path(destination)

    assert source != destination, f"{source} and {destination} are identical!"
    assert source.is_file(), f"{source} not found!"

    mode = "wb" if exist_ok else "xb"
    with destination.open(mode=mode) as fid:
        fid.write(source.read_bytes())

    assert areidentical(
        source, destination
    ), f"{source} and {destination} are not identical!"

    logger.info("Copied %s to %s" % (source, destination))


def remove_from_dict(d, keys):
    """Remove ``keys`` from ``d``.

    :param d: input mappable
    :param keys: iterable of keys to be removed
    :return: new dictionary with ``keys`` removed
    """
    return {k: v for k, v in d.items() if k not in keys}


def sh(*cmd, **kwargs):
    logger.info(cmd[0])
    stdout = (
        subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs
        )
        .communicate()[0]
        .decode("utf-8")
    )
    logger.info(stdout)
    return stdout


def arefiles(file_names):
    """Check if all ``file_names`` are in ``job`` folder."""
    return lambda job: all(job.isfile(fn) for fn in file_names)


def file_contains(filename, text):
    """Checks if `filename` contains `text`."""
    return (
        lambda job: job.isfile(filename) and text in open(job.fn(filename), "r").read()
    )


def last_line_contains(filename, text):
    """Checks if last line of a file contains a given string."""

    def foo(job):
        if not job.isfile(filename):
            return False
        last_line = read_last_line(job.fn(filename)).decode("UTF-8")
        return text in last_line

    return foo


# https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file/18603065#18603065
def read_last_line(filename):
    with open(filename, "rb") as f:
        _ = f.readline()  # Read the first line.
        f.seek(-2, os.SEEK_END)  # Jump to the second last byte.
        while f.read(1) != b"\n":  # Until EOL is found...
            f.seek(-2, os.SEEK_CUR)  # ...jump back the read byte plus one more.
        last = f.readline()  # Read last line.
    return last


def isemptyfile(filename):
    return lambda job: job.isfile(filename) and os.stat(job.fn(filename)).st_size == 0
