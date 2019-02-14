import random
import pickle
from task import Task
from statuses import Status

QUEUE_NAME = 'task_queue'


class TaskQueue:

    def __init__(self, connection, queue_name=QUEUE_NAME):
        self.connection = connection
        self.queue_name = queue_name

    def enqueue(self):
        task_id = self.connection.incr('task_id')
        task = Task(task_id, random.randint(0, 10))
        serialized_task = pickle.dumps(task, protocol=pickle.HIGHEST_PROTOCOL)
        self.connection.lpush(self.queue_name, serialized_task)
        self.connection.hmset(f'task:{task_id}', {
            'create_time': task.create_time,
            'start_time': task.start_time,
            'exec_time': task.exec_time,
            'status': Status.IN_QUEUE
        })
        return task.task_id

    def dequeue(self):
        _, serialized_task = self.connection.brpop(self.queue_name)
        task = pickle.loads(serialized_task)
        self.connection.hset(f'task:{task.task_id}', 'status', Status.RUN)
        task.process_task()
        self.connection.hset(f'task:{task.task_id}', 'status', Status.COMPLETED)
        return task.task_id

    def get_length(self):
        return self.connection.llen(self.queue_name)
