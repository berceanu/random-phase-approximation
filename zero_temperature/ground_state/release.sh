#!/usr/bin/env bash

rm -rf build-release
mkdir build-release
cd build-release
cmake -DCMAKE_BUILD_TYPE=RELEASE ..
cmake --build . --target install
