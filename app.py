from flask import Flask, request, jsonify
from flask_cors import CORS # Добавили импорт CORS

app = Flask(__name__)
CORS(app) # Разрешили фронтенду общаться с бэкендом

# ООП: Класс отдельной задачи
class Task:
    def __init__(self, task_id, title):
        self.id = task_id
        self.title = title
        self.completed = False

    def to_dict(self):
        return {"id": self.id, "title": self.title, "completed": self.completed}

# ООП: Класс для управления списком задач
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title):
        task = Task(self.next_id, title)
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

manager = TaskManager()

# --- API Роуты (Связь с клиентской частью) ---

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(manager.get_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = manager.add_task(data['title'])
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

if __name__ == '__main__':
    # Запуск сервера
    app.run(debug=True, port=5000)