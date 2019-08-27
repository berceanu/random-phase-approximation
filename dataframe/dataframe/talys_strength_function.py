from mypackage.talys.api import fn_to_dict, dict_to_df, TalysAPI
from dataframe import proton_number
from mypackage.util import atomic_symbol_for_z

# import pathlib

talys_api = TalysAPI()

atomic_symbol = atomic_symbol_for_z(proton_number).title()
photon_strength_function_file = "%s.psf" % atomic_symbol
fpath = talys_api.backup_hfb_path / photon_strength_function_file

psf_dict = fn_to_dict(fname=fpath, proton_number=proton_number)
df = dict_to_df(psf_dict)

df2 = df.stack(1).reset_index()

if __name__ == "__main__":
    print(fpath)
