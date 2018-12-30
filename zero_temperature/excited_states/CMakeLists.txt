cmake_minimum_required(VERSION 3.10)

project(ztes)


set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} -Wno-deprecated)

#
# Compile.
#
file(GLOB_RECURSE sources  src/*.cc src/*.h )
add_executable(run ${sources})

target_link_libraries(run m)
