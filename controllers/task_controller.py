from flask import request, jsonify
from models import db
from models.task import Task
from models.user import User

def _serialize_task(t: Task) -> dict:
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status,
        "user_id": t.user_id,
    }

class TaskController:
    @staticmethod
    def list_tasks():
        """
        Listar Tarefas
        ---
        tags:
          - Tasks
        description: Retorna a lista de tarefas.
        responses:
          200:
            description: Lista de tarefas
            schema:
              type: array
              items:
                $ref: '#/definitions/Task'
        """
        tasks = Task.query.all()
        return jsonify([_serialize_task(t) for t in tasks]), 200

    @staticmethod
    def create_task():
        """
        Criar Tarefa
        ---
        tags:
          - Tasks
        description: Cria uma nova tarefa.
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - user_id
              properties:
                title:
                  type: string
                description:
                  type: string
                user_id:
                  type: integer
        responses:
          201:
            description: Tarefa criada
            schema:
              $ref: '#/definitions/Task'
          400:
            description: Requisição inválida
          404:
            description: Usuário não encontrado
        """
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        user_id = data.get("user_id")
        description = data.get("description", "")

        if not title or not user_id:
            return jsonify({"message": "Campos obrigatórios: title, user_id"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404

        new_task = Task(title=title, description=description, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        return jsonify(_serialize_task(new_task)), 201

    @staticmethod
    def update_task(task_id: int):
        """
        Atualizar Tarefa
        ---
        tags:
          - Tasks
        description: Atualiza uma tarefa existente.
        consumes:
          - application/json
        parameters:
          - in: path
            name: task_id
            type: integer
            required: true
            description: ID da tarefa
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: ["Pendente", "Concluído"]
                user_id:
                  type: integer
        responses:
          200:
            description: Tarefa atualizada
            schema:
              $ref: '#/definitions/Task'
          404:
            description: Tarefa não encontrada
        """
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Tarefa não encontrada"}), 404

        data = request.get_json(silent=True) or {}

        for field in ("title", "description", "status", "user_id"):
            if field in data and data[field] is not None:
                setattr(task, field, data[field])

        db.session.commit()
        return jsonify(_serialize_task(task)), 200

    @staticmethod
    def delete_task(task_id: int):
        """
        Excluir Tarefa
        ---
        tags:
          - Tasks
        description: Remove uma tarefa pelo ID.
        parameters:
          - in: path
            name: task_id
            type: integer
            required: true
            description: ID da tarefa
        responses:
          200:
            description: Exclusão concluída
            schema:
              type: object
              properties:
                message:
                  type: string
          404:
            description: Tarefa não encontrada
        """
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Tarefa não encontrada"}), 404

        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarefa excluída com sucesso"}), 200
