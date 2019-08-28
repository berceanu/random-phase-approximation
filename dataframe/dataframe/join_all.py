from dataframe import df_path
import pandas as pd

pd.options.display.max_rows = 30
pd.options.display.max_columns = 10

comp_ds = pd.read_hdf(df_path, "computed_dipole_strengths")
talys_ds = pd.read_hdf(df_path, "talys_dipole_strengths")


# todo remove
def my_pivot(df):
    return pd.pivot_table(
        df,
        index=["model", "temperature", "excitation_energy"],
        values=["strength_function_fm", "strength_function_mb"],
        columns=["proton_number", "neutron_number", "mass_number"],
    )


if __name__ == "__main__":
    columns = [
        "proton_number",
        "neutron_number",
        "mass_number",
        "temperature",
        "excitation_energy",
    ]
    left = comp_ds.set_index(columns)
    right = talys_ds.set_index(columns)
    df = left.merge(
        right,
        left_index=True,
        right_index=True,
        how="left",
        suffixes=("_yifei", "_talys"),
    )
    df = df.reset_index(level="excitation_energy")
    df = df[
        [
            "model_yifei",
            "model_talys",
            "excitation_energy",
            "strength_function_fm_yifei",
            "strength_function_fm_talys",
            "strength_function_mb_yifei",
            "strength_function_mb_talys",
        ]
    ]

    # todo remove
    idx = pd.IndexSlice
    # tiny = df.loc[idx[50, 76, 50 + 76, 0.0, 0.90:1.10], ("strength_function_fm_yifei", "strength_function_fm_talys")]
    # print(df.columns.tolist())
    """
    ['model_yifei',
     'model_talys',
     'strength_function_fm_yifei',
     'strength_function_fm_talys',
     'strength_function_mb_yifei',
     'strength_function_mb_talys']
    """

    df.to_hdf(df_path, "combined_dipole_strengths", format="table")
