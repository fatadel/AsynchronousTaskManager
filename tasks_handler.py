# Task handler
# Must be run separately from the app

import multiprocessing
from queue_worker import worker

# Number of simultaneous processes
PROCESSES = 2


def handler():
    # array of processes to join
    processes = []
    while True:
        for i in range(PROCESSES):
            # Create new process with worker
            p = multiprocessing.Process(target=worker)
            # Append to processes array
            processes.append(p)
            # Start the process
            p.start()
        # Join the processes
        for p in processes:
            p.join()


if __name__ == '__main__':
    handler()
