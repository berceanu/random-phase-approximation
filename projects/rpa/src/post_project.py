import signac

rpa_project = signac.get_project()

for zero_job in rpa_project.find_jobs({"temperature": 0}):
    for nonzero_job in rpa_project.find_jobs(
        {"temperature": {"$ne": 0}, "neutron_number": zero_job.sp.neutron_number}
    ):
        print(zero_job.statepoint(), nonzero_job.statepoint())
