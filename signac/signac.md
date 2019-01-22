```python
@Project.operation
@cmd
@Project.post.isfile('rpa.wel')
def run_this_first(job):
    return "fortran_executable {ws}".format(ws=job.workspace())

@Project.operation
@cmd
@Project.post.after(run_this_first):
def run_this_second(job):
    return "your command > {}".format(job.fn('outputfile.txt'))
    return "matlab -r 'prog {job.sp.foo} {job.sp.bar}' > {job.ws}/output.txt"
```

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
```

```python
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
- the `volume_computed()` function is a condition function. It's also decorated as a label-function, which means it's going to show up in the status summary, but not every condition function has to be a label function
- your condition functions can be arbitrary python functions that take the job argument as first argument, you don't have to try to cramp everything into the decorator

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
