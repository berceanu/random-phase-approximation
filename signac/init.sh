#!/usr/bin/env bash

rm -rf workspace/
rm signac.rc
rm signac_statepoints.json
rm project.log
rm signac_project_document.json
rm .signac_sp_cache.json.gz
python3 src/init.py
