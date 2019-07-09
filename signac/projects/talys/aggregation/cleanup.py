#!/usr/bin/env python3
import logging
import pathlib
import shutil

logger = logging.getLogger(__name__)


def unlink_file(fn):
    if fn.is_file():
        fn.unlink()
        logger.warning("Removed %s" % fn)
    else:
        logger.info("%s not found!" % fn)


def cleanup_proj(root=pathlib.Path.cwd()):
    # remove workspace/ folder
    workspace = root / "workspace"
    if workspace.is_dir():
        shutil.rmtree(workspace)
        logger.warning("Removed %s" % workspace)
    else:
        logger.info("%s not found!" % workspace)

    unlink_file(root / "signac.rc")
    unlink_file(root / "project.log")
    unlink_file(root / ".signac_sp_cache.json.gz")


def main():
    temperature_dir = pathlib.Path.cwd() / "temperature"
    cleanup_proj(root=temperature_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("==Clean-up started==")
    main()
    logger.info("==Clean-up finished==")
