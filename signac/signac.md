```python
@Project.operation
@cmd
@Project.post.isfile('rpa.wel')
def run_this_first(job):
    return f"fortran_executable {job.workspace()}"

@Project.operation
@cmd
@Project.post.after(run_this_first):
def run_this_second(job):
    return f"cpp_executable {job.sp.a} {job.sp.b} > {job.fn('output.txt')}"
```

- `post.after(run_this_first)` reuses all of `run_this_first()`'s post conditions as pre-conditions for the `run_this_second()` operation
- `job.fn('output.txt')` equiv to `os.path.join(job.workspace(), 'output.txt')`

```python
@Project.label
def volume_computed(job):
    return os.path.isfile("volume.txt")

@Project.operation
@Project.post(volume_computed)
def compute_volume(job):
    volume = job.sp.N * job.sp.kT / job.sp.p
    with open(job.fn('volume.txt'), 'w') as file:
        file.write(str(volume) + '\n')

@Project.operation
@Project.pre(volume_computed)
@Project.post.isfile("data.json")
def store_volume_in_json_file(job):
    with open(job.fn("volume.txt")) as textfile:
        with open(job.fn("data.json"), "w") as jsonfile:
            data = {"volume": float(textfile.read())}
            jsonfile.write(json.dumps(data) + "\n")
```

- the `volume_computed()` function is a condition function. It's also decorated as a label-function, which means it's going to show up in the status summary, but not every condition function has to be a label function
- your condition functions can be arbitrary python functions that take the job argument as first argument, you don't have to try to cramp everything into the decorator
- replacing the `pre(volume_computed)` condition with `pre.after(compute_volume)`, which is a short-cut to reuse all of `compute_volume()`’s post-conditions as pre-conditions for the `store_volume_in_json_file()` operation

```python
# for --load-matrix case

@Project.operation
@Project.post(data_available)
def look_for_previous_results(job):
    project = get_project()
    previous_results = project.find_jobs({'a': job.sp.a, 'b': job.sp.b})
    if len(previous_results):
        # copy previous results
        job.doc.need_full_calculation = False
    else:
        job.doc.need_full_calculation = True

@Project.operation
@Project.pre.true('need_full_calculation')
@Project.post(data_available)
def full_calculation(job):
    # code for full calculation
```

- operation function is eligible for execution if all pre-conditions are met, at least one post-condition is not met and the operation is not currently submitted or running
- operation is considered completed when all its post conditions are met, and it is up to the user to define those post conditions
- cheap conditions should be placed before expensive conditions; the same holds for post-conditions


## OTHER

- you can use the `-d` or `--detailed` option to show it on a per-job level
- you need to add the `--progress` option for that
- if you run locally a simple `--parallel` appended to the run command will invoke parallel execution
- [`_read_last_line`](https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file/18603065#18603065) sounds like it would do the trick.

## USAGE
```console
$ python src/init.py
$ python src/project.py run
```
