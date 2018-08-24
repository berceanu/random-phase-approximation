#!/usr/bin/env python3

def extract_transerg(filename):
    with open(filename) as f:
        lines = f.readlines()

    return (float(line.rstrip().split()[2]) for line in lines)



if __name__ == "__main__":
    print(extract_transerg('transerg.in'))

    # Replace variables in file
    with open('start.dat', 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('transerg   =   0.00', 'transerg   =   10.43'))
