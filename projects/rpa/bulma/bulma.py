import logging
import pathlib

import signac

logger = logging.getLogger(__name__)


def main():
    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".."
    rpa = signac.get_project(root=rpa_root)

    logger.info("rpa project: %s" % rpa.root_directory())

    for job in rpa:
        if job.sp.transition_energy != 0.42:
            print(job.id)


if __name__ == "__main__":
    main()
