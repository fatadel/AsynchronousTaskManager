import time

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
        time.sleep(self.exec_time)
