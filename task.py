import time

from statuses import Status


class Task:
    def __init__(self, task_id, exec_time):
        self.task_id = task_id
        self.exec_time = exec_time
        self.status = Status.IN_QUEUE

    def process_task(self):
        time.sleep(self.exec_time)
