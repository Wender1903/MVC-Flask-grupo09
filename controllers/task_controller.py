from flask import render_template, request, redirect, url_for, jsonify
from models import db
from models.task import Task
from models.user import User

class TaskController:
    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        return render_template("tasks.html", tasks=tasks) 
    
    @staticmethod
    def create_tasks():
        if request.method == "GET":
            users = User.query.all()
            return render_template("create_task.html", users=users)    
        
        elif request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            user_id = request.form.get("user_id")

            new_task = Task(title = title, 
                            description = description, 
                            user_id = user_id)
            
            db.session.add(new_task)
            db.session.commit()

            return redirect(url_for("list_tasks"))
        
    @staticmethod
    def update_tasks(task_id):
        task = Task.query.get(task_id)

        if not task:
            return jsonify({"mensagem": "Erro, Tarefa não encontrada"}), 404
        
        if task.status == "Pendente":
            task.status = "Concluído"
        else:
            task.status = "Pendente"

        db.session.commit()
        return redirect(url_for("list_tasks"))
    
    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"mensagem": "Erro, Tarefa não encontrada"}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return redirect(url_for('list_tasks'))
