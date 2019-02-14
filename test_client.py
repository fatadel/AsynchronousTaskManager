import redis
from task_queue import TaskQueue

NUMBER_OF_TASKS = 10

if __name__ == '__main__':
    connection = redis.Redis()
    queue = TaskQueue(connection)
    for i in range(NUMBER_OF_TASKS):
        queue.enqueue()
    print(f'Enqueued {NUMBER_OF_TASKS} tasks')
