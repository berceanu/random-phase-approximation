#!/usr/bin/env bash

rm -rf Debug
mkdir Debug
cd Debug
cmake -G"CodeLite - Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug ..
