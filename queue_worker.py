import redis

from task_queue import TaskQueue


def worker():
    connection = redis.Redis()
    queue = TaskQueue(connection)
    if queue.get_length() > 0:
        queue.dequeue()
        return True
    else:
        print('No tasks in queue')
        return False


if __name__ == '__main__':
    worker()
