from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date

app = Flask(__name__)
CORS(app)

class Task:
    def __init__(self, task_id, title, due_date=None):
        self.id = task_id
        self.title = title
        self.completed = False
        self.due_date = due_date  # строка "YYYY-MM-DD" или None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "due_date": self.due_date,
            "overdue": self.is_overdue()
        }

    def is_overdue(self):
        if not self.due_date or self.completed:
            return False
        return self.due_date < date.today().isoformat()

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, due_date=None):
        task = Task(self.next_id, title, due_date)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def toggle_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                return task
        return None

    def get_tasks_by_date(self, due_date):
        return [t.to_dict() for t in self.tasks if t.due_date == due_date]

    def get_overdue_tasks(self):
        return [t.to_dict() for t in self.tasks if t.is_overdue()]

manager = TaskManager()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(manager.get_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = manager.add_task(data['title'], data.get('due_date'))
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    manager.delete_task(task_id)
    return jsonify({"message": "Deleted"}), 200

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    task = manager.toggle_task(task_id)
    if task:
        return jsonify(task.to_dict())
    return jsonify({"error": "Not found"}), 404

@app.route('/api/tasks/calendar/<due_date>', methods=['GET'])
def get_tasks_by_date(due_date):
    return jsonify(manager.get_tasks_by_date(due_date))

@app.route('/api/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    return jsonify(manager.get_overdue_tasks())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
