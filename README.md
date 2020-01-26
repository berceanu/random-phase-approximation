# random-phase-approximation
Execution/visualization framework for microscopic nuclear models, based on [signac](https://signac.io/).

DEPENDENCIES:

- compiled microscopic nuclear model executables, from `nuclear-codes`
  - the executables should be placed under `bin/`
- `TALYS >= 1.9`, with
  - database in `~/src/talys/`
  - binary at `~/bin/talys`

INSTALLATION:

- install **Miniconda** Python distribution, then

```console
$ conda env create -f environment.yml
$ conda activate random-phase-approximation
$ python -m pip install -e mypackage dataframe figstyle
```

For interactive plots inside **jupyter lab**:

```console
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
$ jupyter labextension install jupyter-matplotlib
```

**Note:** If you already have an older version of the environment installed, you can remove it via

```console
$ conda remove --name random-phase-approximation --all
```

or update via

```console
$ conda env update -f environment.yml
```
