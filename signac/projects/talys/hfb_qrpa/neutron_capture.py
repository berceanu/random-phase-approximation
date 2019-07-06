#!/usr/bin/env python3
import signac

proj = signac.get_project(root=".")

job = iter(proj.find_jobs(filter=dict(astro="y", neutron_number=96))).next()

print(job.get_id())
