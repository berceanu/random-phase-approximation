#!/usr/bin/env bash

rm -rf build-release
mkdir build-release
cd build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --target install
