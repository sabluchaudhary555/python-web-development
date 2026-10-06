from flask import Flask

app = Flask(__name__)

# 1. String converter (Default: accepts any text without a slash)
@app.route("/user/<string:username>")
def show_user(username):
    return f"Username: {username}"


# 2. Integer converter (Accepts positive integers only; returns 404 if invalid)
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post ID: {post_id}"


# 3. Float converter (Accepts positive floating-point numbers)
@app.route("/price/<float:amount>")
def show_price(amount):
    return f"Price: {amount}"


# 4. Path converter (Accepts text, including forward slashes '/')
@app.route("/files/<path:filepath>")
def show_file(filepath):
    return f"File path: {filepath}"


# 5. UUID converter (Accepts valid Universally Unique Identifier strings)
@app.route("/session/<uuid:session_id>")
def show_session(session_id):
    return f"Session UUID: {session_id}"


if __name__ == "__main__":
    app.run(debug=True)