from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ✅ Define Task model globally (not inside create_app)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


def create_app(testing=False, database_uri=None):
    app = Flask(__name__, static_folder="public", static_url_path="")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri or "sqlite:///todo.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if testing:
        app.config["TESTING"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ------------------ Routes ------------------
    @app.get("/api/health")
    def health():
        return {"status": "ok"}, 200

    @app.get("/api/tasks")
    def list_tasks():
        tasks = Task.query.order_by(Task.id.desc()).all()
        return jsonify([t.to_dict() for t in tasks]), 200

    @app.post("/api/tasks")
    def add_task():
        data = request.get_json(force=True)
        title = (data.get("title") or "").strip()
        if not title:
            return {"error": "title required"}, 400
        t = Task(title=title)
        db.session.add(t)
        db.session.commit()
        return t.to_dict(), 201

    @app.patch("/api/tasks/<int:task_id>")
    def update_task(task_id):
        t = Task.query.get_or_404(task_id)
        data = request.get_json(force=True)
        if "title" in data:
            t.title = (data["title"] or "").strip() or t.title
        if "done" in data:
            t.done = bool(data["done"])
        db.session.commit()
        return t.to_dict(), 200

    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id):
        t = Task.query.get_or_404(task_id)
        db.session.delete(t)
        db.session.commit()
        return {"deleted": task_id}, 200

    @app.get("/")
    def root():
        return send_from_directory(app.static_folder, "index.html")

    return app


# ✅ Only run server if script is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
