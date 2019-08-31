from dataframe import df_path
import pandas as pd
from dataframe import (
    dipole_strength,
    talys_dipole_strength,
    cross_section_and_capture_rate,
)

pd.options.display.max_rows = 30
pd.options.display.max_columns = 10


def main():
    xs_rate_data = cross_section_and_capture_rate.main().reset_index()
    xs_rate_data.to_hdf(df_path, "neutron_energy", format="table")

    left = dipole_strength.main().reset_index()
    right = talys_dipole_strength.main().reset_index()

    nn_right = right.loc[:, "neutron_number"]
    nn_left = left.loc[:, "neutron_number"]
    mask = nn_right.isin(nn_left)
    right = right.loc[mask, :]

    energy_right = right.loc[:, "excitation_energy"]
    energy_left = left.loc[:, "excitation_energy"]
    mask = energy_left.isin(energy_right)
    left = left.loc[mask, :]

    df = left.merge(
        right,
        on=["proton_number", "neutron_number", "temperature", "excitation_energy"],
        how="left",
    )
    df.to_hdf(df_path, "excitation_energy", format="table")


if __name__ == "__main__":
    main()
