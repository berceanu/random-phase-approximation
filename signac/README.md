# mock-signac-proj
Test project using the [signac](https://signac.io) data management framework.

`bin` contains the mock executables: `dish.sh` (for ground state calculation) and `ztes.sh` (for excited state calculation)
"mock" means the original FORTRAN and C++ codes were replaced by `bash` scripts which pretend to do the calculation and output the same filenames, but finish in 5s each

## Usage

```console
# first time only, clears workspace!
$ ./init.sh
```

```console
$ python3 src/init.py
$ python3 src/project.py run --parallel
$ python3 src/project.py status --pretty --full --stack
$ python3 src/dashboard.py run --host 0.0.0.0 --port 9999
```

```console
$ rsync -r -a -v -e ssh --delete P6000:~/Development/random-phase-approximation/signac/workspace/ workspace/
```
