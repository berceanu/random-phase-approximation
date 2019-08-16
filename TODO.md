# TODO

- [ ] move `C++`/`FORTRAN` sources to separate private repo, `RMF-RQRPA`
    - [ ] keep only the compiled binaries, in LFS
    - [ ] make `random-phase-approximation` public

- [ ] use shorter dir names, such as `anim`, `agg`, `temp`, `neutr`
    - [ ] replace `signac/projects/` by `proj/`
    - [ ] rename `random-phase-approximation` to `rpa` on vps instance
    - [ ] check/update code paths

- [ ] remove `util/`, `tests/`, `rsync/`, `cmake_fortran` etc

- [ ] update weblinks to reflect tree structure of subprojects

- [ ] update `talys/` (sub-)projects with the new input/insights
    - [ ] run `hfb_qrpa`
        - [ ] update `input.txt` and `init.py`
        - [ ] use same energy grid for `rpa/` and `talys/`
        - [ ] add output to LFS
        - [ ] sync vps repo
        - [ ] add link to webpage
    - [ ] do the same for the remaining (sub-)projects


- [ ] run `rpa/` projects
    - [ ] update `init.py` to use only `Sn` isotopes
    - [ ] update `agg` and `anim` to plot only *isovector*, no *vlines*
    - [ ] run 
    - [ ] update LFS `workspace/`
    - [ ] sync vps instance repo

- [ ] aggregation via `pandas`
    - [ ] replace `agg` and `anim` with global pandas dataframe
        - [ ] create plotting functions that act on the df
    - [ ] test plot recipe from gitter/matplotlib
        - [ ] extract/generate plotting data (21 curves)
        - [ ] try using a Pandas dataframe for the aggregation
        - [ ] find out what aggregation over variable v means
        - [ ] try aggregation over temperature and neutron number in same plot

## Aggregation via `pandas`

Create `proj/df` `signac` project, whose goal is it create a single data structure, namely a `pandas` dataframe, that contains all the project output data. This dataframe can then be operated on by user-defined functions, data in it can be aggregated and plotted interactively in `jupyter notebooks`.


### Sample data to be included in the overall df

- consider `lorentzian` electric dipole strengths only!
- consider `isovector` data only!
- consider only the tin (Sn) isotopes, `proton_number = 50`!
- use same energy grid for `C++/FORTRAN` codes and `TALYS`!

```
ztes_lorvec.out: T = 0.0
ftes_lorvec.out: T = 0.5, 1.0, 2.0
```
- see `rpa/aggregation/src/aggregation.py:109`


```
sample z/ftes_lorvec.out file
```
```
#RPA-results:
#Nucleus: SN 132
#Excitation: 1 -
...
#Real part: -1.797451e-13

#Parameterset: DD-ME2
#natural parity: yes
#Isovector result:

#width: 1.000000e+00
#maximum value: 9.166250e+00
#at energy: 1.523000e+01
0.000000e+00	0.000000e+00
1.000000e-02	2.881808e-02
```

- Q: where do the values in the left column come from? Check input files.

- [ ] add samples/code links for `ncap` and `xsec`

### df structure

|model| N  | T_9 |ncap |E_n | R | xsec  |
|-----|--- |---- |-----| ---| --|-------|
| A   | 76 | 0.0 |     | 0  | 1 | 1     |
| A   | 76 | ..  |     | .. | ..| ..    |
| A   | 76 | 0.0 |     | 30 | 5 | 0.5   |
| A   | 76 | 0.5 |     | 0  | 2 | 0.2   |
| A   | 76 | ..  |     | .. | ..| ..    |
| A   | 76 | 2.0 |     | 30 | 7 | 0.7   |
| A   | 78 | 0.0 |     | 0  | 3 | 0.3   |

`model`: `A`/`B`

`A` = "YIFEI" (T-dep. RPA)

`B` = "TALYS" (HFB+QRPA)

```python
units["model"] = None
units["N"] = None
units["T_9"] = "[MeV]"
units["ncap"] = r"[s${}^{-1}$cm${}^{3}$mol${}^{-1}$]"
units["E_n"] = "[MeV]"
units["R"] = r"[e${}^{2}$ fm${}^{2}$/MeV]"
units["xsec"] = "[mb]"
```

## Links

- [cross validated](https://stats.stackexchange.com/questions/422009/best-way-to-plot-multiple-similar-lines/422067#422067)

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
