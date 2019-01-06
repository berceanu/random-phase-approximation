cmake_minimum_required(VERSION 3.5)

project(ftes)

# example how to set c++ compiler flags for GNU
if(CMAKE_CXX_COMPILER_ID MATCHES GNU)
    set(CMAKE_CXX_FLAGS         "${CMAKE_CXX_FLAGS} -Woverloaded-virtual -Wno-write-strings -Wno-unused -Wno-deprecated")
    set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g3")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()

set (source_dir "${PROJECT_SOURCE_DIR}/src/")
set (include_dir "${PROJECT_SOURCE_DIR}/include/")

file (GLOB source_files "${source_dir}/*.cc")
file (GLOB include_files "${include_dir}/*.h")

add_executable (ftes ${source_files} ${include_files})

target_include_directories(ftes PRIVATE ${include_dir})
target_link_libraries(ftes m)

SET(CMAKE_INSTALL_PREFIX ../../..)
INSTALL(TARGETS ftes RUNTIME DESTINATION bin)
