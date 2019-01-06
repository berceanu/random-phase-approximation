#!/usr/bin/env bash

rm -rf build-debug
mkdir build-debug
cd build-debug
cmake -DCMAKE_BUILD_TYPE=DEBUG ..
cmake --build . --target all

# Note: TYPE=TESTING is also available
