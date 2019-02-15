import redis
from flask import Flask, jsonify
from task_queue import TaskQueue

app = Flask(__name__)
connection = redis.Redis(decode_responses=True)
queue = TaskQueue(connection)


@app.route('/')
def hello_world():
    connection.flushdb()
    return 'Hello World!'


# TODO edit method to POST
@app.route('/create-task')
def create_task():
    return jsonify({
        'task_id': queue.enqueue()
    })


@app.route('/get-task/<int:task_id>')
def get_task(task_id):
    task = connection.hgetall(f'task:{task_id}')
    if len(task) == 0:
        return jsonify({
            'error': 'Task not found'
        })
    else:
        return jsonify({
            'status': task.get('status'),
            'create_time': task.get('create_time'),
            'start_time': task.get('start_time'),
            'time_to_execute': f"{task.get('exec_time')} second(s)"
        })


if __name__ == '__main__':
    app.run()
