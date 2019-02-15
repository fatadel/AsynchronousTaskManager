import time
import os


def process_task(task_id, exec_time):
    print(f'Task #{task_id} started with pid {os.getpid()}')
    time.sleep(exec_time)
    print(f'Task #{task_id} completed in {exec_time} seconds')
