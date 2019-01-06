#!/usr/bin/env bash

rm -rf build-release
mkdir build-release
cd build-release
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=../../bin ..
cmake --build . --target install

