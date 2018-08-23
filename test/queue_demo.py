#!/usr/bin/env python3

import subprocess
import threading
import sys
import queue


def read_output(pipe, q):
    """reads output from `pipe`, when line has been read, puts
    line on queue `q`"""

    while True:
        l = pipe.readline()
        q.put(l)

logTimes = sys.argv[1]
# start both `proc_a.py` and `proc_b.py`
proc_a = subprocess.Popen(("./log", logTimes), stdout=subprocess.PIPE, bufsize=1)
proc_b = subprocess.Popen(("./log", logTimes), stdout=subprocess.PIPE, bufsize=1)

# queues for storing output lines
pa_q = queue.Queue()
pb_q = queue.Queue()

# start a pair of threads to read output from procedures A and B
pa_t = threading.Thread(target=read_output, args=(proc_a.stdout, pa_q))
pb_t = threading.Thread(target=read_output, args=(proc_b.stdout, pb_q))
pa_t.daemon = True
pb_t.daemon = True
pa_t.start()
pb_t.start()

while True:
    # check if either sub-process has finished
    proc_a.poll()
    proc_b.poll()

    if proc_a.returncode is not None or proc_b.returncode is not None:
        print(proc_a.returncode, proc_b.returncode)
        print('exiting')
        break

    # write output from procedure A (if there is any)
    try:
        l = pa_q.get(False)
        sys.stdout.write("%s: %s\n" % ("A: ", l))
    except queue.Empty:
        print('empty!')
        pass

    # write output from procedure B (if there is any)
    try:
        l = pb_q.get(False)
        sys.stdout.write("%s: %s\n" % ("B: ", l))
    except queue.Empty:
        print('empty!')
        pass