import redis
from flask import Flask, jsonify
from task_queue import TaskQueue

# Initialize flask app instance
app = Flask(__name__)
# Initialize connection to Redis database
connection = redis.Redis(decode_responses=True)
# Initialize task queue
queue = TaskQueue(connection)


# Welcome page
@app.route('/')
def index():
    return 'Dr.Web is better than Kaspersky!'


# Create task endpoint
@app.route('/create-task', methods=['POST'])
def create_task():
    # Add task to queue and return its id
    return jsonify({
        'task_id': queue.enqueue()
    })


# Get task data endpoint
@app.route('/get-task/<int:task_id>')
def get_task(task_id):
    # Fetch task data from database
    task = connection.hgetall(f'task:{task_id}')

    # Return error if nothing found or task data otherwise
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


# Clear database endpoint
@app.route('/clear-db', methods=['POST'])
def hello_world():
    # Clear current database
    connection.flushdb()
    return 'Database cleared'


if __name__ == '__main__':
    app.run()
