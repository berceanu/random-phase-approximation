#!/usr/bin/env python3
# Copyright (c) 2018 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
from signac_dashboard import Dashboard
from signac_dashboard.modules.statepoint_list import StatepointList
from signac_dashboard.modules.image_viewer import ImageViewer
from signac_dashboard.modules.document_list import DocumentList
from signac_dashboard.modules.file_list import FileList
from signac_dashboard.modules.notes import Notes
import mypackage.dipole_transitions as dt



class MyDashboard(Dashboard):
    def job_sorter(self, job):
        return job.sp.get('proton_number', -1)
    def job_title(self, job):
        return f"Proton number = {job.sp['proton_number']}"


if __name__ == '__main__':
    config = {'DASHBOARD_PATHS': ['src/']}
    dashboard = MyDashboard(modules=[
        ImageViewer(name='Transition strength distribution', img_globs=['*.png']),
        StatepointList(enabled=True),
        DocumentList(max_chars=140),
        FileList(enabled=False),
        Notes(enabled=False),
        dt.DipoleTransitions(name='Dipole Transitions', enabled=True),
        ],
        config=config
        )
    dashboard.main()
