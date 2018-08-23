#!/usr/bin/env python3

import subprocess
import sys
from threading import Thread


def async_stream_process_stdout(process, log_fn):
    """ Stream the stdout and stderr for a process out to display async
    :param process: the process to stream the log for
    :param log_fn: a function that will be called for each log line
    :return: None
    """
    logging_thread = Thread(target=stream_process_stdout,
                            args=(process, log_fn, ))
    logging_thread.start()

    return logging_thread

def stream_process_stdout(process, log_fn):
    """ Stream the stdout and stderr for a process out to display
    :param process: the process to stream the logs for
    :param log_fn: a function that will be called for each log line
    :return: None
    """
    while True:
        line = process.stdout.readline().rstrip().decode('utf-8')
        if not line:
            break

        log_fn(line)

def log_fn(process):
    return lambda line: sys.stdout.write('{}: {:.2f}%\n'.format(process, float(line.split()[-1]))) if 'pa1 = ' in line else None

if __name__ == "__main__":

    ps_one = subprocess.Popen("./run", stdout=subprocess.PIPE, bufsize=1,
     cwd="./zero_temperature/excited_states/")
    ps_two = subprocess.Popen("./run", stdout=subprocess.PIPE, bufsize=1,
     cwd="./finite_temperature/excited_states/")

    logger_one = async_stream_process_stdout(ps_one, log_fn('zero T'))
    logger_two = async_stream_process_stdout(ps_two, log_fn('finite T'))

    logger_one.join()
    logger_two.join()


