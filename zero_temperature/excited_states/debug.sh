#!/usr/bin/env bash

rm -rf build-debug
mkdir build-debug
cd build-debug
cmake -G "CodeLite - Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug ..
