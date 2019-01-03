#!/usr/bin/env bash

rm -rf Debug
mkdir Debug
cd Debug
cmake -DCMAKE_BUILD_TYPE=DEBUG ..
make -j 72

# Note: TYPE=TESTING is also available
