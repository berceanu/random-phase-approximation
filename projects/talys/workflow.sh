#!/usr/bin/env bash

rm -rf workspace/
rm -rf signac.rc
rm -rf project.log

./src/init.py

./src/project.py run

