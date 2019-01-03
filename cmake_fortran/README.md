Code from https://github.com/SethMMorton/cmake_fortran_template

### cmake/Modules/ ###

This directory contains CMake scripts that aid in configuring the build system.

###### SetCompileFlag.cmake ######

This file defines a function that will test a set of compiler flags to see which one works and adds that flag to a list of compiler flags.  This is used to set compile flags when you don't know which compiler will be used.

###### SetFortranFlags.cmake ######

This file uses the function from `SetCompilerFlag.cmake` to set the DEBUG, TESTING, and RELEASE compile flags for your build.  You might want to inspect this file and edit the flags to your liking.


## Configuring the build ##

It is usually preferred that you do an out-of-source build.  To do this, create a `build/` directory at the top level of your project and build there.  

    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
    
As written, this template will allow you to specify one of three different sets of compiler flags.  The default is RELEASE.  You can change this using to TESTING or DEBUG using

    $ cmake .. -DCMAKE_BUILD_TYPE=DEBUG
    
or

    $ cmake .. -DCMAKE_BUILD_TYPE=TESTING
