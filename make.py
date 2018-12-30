#!/usr/bin/env python3

import re
import sys
import os
import shutil
import logging
logging.basicConfig(level='INFO')
logger = logging.getLogger('Update')

fnamerex = r'[\w]+\.[A-Za-z]{1,3}'
cpprex = r'g\+\+'
fortrex = r'gfortran'

def change_ext(fname, old_ext, new_ext):
    base, ext = os.path.splitext(fname)
    if ext != old_ext:
        raise TypeError('Detected different extension in %s', fname)
    return base + new_ext

def distinct_extensions(fnames):
    extensions = []
    for f in fnames:
        _, ext = os.path.splitext(f)
        extensions.append(ext)
    return set(extensions)

def check_extensions(fnames, extensions):
    for f in fnames:
        _, ext = os.path.splitext(f)
        if ext not in extensions:
            raise TypeError('Wrong file extension on %s', f)
    return None

def extract_from(makefile):
    with open(makefile) as file:
        logger.info('Reading %s', makefile)
        file_contents = file.read()
        filenames = re.findall(fnamerex, file_contents)
        logger.info('Distinct extensions: %s', distinct_extensions(filenames))
        #
        if re.search(cpprex, file_contents): # C++
            logger.info('C++ makefile detected.')
            check_extensions(filenames, ['.o', '.cc', '.h'])
            logger.info('Removing all .o files.')
            filenames = [f for f in filenames if os.path.splitext(f)[1] != '.o']
            #
        elif re.search(fortrex, file_contents): # Fortran
            logger.info('Fortran makefile detected.')
            logger.info('Renaming all .o files to .f')
            filenames = [change_ext(f, '.o', '.f') for f in filenames]
            #
        else: # Otherwise
            raise TypeError('Cannot detect type of makefile.') 
    # remove duplicates
    filenames = list(set(filenames))
    logger.info('%s distinct file names from Makefile.', len(filenames))
    return filenames

def main(): 
    base_path = str(sys.argv[1]) # eg., /home/berceanu/Development/rpa/finite_temperature/ground_state
    makefile = os.path.join(base_path, 'Makefile.old')
    makefilenames = extract_from(makefile) # extract file names from the Makefile

    # Given a set of files in `src`, *move* the ones that are _not_ in `Makefile` to `unused`.

    # create `unused` folder, if not there
    unused = os.path.join(base_path, 'unused')
    if not os.path.exists(unused):
        os.makedirs(unused)

    # get contents of `src`
    src = os.path.join(base_path, 'src')
    src_files = os.listdir(src)
    logger.info('Distinct extensions in `src`: %s', distinct_extensions(src_files))
    logger.info('%s distinct file names in `src`.', len(src_files))

    # files in `src` but not in Makefile
    not_in_makefile = list(set(src_files).difference(set(makefilenames)))
    assert len(not_in_makefile) == len(src_files) - len(makefilenames) #check
    if not not_in_makefile:
        raise ValueError('Nothing to do, exiting.')

    # move them to unused folder
    for fname in not_in_makefile:
        path = os.path.join(src, fname)
        shutil.move(path, unused)

if __name__ == "__main__":
    main()
