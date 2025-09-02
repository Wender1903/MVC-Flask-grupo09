import os
from flask import Flask
from config import Config
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from models import db  # Importa a instância única de SQLAlchemy

# Cria a app
app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)

# Inicializa o banco de dados
db.init_app(app)

# Cria tabelas
with app.app_context():
    db.create_all()

# -------------------- Rotas Task --------------------
app.add_url_rule('/tasks', view_func=TaskController.list_tasks, methods=['GET'], endpoint='list_tasks')
app.add_url_rule('/tasks/new', view_func=TaskController.create_task, methods=['GET','POST'], endpoint='create_task')
app.add_url_rule('/tasks/update/<int:task_id>', view_func=TaskController.update_task, methods=['POST'], endpoint='update_task_status')
app.add_url_rule('/tasks/delete/<int:task_id>', view_func=TaskController.delete_task, methods=['POST'], endpoint='delete_task')

# -------------------- Rotas User --------------------
app.add_url_rule('/', 'index', UserController.index)
app.add_url_rule('/contact', 'contact', UserController.contact, methods=['GET','POST'])


# -------------------- Rodar App --------------------
if __name__ == '__main__':
    app.run(debug=True, port=5002)
