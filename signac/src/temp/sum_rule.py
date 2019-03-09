# -*- coding: utf-8 -*-
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
import math
import signac
import pandas as pd
import mypackage.code_api as code_api

# %%
code = code_api.NameMapping()
rpa = signac.get_project()
print(rpa.root_directory())

selection = rpa.find_jobs({'proton_number': 50, 'neutron_number': 82,
                           'temperature': 0.})

# %%
50 + 82

# %%
myjob = next(selection)

# %%
myjob._id

# %% [markdown]
# https://en.wikipedia.org/wiki/Elementary_charge
#
# In SI, we have the relation:
# $$e^2 = 2 \epsilon_0 \alpha h c = 4 \pi \epsilon_0 \alpha \hbar c$$
#
# The conversion factor for charge from SI to Gaussian units is $q_{\text{SI}} = q_{\text{G}} \sqrt{4 \pi \epsilon_{0}^{\text{SI}}}$
# https://en.wikipedia.org/wiki/Gaussian_units
#
# Therefore we get
# $$ e_{\text{G}}^2 = \alpha \hbar_{\text{G}} c$$

# %%
α = 7.297352570e-03 # fine structure constant

ħ_G = 1.0545716e-27 #erg⋅s
erg_to_MeV = 624150.91 # MeV
ħ_MeV = ħ_G * erg_to_MeV # MeV⋅s

c = 2.9979246e+23 # fm/s

# %%
ħ_MeVc = ħ_MeV * c
print(f'ħ_G c = {ħ_MeVc} MeV⋅fm')

# %%
e_sq_G = α * ħ_MeVc # MeV⋅fm
print(f'e^2_G = {e_sq_G} MeV⋅fm')

# %%
u_factor = 10 * 16 * math.pi**3 * α / 9 # mb / (e^2 * fm^2)
print('{:.6f}'.format(u_factor))

# %% [markdown]
# https://doi.org/10.1016/j.nuclphysa.2009.03.009
#
# From Eq. (11) in this paper, we get a factor of 
# $$\frac{16\pi^3e^2_G}{9\hbar c} = \frac{16\pi^3 \alpha}{9}$$
# $$f_g = \frac{16\pi^3 \alpha}{9} \times S\left[\frac{\text{fm}^2}{\text{MeV}}\right] = 0.402247 \times S\left[\frac{\text{fm}^2}{\text{MeV}}\right] = 4.022466 \times S\left[\frac{\text{mb}}{\text{MeV}}\right] $$

# %%
lorvec_fn = myjob.fn(code.out_file(temp='zero', 
                        skalvec='isovector', lorexc='lorentzian'))
excvec_fn = myjob.fn(code.out_file(temp='zero', 
                        skalvec='isovector', lorexc='excitation'))

# %%
# ! head -n 25 {lorvec_fn} 
! head -n 20 {excvec_fn}

# %%
def sum_rule(fname, 
             cutoff_en=None, # MeV
             unit_factor=u_factor, # mb / (e^2 * fm^2)
            ):
    df = pd.read_csv(fname, delim_whitespace=True, comment='#', skip_blank_lines=True,
            header=None, names=['U', 'fE1']) # Mev, e^2*fm^2/MeV
    if cutoff_en:
        df = df[(df.U <= cutoff_en)] # MeV
    df['fE1s'] = df['fE1'].apply(lambda x: x * unit_factor) # mb/MeV
    df['UxfE1s'] = df.apply(lambda row: (row['U'] * row['fE1s']),
                                   axis=1)
    total_sum = df['UxfE1s'].sum()
    return df, total_sum

# %%
lorvec_df, lorvec_sum = sum_rule(lorvec_fn)
excvec_df, excvec_sum = sum_rule(excvec_fn)
print(f'Lorentzian isovector sum rule: {lorvec_sum:.3f} mb⋅MeV.')
print(f'Excitation isovector sum rule: {excvec_sum:.3f} mb⋅MeV.')
print(f'Experimentally measured value is 2330 ± 590 mb⋅MeV.') 

# %%
lorvec_df.head(20)

# %%
excvec_df.tail()

# %%

