#!/usr/bin/env python3
import pathlib

import mypackage.util as util
import pandas as pd
import signac

proj = signac.get_project(root=".")

job = next(iter(proj.find_jobs(filter=dict(astro="y", neutron_number=96))))

print(f"\nWorking on job {job.get_id()}\n")

job_dir = pathlib.Path(job.workspace())

for file in job_dir.iterdir():
    print(file.name)

astrorate_fn = "astrorate.tot"
astrorate_path = pathlib.Path(job.fn(astrorate_fn))

print(f"\n{astrorate_fn}:")
print(astrorate_path.open().read())

astrorate_df = pd.read_csv(astrorate_path, sep=r"\s+", comment="#")

nucleus = util.get_nucleus(job.sp.proton_number, job.sp.neutron_number)
ng_col = f"(n,g){nucleus}"

# (n,g): 50 145Sn + n -> 146Sn
neutron_capture_rate_df = astrorate_df[["T9", ng_col]]

print(neutron_capture_rate_df)

# todo remove file
