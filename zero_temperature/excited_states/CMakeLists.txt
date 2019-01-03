cmake_minimum_required(VERSION 3.5)

# project name
project(ztes)

# example how to set c++ compiler flags for GNU
if(CMAKE_CXX_COMPILER_ID MATCHES GNU)
    set(CMAKE_CXX_FLAGS         "${CMAKE_CXX_FLAGS} -Woverloaded-virtual -Wno-write-strings -Wno-unused -Wno-deprecated")
    set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g3")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()

#
# Compile.
#

file (GLOB source_files src/*.cc include/*.h)

add_executable (ztes ${source_files})

target_include_directories(ztes PRIVATE include/)
target_link_libraries(ztes m)
