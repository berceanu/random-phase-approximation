cmake_minimum_required(VERSION 3.5)

project(skys Fortran)

# Add our local modlues to the module path
SET(CMAKE_MODULE_PATH "../../cmake_fortran/Modules/")

# This INCLUDE statement executes code that sets the compile flags for DEBUG,
# RELEASE, and TESTING.  You should  review this file and make sure the flags 
# are to your liking.
INCLUDE(${CMAKE_MODULE_PATH}/SetFortranFlags.cmake)

#
# Compile.
#
file(GLOB_RECURSE sources  src/*.f)
add_executable(skys ${sources})

SET(CMAKE_INSTALL_PREFIX ../../..)
INSTALL(TARGETS skys RUNTIME DESTINATION bin)