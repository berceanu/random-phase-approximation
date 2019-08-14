# TODO

- [ ] move `C++`/`FORTRAN` sources to separate private repo
    - [ ] keep only the compiled binaries, in LFS
    - [ ] make `random-phase-approximation` public

- [ ] use shorter dir names, such as `anim`, `agg`, `temp`, `neutr`
    - [ ] replace `signac/projects/` by `proj/`
    - [ ] check/update code paths

- [ ] update `talys/` (sub-)projects with the new input/insights
    - [ ] run `hfb_qrpa`
        - [ ] update `input.txt` and `init.py`
        - [ ] add output to LFS
        - [ ] sync vps repo
        - [ ] include in webpage
    - [ ] do the same for the remaining projects


- [ ] run `rpa/` projects
    - [ ] update `init.py` to use only `Sn` isotopes
    - [ ] update `agg` and `anim` to plot only *isovector*(?), no *vlines*
    - [ ] run 
    - [ ] update LFS `workspace/`

- [ ] aggregate over neutron numbers
    - [ ] create `rpa/agg/neutr`
    - [ ] rename old aggregation to `rpa/agg/temp`
    - [ ] test plot recipe from gitter/matplotlib
        - [ ] extract/generate plotting data (21 curves)

## Links

- [cross validated](https://stats.stackexchange.com/questions/422009/best-way-to-plot-multiple-similar-lines/422067#422067)
- 
![](https://i.imgur.com/wAcmc48.png)


- [kde ridgeplot](https://seaborn.pydata.org/examples/kde_ridgeplot.html)

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Create the data
rs = np.random.RandomState(1979)
x = rs.randn(500)
g = np.tile(list("ABCDEFGHIJ"), 50)
df = pd.DataFrame(dict(x=x, g=g))
m = df.g.map(ord)
df["x"] += m

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=15, height=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "x", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "x")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)

```

![](https://i.imgur.com/14TXqOY.png)


- [joypy](https://github.com/sbebo/joypy)

![](https://i.imgur.com/VJFPQei.png)


- [frequency trails](http://www.brendangregg.com/FrequencyTrails/intro.html)

![](https://i.imgur.com/Stk6AHY.png)



## Gitter Code

```python
for j in range(nplots):
    ax.plot(x, y[j] + j * dy); 
    ax.axhline(j * dy)
```

You can also do `x+dx * j` if you like, I find that harder to parse.
You can also just do a `pcolormesh(x, np.range(nplots), y)`.
