from task_queue import TaskQueue
from app import connection


def worker():
    queue = TaskQueue(connection)
    if queue.get_length() > 0:
        queue.dequeue()
    else:
        print('No tasks in queue')


if __name__ == '__main__':
    worker()
