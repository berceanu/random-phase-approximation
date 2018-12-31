```
% prog.m
function []=prog(arg1, arg2)

display(arg1);
display(arg2);

exitcode = 0;

@FlowProject.operation
@flow.cmd
def compute_volume(job):
    return "matlab -r 'prog {job.sp.foo} {job.sp.bar}' > {job.ws}/output.txt"
```

- write a function `generate_inputs` that can take the parameters as inputs, and will generate `dis.dat` and `start.dat`
- `generate_inputs` creates `dis.dat` with `a=4` and `start.dat` with `b=5` say and they are copied to `run_a4_b5`


```
# init.py
import signac

project = signac.init_project('ideal-gas-project')

for p in range(1, 10):
    sp = {'p': p, 'kT': 1.0, 'N': 1000}
    job = project.open_job(sp)
    job.init()
```

- creates a `signac` data space, which basically amounts to taking a directory on the filesystem, marking it as a `signac` data space, and then creating subdirectories for every parameter combination you pass as an argument to the `project.open_job` function

```
from flow import FlowProject, cmd

class Project(FlowProject):
    pass

@Project.operation
@cmd
@Project.post.isfile('rpa.wel')
def run_this_first(job):
    return "$FORTRAN_SCRIPT"

@Project.operation
@Project.post.after(run_this_first):
def run_this_second(job):
    return $CPP_SCRIPT
```

- pass the "working directory" and then prepend all filenames with that directory


- `return "fortran_executable {ws}".format(ws=job.workspace())`


- [`_read_line_line`](https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file/18603065#18603065) sounds like it would do the trick.



- since your operations are bash commands, you can just pipe your output into a specific file like you would normally; so you would do something like : 
`return "your command > {}".format(job.fn('outputfile.txt'))`
- if you run locally a simple `--parallel` appended to the run command will invoke parallel execution

- your condition functions can be arbitrary python functions that take the job argument as first argument, you don't have to try to cramp everything into the decorator.

```
# project.py
from flow import FlowProject


def volume_computed(job):
    return os.path.isfile("volume.txt")


@FlowProject.operation
@FlowProject.post(volume_computed)
def compute_volume(job):
    volume = job.sp.N * job.sp.kT / job.sp.p
    with open(job.fn('volume.txt'), 'w') as file:
        file.write(str(volume) + '\n')


if __name__ == '__main__':
    FlowProject().main()
```

The `volume_computed()` function is a condition function. It's also decorated as a label-function, which means it's going to show up in the status summary, but not every condition function has to be a label function.

You can use the `-d` or `--detailed` option to show it on a per-job level.
You need to add the `--progress` option for that.


