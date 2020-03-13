import logging
import pathlib
import shutil
import signac

logger = logging.getLogger(__name__)


def main():
    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".."
    rpa = signac.get_project(root=rpa_root)

    logger.info("rpa project: %s" % rpa.root_directory())

    for job in rpa:
        if job.sp.transition_energy != 0.42:
            fname = "inset.png"
            local_fname = f"{job.id}_{fname}"
            shutil.copy(job.fn(fname), local_fname)
            print(f"{local_fname}: {job.sp.temperature}, {job.sp.transition_energy}")


if __name__ == "__main__":
    main()
