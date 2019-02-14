import random
import pickle
from task import Task

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
        return task.task_id

    def dequeue(self):
        _, serialized_task = self.connection.brpop(self.queue_name)
        task = pickle.loads(serialized_task)
        task.process_task()
        return task.task_id

    def get_length(self):
        return self.connection.llen(self.queue_name)
