#%%
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from IPython.display import Image
from IPython.core.display import HTML 

#%%
df = pd.read_csv('src/temp/ftes_excvec.out', delim_whitespace=True, comment='#', skip_blank_lines=True,
                     header=None, names=['energy', 'transition_strength'])

#%%
df = df[(df.energy < 30) & (df.transition_strength > 0.1)]

#%%
!pwd


#%%
fig = Figure(figsize=(10, 6))
canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)

ax.vlines(df.energy, 0., df.transition_strength, colors='red')
ax.set_title("Isovector dipole transition strength distribution")
ax.set(
    # xlim=[0, 30],
    # ylim=[0, 4.5],
    ylabel=r"$R \; (e^2fm^2/MeV)$",
    xlabel="E (MeV)",
)
canvas.print_figure('strength.png')
Image(filename = "strength.png", width=100, height=100)


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
