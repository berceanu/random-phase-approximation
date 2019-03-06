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
# %autosave 0

# %%
import pandas as pd
import numpy as np
import re
import pprint
from collections import OrderedDict

# %%
! head ftes_lorvec.out

# %%
146 - 50 # N

# %%
# 'energy', 'transition_strength'
df_lorvec = pd.read_csv('ftes_lorvec.out', delim_whitespace=True, comment='#', skip_blank_lines=True,
            header=None, names=['U', 'fE1'])

# %%
df_lorvec = df_lorvec[(df_lorvec.U >= 0.1) & (df_lorvec.U <= 30)] # MeV

# %%
df_lorvec.head()

# %%
every_10 = df_lorvec.iloc[::10, :]
every_10.reset_index(drop=True, inplace=True)
every_10_T = every_10.T

# %%
df = every_10_T
df2 = pd.concat([df], keys=[146], names=['A'])
df3 = pd.concat([df2], keys=[50], names=['Z'])
lorvec_df = df3

# %%



# %%



# %%
stocks = pd.read_csv('http://bit.ly/smallstocks')

# %%
stocks.groupby('Symbol').Close.mean()

# %%
ser = stocks.groupby(['Symbol', 'Date']).Close.mean()

# %%
ser.index

# %%
ser.unstack()

# %%
df = stocks.pivot_table(values='Close', index='Symbol', columns='Date')

# %%
stocks.set_index(['Symbol', 'Date'], inplace=True)

# %%
ser.loc[:, '2016-10-03']

# %%
stocks.index

# %%
stocks.sort_index(inplace=True)

# %%



# %%



# %%
def to_float(iterable):
    return (float(val) for val in iterable)

# %%
class ConfigurationSyntaxError(Exception):
    pass

# %%
# @TODO 
# df_to_dict(df):
    # get dictionary from dataframe X
# @TODO 
# dict_to_fn(ordered_nested_dict, fname):
    # write dict to file 
# @TODO same float formatting
# @TODO multiply by constant to convert e^2fm^2 to barn
# @TODO why missing some A values

# %%
def fn_to_dict(fname):
    z_from_fname = int(''.join(filter(lambda c: not c.isalpha(), fname)))
    with open(fname) as f:
        contents = f.read()
    
    new_line = re.compile('\n[\s\r]+?\n')
    blocks = new_line.split(contents)
    
    assert blocks[-1].strip() == '', "Last line not empty!"
    assert len(blocks[:-1]) == 82, "Not right number of blocks!"
    
    mydict = OrderedDict()
    mydict[z_from_fname] =  OrderedDict()
    
    minA, maxA = 400, 0
    for blk in blocks[:-1]: # except last line
        block = blk.splitlines()
    
        nucleus_header = block[0].split()
        Z, A = (int(val) for val in nucleus_header[1::2])
        if (nucleus_header[0::2] != ['Z=', 'A=']) or (Z != z_from_fname):
            raise ConfigurationSyntaxError('Wrong header inside %s!' % fname)
        if int(A) < minA:
            minA = int(A)
        if int(A) > maxA:
            maxA = int(A)
        
        col_header = block[1].split()
        if col_header[:2] != ['U[MeV]', 'fE1[mb/MeV]']:
            raise ConfigurationSyntaxError('Wrong header inside %s!' % fname)

        columns = (row.split() for row in block[2:])
        c1_vals, c2_vals = zip(*columns)

        d = OrderedDict()
        d[A] = OrderedDict(U=tuple(to_float(c1_vals)),
                         fE1=tuple(to_float(c2_vals)))
        mydict[Z].update(d)
        
    print(f"Amax - Amin = {maxA - minA}, {len(blocks[:-1])} blocks")
    return mydict, minA, maxA

# %%
def dict_to_fn(ordered_nested_dict, fname):
    ond = ordered_nested_dict
    z_from_fname = int(''.join(filter(lambda c: not c.isalpha(), fname)))
    print(z_from_fname)
#     print(ond[z_from_fname])
    nucleus_header = f' Z={z_from_fname:4d} A={90:4d}'
    print(nucleus_header)
    col_header = f'  U[MeV]  fE1[mb/MeV]'
    print(col_header)
    data = '{:9.3f}   {:.3E}'.format(11.100, 6.510E-03)
    print(data)
    
    for Z in ond.keys():
        for A in ond[Z].keys():
            print(Z, A)
            for U, fE1 in zip(ond[Z][A]['U'], ond[Z][A]['fE1']):
                print(U, fE1)
    
    with open(fname, "w") as f:
        f.write('This is not a test.\n')



