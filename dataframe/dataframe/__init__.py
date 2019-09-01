"""
Project for creating a `pandas` dataframe that will contain all the project's output data.
This dataframe can then be operated on by user-defined functions, data in it can be aggregated
and plotted interactively in `jupyter` notebooks.
"""
import pathlib
import pkg_resources

proton_number = 50

df_path = pathlib.Path(
    pkg_resources.resource_filename("dataframe", "data/dataframe.h5")
)

units = dict()
units["temperature"] = "[MeV]"  # T/T9
units["excitation_energy"] = "[MeV]"  # E/U
units["neutron_energy"] = "[MeV]"  # E_n
units["strength_function_fm"] = r"[e${}^{2}$fm${}^{2}$/MeV]"  # R
units["strength_function_mb"] = "[mb/MeV]"  # fE1
units["cross_section"] = "[mb]"
units["capture_rate"] = r"s${}^{-1}$cm${}^{3}$mol${}^{-1}$"  # Rate


def model(temperature, talys=False):
    if talys:
        return "HF-QRPA"
    if temperature > 0:
        return "FTRMF + FTRPA"
    return "RHB + QRPA"
