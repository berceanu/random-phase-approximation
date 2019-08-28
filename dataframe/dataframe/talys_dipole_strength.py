from dataframe import df_path, proton_number
from mypackage.talys.api import fn_to_dict, dict_to_df, TalysAPI
from mypackage.talys.api import u_factor
from mypackage.util import atomic_symbol_for_z

talys_api = TalysAPI()

atomic_symbol = atomic_symbol_for_z(proton_number).title()
photon_strength_function_file = "%s.psf" % atomic_symbol
fpath = talys_api.backup_hfb_path / photon_strength_function_file

if __name__ == "__main__":
    psf_dict = fn_to_dict(fname=fpath, proton_number=proton_number)
    df = (
        dict_to_df(psf_dict)
        .stack(level=[0, 1])
        .reset_index(level=0, drop=True)
        .reset_index()
        .rename(
            columns={
                "Z": "proton_number",
                "A": "mass_number",
                "U": "excitation_energy",
                "fE1": "strength_function_mb",
            }
        )
        .assign(
            neutron_number=lambda frame: frame.mass_number - frame.proton_number,
            strength_function_fm=lambda frame: frame.strength_function_mb / u_factor,
            model="HF-QRPA",
            temperature=0.0,
        )
        .astype({"model": "category"})
        .sort_values(
            by=["proton_number", "neutron_number", "mass_number", "excitation_energy"]
        )
    )
    df = df[
        [
            "proton_number",
            "neutron_number",
            "mass_number",
            "model",
            "temperature",
            "excitation_energy",
            "strength_function_fm",
            "strength_function_mb",
        ]
    ]

    df.to_hdf(df_path, "talys_dipole_strengths", format="table")
