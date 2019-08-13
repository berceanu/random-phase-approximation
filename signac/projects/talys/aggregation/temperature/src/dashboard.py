#!/usr/bin/env python3
from signac_dashboard import Dashboard
from signac_dashboard.modules.statepoint_list import StatepointList
from signac_dashboard.modules.document_list import DocumentList
from signac_dashboard.modules.image_viewer import ImageViewer
from signac_dashboard.modules.file_list import FileList
from signac_dashboard.modules.notes import Notes


class MyDashboard(Dashboard):
    def job_sorter(self, job):
        return job.sp["proton_number"], job.sp["temperature"]

    def job_title(self, job):
        return f"(Z, N) = ({job.sp['proton_number']}, {job.sp['temperature']})"


# To use multiple workers, a single shared key must be used. By default, the
# secret key is randomly generated at runtime by each worker. Using a provided
# shared key allows sessions to be shared across workers. This key was
# generated with os.urandom(16)

config = {
    'DASHBOARD_PATHS': ['src/'],
    'SECRET_KEY': b"\x99o\x90'/\rK\xf5\x10\xed\x8bC\xaa\x08\x9d\x99"
}

modules = [
    ImageViewer(name="Figures", img_globs=["*.png"]),
    StatepointList(enabled=False),
    DocumentList(max_chars=140),
    FileList(enabled=False),
    Notes(enabled=False),
]

dashboard = MyDashboard(config=config, modules=modules)


if __name__ == "__main__":
    dashboard.main()
