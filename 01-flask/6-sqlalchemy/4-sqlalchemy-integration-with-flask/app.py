from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# SQLite URI inside current working directory
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ----------------------------------------------------
# 1. Model Definition using Flask-SQLAlchemy syntax
# ----------------------------------------------------
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "body": self.body}

# Table initialization within application context
with app.app_context():
    db.create_all()

# ----------------------------------------------------
# 2. REST API Routes (CRUD)
# ----------------------------------------------------
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json() or {}
    if "title" not in data or "body" not in data:
        return jsonify({"error": "Missing title or body"}), 400

    new_post = Post(title=data["title"], body=data["body"])
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@app.route("/posts", methods=["GET"])
def get_posts():
    # Convenience query interface (Post.query)
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts]), 200

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post.to_dict()), 200

@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json() or {}
    post.title = data.get("title", post.title)
    post.body = data.get("body", post.body)
    db.session.commit()
    return jsonify(post.to_dict()), 200

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"status": "deleted", "post_id": post_id}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)