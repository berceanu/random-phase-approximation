Project using the [signac](https://signac.io) data management framework.

## Usage

First, run the `rpa-aggregation` parent project, see `../README.md`.

Afterwards:

```console
$ python src/animation.py --help
$ python src/dashboard.py run --host 0.0.0.0 --port 5000
```

## Example

```console
$ python src/animation.py --protonNumber 50 --minNeutronNumber 76 --framerate 4.0 --resolution "1920x1080"
```
