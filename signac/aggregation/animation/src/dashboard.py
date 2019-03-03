from signac_dashboard import Dashboard
from signac_dashboard.modules.statepoint_list import StatepointList
from signac_dashboard.modules.image_viewer import ImageViewer
from signac_dashboard.modules.video_viewer import VideoViewer
from signac_dashboard.modules.document_list import DocumentList
from signac_dashboard.modules.file_list import FileList
from signac_dashboard.modules.notes import Notes


class MyDashboard(Dashboard):
    def job_sorter(self, job):
        # shuld return key for
        #  sorted(jobs, key=lambda job: job_sorter(job))
        return job.sp['proton_number']

    def job_title(self, job):
        return f"Z = {job.sp['proton_number']}"


if __name__ == '__main__':
    config = {'DASHBOARD_PATHS': ['src/']}
    dashboard = MyDashboard(modules=[
        ImageViewer(name='Transition strength distribution', img_globs=['*.png']),
        VideoViewer(name='Animation', video_globs=['*.mp4'], preload='auto'),
        StatepointList(enabled=True),
        DocumentList(max_chars=140),
        FileList(enabled=False),
        Notes(enabled=False)
        ],
        config=config
        )
    dashboard.main()
