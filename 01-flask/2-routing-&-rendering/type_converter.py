from flask import Flask, request
import uuid

app = Flask(__name__)


# 1. Standard Dynamic Route with Type Converter
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post ID: {post_id}"


# 2. Dynamic Route combined with Query Parameters
# URL Example: http://127.0.0.1:5000/search?q=flask
@app.route("/search")
def search():
    query = request.args.get("q")
    return f"Searching for: {query}"


# 3. UUID Converter with Query Parameters
# URL Example: http://127.0.0.1:5000/session/12345678-1234-5678-1234-567812345678?action=refresh
@app.route("/session/<uuid:session_id>")
def manage_session(session_id):
    action = request.args.get("action", "view")
    return f"Session UUID: {session_id} | Action Requested: {action}"


if __name__ == "__main__":
    app.run(debug=True)