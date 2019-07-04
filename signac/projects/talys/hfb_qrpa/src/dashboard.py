#!/usr/bin/env python3
from signac_dashboard import Dashboard
from signac_dashboard.modules.statepoint_list import StatepointList
from signac_dashboard.modules.image_viewer import ImageViewer
from signac_dashboard.modules.file_list import FileList
from signac_dashboard.modules.notes import Notes


class MyDashboard(Dashboard):
    def job_sorter(self, job):
        # should return key for
        # sorted(jobs, key=lambda job: job_sorter(job))
        return job.sp["proton_number"], job.sp["neutron_number"], job.sp["astro"]

    def job_title(self, job):
        return f"(Z, N) = ({job.sp['proton_number']}, {job.sp['neutron_number']}), astro={job.sp.astro}"


if __name__ == "__main__":
    config = {"DASHBOARD_PATHS": ["src/"]}
    dashboard = MyDashboard(
        modules=[
            ImageViewer(name="Figures", img_globs=["*.png"]),
            StatepointList(enabled=True),
            FileList(enabled=False),
            Notes(enabled=False),
        ],
        config=config,
    )
    dashboard.main()
