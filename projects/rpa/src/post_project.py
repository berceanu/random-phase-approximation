import signac
from mypackage.util import copy_file

rpa_project = signac.get_project()

for zero_job in rpa_project.find_jobs({"temperature": 0}):
    for nonzero_job in rpa_project.find_jobs(
        {"temperature": {"$ne": 0}, "neutron_number": zero_job.sp.neutron_number}
    ):
        copy_file(
            source=zero_job.fn(zero_job.doc.photon_strength_function),
            destination=nonzero_job.fn(nonzero_job.doc.photon_strength_function),
            exist_ok=True,
        )
        print(zero_job, nonzero_job)
