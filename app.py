import redis
from flask import Flask, jsonify
from task_queue import TaskQueue

app = Flask(__name__)
connection = redis.Redis()
queue = TaskQueue(connection)


@app.route('/')
def hello_world():
    return 'Hello World!'


# TODO edit method to POST
@app.route('/create-task')
def create_task():
    return jsonify({
        'task_id': queue.enqueue()
    })


@app.route('/get-task/<int:task_id>')
def get_task():
    pass


if __name__ == '__main__':
    app.run()
