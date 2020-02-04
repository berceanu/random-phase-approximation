# TODO


## Aggregation via `pandas`


### Sample data to be included in the overall df

- consider `lorentzian` electric dipole strengths only!
- consider `isovector` data only!
- [x] consider only the tin (Sn) isotopes, `proton_number = 50`!


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

| proton_number | neutron_number | mass_number | model | temperature | excitation_energy | neutron_energy | strength_function_fm | strength_function_mb | cross_section | capture_rate |
| ------------- | -------------- | ----------- | ----- | ----------- | ----------------- | -------------- | -------------------- | -------------------- | ------------- | ------------ |



| temperature | nuclear state | model |
| ----------- | ------------- | ----- |
| 0           |  ground       | RHB   |
| > 0         |  ground       | FTRMF |
| 0           |  excited      | QRPA  |
| > 0         |  excited      | FTRPA |


- TALYS: `HF-QRPA`?

## Final plots

### One isotope(reaction) per row, all tempeatures
<!-- ![one isotope per row](https://i.imgur.com/N387UZa.png) -->

### One temperature per row, all isotopes
<!-- ![one temperature per row](https://i.imgur.com/HlsNRnn.png) -->

## Workflow

Step 0 involves building the required dataframe which should hold everything needed below.

1. Select `niso` isotopes, eg. `isotopes = (76, 86, 96)`, `niso = 3` and a set of `ntemp` temperatures, eg. `temperatures = (0.0, 1.0, 2.0)`, `ntemp = 3`
2. For each isotope in `isotopes`, plot one figure with `ntemp` curves, showing all the `temperatures`; each figure depicts the variation of the electric dipole transition strength `R` [e${}^{2}$ fm${}^{2}$/MeV] vs `E` [MeV]; `niso` figures total
3. For each temperature in `temperatures`, plot one figure with `niso` curves, showing all the `isotopes`; each figure depicts the variation of the electric dipole transition strength `R` [e${}^{2}$ fm${}^{2}$/MeV] vs `E` [MeV]; `ntemp` figures total
4. Repeat steps 2&3, after converting the transition strength `R` [e${}^{2}$ fm${}^{2}$/MeV] to `fE1` [mb/MeV];
5. Repeat steps 2-4, for the neutron production `cross-section` [mb] instead of `fE1` [mb/MeV];
6. Plot the neutron `capture rate` versus mass number `A`, resulting in one figure with `ntemp` curves;
7. Plot the neutron `capture rate` versus temperature `T`, resulting in one figure with `niso` curves; the temperature axis only has `ntemp` points;

### Notes

- each plot should take a `type` argument, with possible values `lin-lin`, `log-log`, `log-lin` (log on Y axis), `lin-log` (log on X axis)
- each plot should take the limits of the energy axis, defaulting to `[0.1, 10]` MeV
- each plot should have an optional `include_talys` argument, defaulting to `False`
- each plot should operate on (and return) `Axes` instances
- add model to pcolormesh plot

## Finalize plots

- [ ] use different symbols: triangle, square etc (not just circles)
- [ ] Q about `TALYS` result: why neutron capture rate is decreasing with increasing temperature?
- [ ] use A instead of N for Neutron capture rate plot
- [ ] use N = number instead of just number
- [ ] use ${}^{A}Sn$ instead of N for legends
- [ ] merge `df-merger` branch into `master`
- [ ] create new branch for new neutron capture figure

1.  Do the calculations of neutron capture (NC) rates at T=1, 2 MeV but with E1
    strength function at T=0 MeV from RHB+QRPA.  Then Plot them on the same
    figure of NC rates, and remove T=0.5 MeV result.

2.  Do the analysis of ph transition components for some low-lying states of
    N=76, 86, 96.  How to select these low-lying states:  Below E=10 MeV, find
    one or two discrete states with highest transition strength.

3.  Add the figure of E1 strength and cross section at T=0, 1 and 2 MeV.  In
    each panel of the figure, plot 3 isotopes of N=76, 86 96.

4. Improve the format of  E1 strength and cross section figure.  (1) Enlarge
   all the writings. (2). Put nucleus symbols. (3) Adjust the height-width
   ratio.


