# TODO

- [ ] oscillations
    - [ ] create talys subproject `hfb_qrpa_no_micro`
    - [ ] find isotope with maximal oscillations
    - [ ] plot on same graph with `hfb_qrpa`

## Aggregation via `pandas`

- [ ] aggregation via `pandas`
    - [ ] replace `agg` and `anim` with global pandas dataframe
        - [ ] create plotting functions that act on the df
    - [ ] test plot recipe from gitter/matplotlib
        - [ ] extract/generate plotting data (21 curves)
        - [ ] try aggregation over temperature and neutron number in same plot

Create `proj/df` `signac` project, whose goal is it create a single data structure, namely a `pandas` dataframe, that contains all the project output data. This dataframe can then be operated on by user-defined functions, data in it can be aggregated and plotted interactively in `jupyter notebooks`.


### Sample data to be included in the overall df

- consider `lorentzian` electric dipole strengths only!
- consider `isovector` data only!
- consider only the tin (Sn) isotopes, `proton_number = 50`!


```
ztes_lorvec.out: T = 0.0
ftes_lorvec.out: T = 0.5, 1.0, 2.0
```


```
sample [zf]tes_lorvec.out file
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
- the first column (energies) goes from `0` up to `50` MeV in increments of `0.01` MeV: `np.linspace(0, 50, 5001, retstep=True)`


- `TALYS` contains the tabulated microscopic gamma-ray strength functions computed according to HF-QRPA [see manual, page 143]:
```
sample structure/gamma/hfb/Sn.psf
```
```
 Z=  50 A=  90
  U[MeV]  fE1[mb/MeV]
    0.100   6.291E-03
    0.200   6.776E-03
    .....   .........
    
 Z=  50 A=  91
  U[MeV]  fE1[mb/MeV]
    0.100   6.350E-03
    0.200   6.840E-03
    .....   .........
 ...
```
- the energy axis `U` goes from `0.1` up to `30` MeV in increments of `0.1` MeV: `np.linspace(0.1, 30, 300, retstep=True)`
- the file contains tin (Z=`50`) isotopes with masses from A=`90` to A=`178`, with a gap from A = `171` to A = `177`; in total there are 82 isotopes in this file

The `rpa` project workflow for generating each job's photon strength function (`.psf`) file, which is then passed to `TALYS`, is as follows:

```flow
st=>start: structure/gamma/hfb/Sn.psf
e=>end: talys_df
op=>operation: talys.api.fn_to_dict()
op2=>operation: talys.api.dict_to_df()
st->op->op2->e
```

```flow
st=>start: [zf]tes_lorvec.out
e=>end: lorvec_df
op=>operation: talys.api.lorvec_to_df()
st->op->e
```

```flow
st=>start: talys.api.replace_table(talys_df, lorvec_df)
e=>end: ${job._id}/Sn.psf
op=>operation: talys.api.df_to_dict()
op2=>operation: talys.api.dict_to_fn()

st->op->op2->e
```

Of particular interest here is the function `mypackage.talys.api.lorvec_to_df()`, which has the following diagram:

```flow
st=>start: read columns E and R from [zf]tes_lorvec.out
op=>operation: R = R * 4.022 mb / (e^2 * fm^2)
op2=>operation: select E between 0.1 and 30 MeV
op3=>operation: keep only every 10th row
e=>end: return dataframe

st->op->op2->op3->e
```

Reading the columns from `[zf]tes_lorvec.out` is achieved by

```python
df_lorvec = pd.read_csv(
    fname,
    delim_whitespace=True,
    comment="#",
    skip_blank_lines=True,
    header=None,
    names=["U", "fE1"],
)
```

```
sample astrorate.g
```
```
# Reaction rate for 139Sn(n,g)
#    T       Rate       MACS
  0.0001 6.09702E+05 6.09702E+05
  0.0005 4.01579E+05 4.01579E+05
  ...... ........... ...........
  9.0000 8.01139E+02 8.01139E+02
 10.0000 2.96834E+02 2.96834E+02 
```

```
sample rp050140.tot
```
```
# n + 139Sn: Production of 140Sn - Total
# Q-value    = 3.16732E+00 mass= 139.963146
# E-threshold= 0.00000E+00
# # energies =    88
#     E          xs
 1.00000E-11 1.87949E+03
 2.53000E-08 3.73663E+01
 ........... ...........
 2.90000E+01 1.05665E-01
 3.00000E+01 9.39864E-02
```
- the energy grid `E` is given as an input file, `n0-30.grid`


### df structure

|model| N  | T   |Rate |U   |fE1| xs    |
|-----|--- |---- |-----| ---| --|-------|
| A   | 76 | 0.0 |     | 0  | 1 | 1     |
| A   | 76 | ..  |     | .. | ..| ..    |
| A   | 76 | 0.0 |     | 30 | 5 | 0.5   |
| A   | 76 | 0.5 |     | 0  | 2 | 0.2   |
| A   | 76 | ..  |     | .. | ..| ..    |
| A   | 76 | 2.0 |     | 30 | 7 | 0.7   |
| A   | 78 | 0.0 |     | 0  | 3 | 0.3   |

`model`: `A`/`B`/`C`/`D`/`E`


- T = 0 gr state: `RHB`
- T > 0 gr state: `FTRMF`
- T =0 ex state: `QRPA`
- T > 0 ex state: `FTRPA`
- TALYS: `HF-QRPA`



```python
units["model"] = None
units["N"] = None

# temperature
units["T"] = "[MeV]"

# # (n,g) reaction rate
units["Rate"] = r"[s${}^{-1}$cm${}^{3}$mol${}^{-1}$]"

units["U"] = "[MeV]"
units["fE1"] = "[mb/MeV]"
units["xs"] = "[mb]"
```

- downsample Yifei's energy grid `E` to `TALYS`'s  `U`
- convert Yifei's transition strength `R` [e${}^{2}$ fm${}^{2}$/MeV] to `fE1` [mb/MeV]

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

