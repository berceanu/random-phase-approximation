"""
Project for creating a `pandas` dataframe that will contain all the project's output data.
This dataframe can then be operated on by user-defined functions, data in it can be aggregated
and plotted interactively in `jupyter` notebooks.
"""
import pathlib
import pkg_resources

model = {"zero": "QRPA", "finite": "FTRPA"}

df_path = pathlib.Path(
    pkg_resources.resource_filename("dataframe", "data/dataframe.h5")
)

units = dict()
units["model"] = None
units["neutron_number"] = None
units["temperature"] = "[MeV]"

units["energy"] = "[MeV]"
units["strength_function"] = r"[e${}^{2}$fm${}^{2}$/MeV]"
