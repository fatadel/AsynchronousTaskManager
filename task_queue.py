import random
import task
from datetime import datetime
from statuses import Status

QUEUE_NAME = 'task_queue'


class TaskQueue:

    def __init__(self, connection, queue_name=QUEUE_NAME):
        self.connection = connection
        self.queue_name = queue_name

    def enqueue(self):
        task_id = self.connection.incr('task_id')
        self.connection.lpush(self.queue_name, task_id)
        self.connection.hmset(f'task:{task_id}', {
            'create_time': datetime.now(),
            'start_time': None,
            'exec_time': random.randint(0, 10),
            'status': Status.IN_QUEUE.name
        })
        return task_id

    def dequeue(self):
        _, task_id = self.connection.brpop(self.queue_name)
        self.connection.hset(f'task:{task_id}', 'status', Status.RUN.name)
        self.connection.hset(f'task:{task_id}', 'start_time', datetime.now())
        exec_time = self.connection.hget(f'task:{task_id}', 'exec_time')
        try:
            task.process_task(task_id, int(exec_time))
        except ValueError:
            print(f'Task #{task_id} has incompatible exec_time, will be processed with 0')
            task.process_task(task_id, 0)
        self.connection.hset(f'task:{task_id}', 'status', Status.COMPLETED.name)
        return task_id

    def get_length(self):
        return self.connection.llen(self.queue_name)
