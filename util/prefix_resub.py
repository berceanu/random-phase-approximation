#!/usr/bin/env python3

import re
import shutil
import tempfile
import sys


def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(re.sub(pattern, repl, line, flags=re.M))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


def main():
    prefix = r'ztes_'

    files = sys.argv[1:] # eg., /home/berceanu/Development/rpa/zero_temperature/excited_states/src/*.cc

    for f in files:
        sed_inplace(f, r'\"(?P<filename>[\w]+)(?P<ext>\.[A-Za-z]{3})\"',
                    r'"{}\g<filename>\g<ext>"'.format(prefix))


if __name__ == "__main__":
    main()

