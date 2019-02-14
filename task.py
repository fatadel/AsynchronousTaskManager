import time
import os

from statuses import Status
from datetime import datetime


class Task:
    def __init__(self, task_id, exec_time):
        self.task_id = task_id
        self.exec_time = exec_time
        self.status = Status.IN_QUEUE
        self.create_time = datetime.now()
        self.start_time = None

    def process_task(self):
        self.status = Status.RUN
        self.start_time = datetime.now()
        print(f'Task #{self.task_id} started with pid {os.getpid()}')
        time.sleep(self.exec_time)
        print(f'Task #{self.task_id} completed in {self.exec_time} seconds')
        self.status = Status.COMPLETED