# %%
t1 = (1,2,3)
t2 = (4,5,6)

for a, b in zip(t1, t2):
    print(a, b)

# %%
md, a, b = fn_to_dict('z050')
print(f"Amin = {a}, Amax = {b}")

# %%
dict_to_fn(md, 'newz050')

# %%
md_tst = {'50': {'100': {'col1': (0.100,
                              0.200,
                              0.300,
                              0.400),
                     'col2': (0.1359,
                              0.14329,
                              0.151455,
                              0.160519)},
             '101': {'col1': (0.100,
                              0.200,
                              0.300,
                              0.400),
                     'col2': (6.510E-03,
                              7.011E-03,
                              7.553E-03,
                              8.134E-03)}
            }
     }

# %%
def dict_to_df(ordered_nested_dict):
    reform = {(firstKey, secondKey, thirdKey): values for firstKey, middleDict in ordered_nested_dict.items() for secondKey, innerdict in middleDict.items() for thirdKey, values in innerdict.items()}
    df = pd.DataFrame(reform)
    df = df.T # transpose
    df.index.names=['Z', 'A', None]
    return df

# %%
# pprint.pprint(md)

# %%
df = dict_to_df(md)
df.head()

# %%
df.loc[(50, 146, ['U', 'fE1']), :]

# %%
lorvec_df.loc[(50, 146, ['U', 'fE1']), :]

# %%
df.loc[(50, 146, ['U', 'fE1']), :] = lorvec_df.loc[(50, 146, ['U', 'fE1']), :]

# %%
df.loc[(50, 146, ['U', 'fE1']), :]

# %%
md_tst = {'50': {'100': {'col1': (0.100,
                              0.200,
                              0.300,
                              0.400),
                     'col2': (0.1359,
                              0.14329,
                              0.151455,
                              0.160519)},
             '101': {'col1': (0.100,
                              0.200,
                              0.300,
                              0.400),
                     'col2': (6.510E-03,
                              7.011E-03,
                              7.553E-03,
                              8.134E-03)}
            }
     }

# %%
df_tst = dict_to_df(md_tst)
df_tst

# %%
df_tst = df_tst.T
pprint.pprint(df_tst.to_dict('list')) # dict is OK
df_tst = df_tst.T
print()
print(df_tst.index) # index is OK

# %%
table = df_tst.loc[('50', '100', ['col1', 'col2']), :]
table

# %%
s = df_tst.loc[('50', '100', 'col1'), :]
s


# %%



# %%



# %%
stocks

# %%
stocks.loc[('AAPL', '2016-10-03'), :] # rows, columns
stocks.loc[('AAPL', '2016-10-03'), 'Close']
stocks.loc[(['AAPL', 'MSFT'], '2016-10-03'), :]
stocks.loc[(['AAPL', 'MSFT'], '2016-10-03'), 'Close']
stocks.loc[('AAPL', ['2016-10-03', '2016-10-04']), 'Close']
stocks.loc[(slice(None), ['2016-10-03', '2016-10-04']), :]

# %%



# %%



# %%
md = {'50': {'100': {'col1': ('0.100',
                              '0.200',
                              '0.300',
                              '0.400'),
                     'col2': ('6.263E-03',
                              '6.746E-03',
                              '7.266E-03',
                              '7.825E-03')},
             '101': {'col1': ('0.100',
                              '0.200',
                              '0.300',
                              '0.400'),
                     'col2': ('6.510E-03',
                              '7.011E-03',
                              '7.533E-03',
                              '8.134E-03')}
            }
     }

# %%
reform = {(firstKey, secondKey, thirdKey): values for firstKey, middleDict in md.items() for secondKey, innerdict in middleDict.items() for thirdKey, values in innerdict.items()}

# %%
df = pd.DataFrame(reform)

# %%
df

# %%
md2={}
for i in df.columns:
    if i[0] not in md2.keys():
        md2[i[0]]={}
    if i[1] not in md2[i[0]].keys():
        md2[i[0]][i[1]]={}
    md2[i[0]][i[1]][i[2]]=tuple(df[i[0]][i[1]][i[2]].values)

# %%
pprint.pprint(md2)

# %%
md2 == md

# %%


