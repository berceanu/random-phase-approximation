import logging
import pathlib
import subprocess

logger = logging.getLogger(__name__)


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

    atomic_symbol = periodic_table[2 * atomic_number: 2 * atomic_number + 2]
    assert len(atomic_symbol) == 2, "Error in atomic symbol selection!"

    return atomic_symbol


def get_nucleus(proton_number, neutron_number):
    """Return nuclide symbol, given the proton and neutron numbers.

    >>> get_nucleus(proton_number=50, neutron_number=82)
    'SN132'
    """

    atomic_symbol = atomic_symbol_for_z(proton_number)
    mass_number = proton_number + neutron_number  # A = Z + N
    return f"{atomic_symbol}{mass_number}"


def split_element_mass(job):
    mass_number = job.sp.proton_number + job.sp.neutron_number
    element = atomic_symbol_for_z(job.sp.proton_number)
    element = element.title()  # capitalize first letter only
    return element, mass_number


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


def copy_file(source, destination, exist_ok=False):
    """Copy ``source`` to ``destination``.

    :param source: path/to/source/file
    :param destination: path/to/destination/file
    :param exist_ok: Overwrite destination if it already exists
    """
    source = pathlib.Path(source)
    destination = pathlib.Path(destination)
    # todo check source and destination are not identical
    assert source.is_file(), f"{source} not found!"

    mode = "wb" if exist_ok else "xb"
    with destination.open(mode=mode) as fid:
        fid.write(source.read_bytes())

    assert areidentical(source, destination), f"{source} and {destination} are not identical!"

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
