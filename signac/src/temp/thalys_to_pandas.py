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

# %%
df = pd.read_csv('ftes_lorvec.out', delim_whitespace=True, comment='#', skip_blank_lines=True,
            header=None, names=['energy', 'transition_strength'])

# %%
df = df[(df.energy >= 0.1) & (df.energy <= 30)] # MeV

# %%
df

# %%
df.iloc[::10, :]

# %%


# %%
user_dict = {12: {'Category 1': {'att_1': 1, 'att_2': 'whatever'},
                  'Category 2': {'att_1': 23, 'att_2': 'another'}},
             15: {'Category 1': {'att_1': 10, 'att_2': 'foo'},
                  'Category 2': {'att_1': 30, 'att_2': 'bar'}}}

# %%


# %%


# %%
user_dict = {12: {'Category 1': {'att_1': 1, 'att_2': 'whatever'},
                  'Category 2': {'att_1': 23, 'att_2': 'another'}},
             15: {'Category 1': {'att_1': 10, 'att_2': 'foo'},
                  'Category 2': {'att_1': 30, 'att_2': 'bar'}}}

# %%
df = pd.DataFrame.from_dict({(i,j): user_dict[i][j] 
                           for i in user_dict.keys() 
                           for j in user_dict[i].keys()},
                       orient='index')

# %%
df.index

# %%
arrays = [['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
         ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]

# %%
tuples = list(zip(*arrays))

# %%
tuples

# %%
index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])

# %%
index

# %%
s = pd.Series(np.random.randn(8), index=index)


# %%
import numpy as np

# %%
s

# %%
s.index

# %%
s.loc['baz']

# %%
import pandas as pd

# %%
stocks = pd.read_csv('http://bit.ly/smallstocks')

# %%
stocks

# %%
stocks.index

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
df

# %%
ser

# %%
ser.loc['AAPL']

# %%
ser.loc['AAPL', '2016-10-03']

# %%
ser.loc[:, '2016-10-03']

# %%
df.loc['AAPL']

# %%
df.loc[:, '2016-10-03']

# %%
stocks.set_index(['Symbol', 'Date'], inplace=True)

# %%
stocks

# %%
stocks.index

# %%
stocks.sort_index(inplace=True)

# %%
stocks

# %%
stocks.loc['AAPL']

# %%
stocks.loc[('AAPL', '2016-10-03'), :] # rows, columns

# %%
stocks.loc[('AAPL', '2016-10-03'), 'Close']

# %%
stocks.loc[(['AAPL', 'MSFT'], '2016-10-03'), :]

# %%
stocks.loc[(['AAPL', 'MSFT'], '2016-10-03'), 'Close']

# %%
stocks.loc[('AAPL', ['2016-10-03', '2016-10-04']), 'Close']

# %%
stocks.loc[(slice(None), ['2016-10-03', '2016-10-04']), :]

# %%
both = pd.merge

# %%


# %%
 Z=  50 A=  90
  U[MeV]  fE1[mb/MeV]
    0.100   6.291E-03
    0.200   6.776E-03
    0.300   7.300E-03

  Z=  50 A=  91
  U[MeV]  fE1[mb/MeV]
    0.100   6.350E-03
    0.200   6.840E-03
    0.300   7.369E-03
    0.400   7.937E-03

# %%
{50: {90: {}, 91: {}}}

# %%
mydict = {50: {90: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]},
               91: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]}},
          51: {90: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]},
               91: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]}}}

# %%
{(i,j): user_dict[i][j] 
                           for i in user_dict.keys() 
                           for j in user_dict[i].keys()}

# %%
df = pd.DataFrame.from_dict({(i,j): user_dict[i][j] 
                           for i in user_dict.keys() 
                           for j in user_dict[i].keys()},
                       orient='index')

# %%
df.index

# %%
df

# %%
df = pd.DataFrame.from_dict(user_dict)

# %%
df

# %%
pd.DataFrame.from_dict?

# %%
import re

# %%
new_line = re.compile('\n[\s\r]+?\n')

# %%
contents = open('z050').read()

# %%
blocks = new_line.split(contents)

# %%
len(blocks)

# %%
class ConfigurationSyntaxError(Exception):
    pass

# %%
blocks[2].splitlines()

# %%
raise ConfigurationSyntaxError('blas')

# %%
tst = {'50': {}}

# %%
mydict = {50: {90: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]},
               91: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]}},
          51: {90: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]},
               91: {'U': [0.100, 0.200, 29.900, 30.000], 'fE1': [6.291E-03, 6.776E-03, 8.220E-01, 8.110E-01]}}}

# %%
def fn_to_dict(fname):
    z_from_fname = int(''.join(filter(lambda c: not c.isalpha(), fname)))
    contents = open(fname).read()
    
    new_line = re.compile('\n[\s\r]+?\n')
    blocks = new_line.split(contents)
    
    assert len(blocks[:-1]) == 82, "Not right number of blocks!"
    assert blocks[-1].strip() == '', "Last line not empty!"
    
    mydict = {str(z_from_fname): {}}
    minA, maxA = 400, 0
    for blk in blocks[:-1]: # except last line
        block = blk.splitlines()
    
        nucleus_header = block[0].split()
        Z, A = nucleus_header[1::2]
        if (nucleus_header[0::2] != ['Z=', 'A=']) or (int(Z) != z_from_fname):
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

        d = {A: {'U': c1_vals, 'fE1': c2_vals}}
        mydict[Z].update(d)
        
    print(f"Amax - Amin = {maxA - minA}, {len(blocks[:-1])} blocks")
    return mydict, minA, maxA

# %%
md, a, b = fn_to_dict('z050')
print(f"Amin = {a}, Amax = {b}")

# %%
pprint.pprint(md)

# %%
b

# %%
b - a

# %%
df = pd.DataFrame.from_dict({(i,j): md[i][j][v] for i in md.keys() for j in md[i].keys() for v in md[i][j]}, orient='index')

# %%
mydict = {(i,j): md[i][j][v] for i in md.keys() for j in md[i].keys() for v in md[i][j]}

# %%
import pprint

# %%
pprint.pprint(mydict)

# %%
Z, A = block[0].split()[1], block[0].split()[3]
print(f"(Z, A) = ({Z}, {A})")

# %%
col1, col2 = block[1].split()[0].split('[')[0], block[1].split()[1].split('[')[0]
print(f"(col1, col2) = ({col1}, {col2})")

# %%
myd = {(i,j): md[i][j][v] for i in md.keys() for j in md[i].keys() for v in md[i][j]}

# %%
df = pd.DataFrame.from_dict({(i,j): myd[i][j] for i in myd.keys() for j in myd[i].keys()}, orient='index')

# %%
df

# %%
print(df.to_string())

# %%
df

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
                        '7.553E-03',
                        '8.134E-03')}
             }
}

# %%
md1 = {(i,j): md[i][j][v] for i in md.keys() for j in md[i].keys() for v in md[i][j]}

# %%

