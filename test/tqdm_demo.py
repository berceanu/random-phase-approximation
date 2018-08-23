#!/usr/bin/env python3

from subprocess import Popen, PIPE
from tqdm import tqdm

def run(command, folder):
    process = Popen(command, stdout=PIPE, shell=True, cwd=folder)
    while True:
        line = process.stdout.readline().rstrip().decode('utf-8')
        if not line:
            break
        yield line


if __name__ == "__main__":
    pbar = tqdm(total=100)
    for line in run("./run", "./finite_temperature/excited_states/"):
       if 'pa1 = ' in line:

           percentage = line.split()[-1]
           percentage = '{0:.2f}'.format(float(percentage))
           
           pbar.update(float(percentage) - pbar.n)
    pbar.close()


