from mypackage.talys.api import fn_to_dict, dict_to_df, TalysAPI
from dataframe import proton_number
from mypackage.util import atomic_symbol_for_z
from mypackage.talys.api import u_factor


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
        .assign(neutron_number=lambda frame: frame.mass_number - frame.proton_number,
                strength_function_fm=lambda frame: frame.strength_function_mb / u_factor,
                model='TALYS',
                temperature=0.0)
        .astype({"model": "category"})
        .query("76 <= neutron_number <= 96")
        .set_index(["neutron_number"])
        .sort_index()
    )

    print(df)
