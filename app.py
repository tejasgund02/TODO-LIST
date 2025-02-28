from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# PostgreSQL database configuration
DATABASE_URL = "postgres://youruser:yourpassword@localhost:5432/todolist"

# Establish the connection to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'id': task[0], 'task': task[1]} for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    new_task = request.get_json()['task']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (task) VALUES (%s) RETURNING id', (new_task,))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': task_id, 'task': new_task})

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    new_task = request.get_json()['task']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET task = %s WHERE id = %s', (new_task, id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': id, 'task': new_task})

if __name__ == '__main__':
    app.run(debug=True)
