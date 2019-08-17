# random-phase-approximation
Visualization framework for microscopic nuclear models.

DEPENDENCIES:

- compiled microscopic model binaries, from `nuclear-codes`
- `TALYS >= 1.9`, with
  - database in `~/src/talys/`
  - binary at `~/bin/talys`

INSTALLATION:

- install **Miniconda** Python distribution
- `$ conda env create -f environment.yml`
- `$ conda activate random-phase-approximation`
- `$ python -m pip install -e mypackage`

**Note:** If you already have an older version of the environment installed, you can remove it via

`$ conda remove --name random-phase-approximation --all`
