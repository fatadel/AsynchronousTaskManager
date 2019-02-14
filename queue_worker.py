import redis

from task_queue import TaskQueue


def worker():
    connection = redis.Redis()
    queue = TaskQueue(connection)
    if queue.get_length() > 0:
        queue.dequeue()
    else:
        print('No tasks in queue')


if __name__ == '__main__':
    worker()
