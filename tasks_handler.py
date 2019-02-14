import multiprocessing
from queue_worker import worker

PROCESSES = 2


def handler():
    processes = []
    while True:
        for i in range(PROCESSES):
            p = multiprocessing.Process(target=worker)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()


if __name__ == '__main__':
    handler()
