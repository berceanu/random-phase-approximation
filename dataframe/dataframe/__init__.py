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

# | proton_number | neutron_number | mass_number |
#     | model | temperature |
#         | excitation_energy | neutron_energy |
#             | strength_function_fm | strength_function_mb |
#                 | cross_section | capture_rate |
