# Task queue class
# The task queue is made as a Redis list. Enqueuing/dequeuing takes O(1), taking into account
# that Redis is an in-memory data structure, this operations are extremely fast.
# The queue contains only ids of tasks. All other task related data is in Redis hash map.
# Writing to Redis hash map is also O(1). Getting from the hash map is O(n), where n -
# is the number of fields for a particular key. Since we don't store more than 4 fields, this
# also becomes super fast.

import random
import task
from datetime import datetime
from statuses import Status

# Default queue name
QUEUE_NAME = 'task_queue'


class TaskQueue:

    def __init__(self, connection, queue_name=QUEUE_NAME):
        """
        Creates new TaskQueue instance.

        :param connection: Database connection
        :param queue_name: Queue name
        """
        self.connection = connection
        self.queue_name = queue_name

    def enqueue(self):
        """
        Enqueues (adds) new tasks in queue.
        Adds task related data to hash map.

        :return: Created task id
        """
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
        """
        Dequeues (removes) task from queue and immediately makes it
        start processing.
        Updates data in hash map.

        :return: Dequeued task id
        """
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
        """
        Returns queue length
        :return: Queue length
        """
        return self.connection.llen(self.queue_name)
