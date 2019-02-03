
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
df = pd.read_csv('ftes_excvec.out', delim_whitespace=True, comment='#', skip_blank_lines=True,
                     header=None, names=['energy', 'transition_strength'])

#%%
df = df[(df.energy < 30) & (df.transition_strength > 0.1)]



#%%
fig, ax = plt.subplots()
ax.vlines(df.energy, 0., df.transition_strength, colors='red')
ax.set_title("Isovector dipole transition strength distribution")
ax.set(
    # xlim=[0, 30],
    # ylim=[0, 4.5],
    ylabel=r"$R \; (e^2fm^2/MeV)$",
    xlabel="E (MeV)",
);


#%%
def transition_energies(df):
    for idx in df.index:
        en = df.loc[idx, 'energy']
        yield float("{0:.2f}".format(en))




#%%
tr_en = transition_energies(df)
next(tr_en)

#%%
next(tr_en)