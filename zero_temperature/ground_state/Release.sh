#!/usr/bin/env bash

rm -rf Release
mkdir Release
cd Release
cmake -DCMAKE_BUILD_TYPE=RELEASE ..
make -j 72
