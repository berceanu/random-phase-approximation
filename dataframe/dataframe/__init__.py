"""
Project for creating a `pandas` dataframe that will contain all the project's output data.
This dataframe can then be operated on by user-defined functions, data in it can be aggregated
and plotted interactively in `jupyter` notebooks.
"""
import pathlib
import pkg_resources

df_path = pathlib.Path(
    pkg_resources.resource_filename("dataframe", "data/dataframe.pkl")
)
