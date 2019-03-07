# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
import re
import pprint
from collections import OrderedDict

# %%
class ConfigurationSyntaxError(Exception):
    pass


def cast_to(to_type, iterable):
    return (to_type(val) for val in iterable)


def z_from_fname(fname):
    Z = int(''.join(filter(lambda c: not c.isalpha(), fname)))
    return Z


def lorvec_to_df(fname):
    # @TODO multiply by constant to convert e^2fm^2 to barn
    df_lorvec = pd.read_csv(fname, delim_whitespace=True, comment='#', skip_blank_lines=True,
                header=None, names=['U', 'fE1'])

    df_lorvec = df_lorvec[(df_lorvec.U >= 0.1) & (df_lorvec.U <= 30)] # MeV

    every_10 = df_lorvec.iloc[::10, :]
    every_10.reset_index(drop=True, inplace=True)

    df = every_10.T
    df2 = pd.concat([df], keys=[146], names=['A'])
    df3 = pd.concat([df2], keys=[50], names=['Z'])
    return df3


def fn_to_dict(fname):
    z_fn = z_from_fname(fname)
    with open(fname) as f:
        contents = f.read()
    
    new_line = re.compile(r'\n[\s\r]+?\n')
    blocks = new_line.split(contents)
    
    assert blocks[-1].strip() == '', "Last line not empty!"
    assert len(blocks[:-1]) == 82, "Not right number of blocks!"
    # there is a gap from A = 170 to A = 178 for Z = 50
    
    ond = OrderedDict() # ordered_nested_dict
    ond[z_fn] =  OrderedDict()
    
    for blk in blocks[:-1]: # except last line
        block = blk.splitlines()
    
        nucleus_header = block[0].split()
        Z, A = cast_to(int, nucleus_header[1::2])
        if (nucleus_header[0::2] != ['Z=', 'A=']) or (Z != z_fn):
            raise ConfigurationSyntaxError('Wrong header inside %s!' % fname)

        col_header = block[1].split()
        if col_header[:2] != ['U[MeV]', 'fE1[mb/MeV]']:
            raise ConfigurationSyntaxError('Wrong header inside %s!' % fname)

        columns = (row.split() for row in block[2:])
        c1_vals, c2_vals = zip(*columns)

        d = OrderedDict()
        d[A] = OrderedDict(  U=tuple(cast_to(float, c1_vals)),
                           fE1=tuple(cast_to(float, c2_vals)))
        ond[Z].update(d)
    
    return ond


def dict_to_fn(ordered_nested_dict, fname):
    ond = ordered_nested_dict

    assert len(ond.keys()) == 1, "More than one Z present in dict!"

    z_fn = z_from_fname(fname)
    assert list(ond.keys())[0] == z_fn, "Z from dict and file does not match!"

    col_header = f'  U[MeV]  fE1[mb/MeV]'
    
    with open(fname, "w") as f:
        for Z in ond.keys():
            for A in ond[Z].keys():
                nucleus_header = f' Z={Z:4d} A={A:4d}'
                f.write(f'{nucleus_header}\n')
                f.write(f'{col_header}\n')
                for U, fE1 in zip(ond[Z][A]['U'], ond[Z][A]['fE1']):
                    f.write('{:9.3f}   {:.3E}\n'.format(U, fE1))
                f.write(' \n')


def df_to_dict(df):
    if isinstance(df.index, pd.MultiIndex):
        mydf = df.T.copy()
    else:
        mydf = df.copy()
        
    ond = OrderedDict() # ordered_nested_dict
    for Z, A, data_col in mydf.columns:
        if Z not in ond.keys():
            ond[Z] = OrderedDict()
        if A not in ond[Z].keys():
            ond[Z][A] = OrderedDict()
        ond[Z][A][data_col] = tuple(mydf[Z][A][data_col].values)
    return ond


def dict_to_df(ordered_nested_dict):
    reform = {(firstKey, secondKey, thirdKey): values for firstKey, middleDict in ordered_nested_dict.items() for secondKey, innerdict in middleDict.items() for thirdKey, values in innerdict.items()}
    df = pd.DataFrame(reform)
    df = df.T # transpose
    df.index.names=['Z', 'A', None]
    return df.T # transpose back


def atomic_mass_numbers(talys):
    if not isinstance(talys_df, pd.MultiIndex):
        df = talys.T.copy()
    else:
        df = talys.copy()
    return df.index.levels[1]


def replace_table(Z, A, talys, lorvec):
    transpose = False
    if not isinstance(talys.index, pd.MultiIndex):
        df1 = talys.T.copy()
        transpose = True
    else:
        df1 = talys.copy()
    if not isinstance(lorvec.index, pd.MultiIndex):
        df2 = lorvec.T.copy()
    else:
        df2 = lorvec.copy()
    df1.loc[(Z, A, ['U', 'fE1']), :] = df2.loc[(Z, A, ['U', 'fE1']), :]
    return df1.T if transpose else df1

# %%
lorvec_df = lorvec_to_df('ftes_lorvec.out')

talys_dict = fn_to_dict('z050')
talys_df = dict_to_df(talys_dict)

mass_numbers = atomic_mass_numbers(talys_df)
print(f"min(A) = {mass_numbers.min()}, max(A) = {mass_numbers.max()}")

talys_df_new = replace_table(50, 146, talys_df, lorvec_df)

new_talys_dict = df_to_dict(talys_df_new)
dict_to_fn(new_talys_dict, 'newz050')

# %%
! diff z050 newz050
