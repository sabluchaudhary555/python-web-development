from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# ----------------------------------------------------
# 1. Basic Static Route
# ----------------------------------------------------
@app.route("/")
def home():
    return "<h1>Welcome to the Flask App </h1>"


# ----------------------------------------------------
# 2. Dynamic Route with Default String Converter
# ----------------------------------------------------
@app.route("/user/<username>")
def show_user(username):
    return f"<h3>Hello, {username}!</h3>"


# ----------------------------------------------------
# 3. Dynamic Route with Type Converters (int, float, path)
# ----------------------------------------------------
@app.route("/post/<int:post_id>")
def show_post(post_id):
    # Non-integer value aane par Flask automatically 404 return karta hai
    return f"<p>Fetching Blog Post ID: <b>{post_id}</b></p>"


@app.route("/price/<float:amount>")
def show_price(amount):
    return f"<p>Product Price: <b>${amount:.2f}</b></p>"


@app.route("/files/<path:file_path>")
def show_file(file_path):
    # Slashes '/' ko ignore kiye bina pura path read karega
    return f"<p>Accessing File Path: <code>{file_path}</code></p>"


# ----------------------------------------------------
# 4. Query Parameters via request.args (e.g. /search?q=flask)
# ----------------------------------------------------
@app.route("/search")
def search():
    query = request.args.get("q", "Nothing")
    page = request.args.get("page", 1, type=int)
    return f"<p>Search Query: <b>{query}</b> | Page: <b>{page}</b></p>"


# ----------------------------------------------------
# 5. url_for & redirect without Templates
# ----------------------------------------------------
@app.route("/old-home")
def old_home():
    # Function name ke basis par dynamic URL bana kar redirect karta hai
    return redirect(url_for("home"))


# ----------------------------------------------------
# 6. In-Memory Rendering (render_template_string)
# ----------------------------------------------------
@app.route("/dashboard")
def dashboard():
    # Yahan koi alag file nahi hai, seedha string ke andar Jinja syntax execute hota hai
    template_code = """
        <h2>User Dashboard</h2>
        <p>User: {{ name }}</p>
        <p>Tech Stack:</p>
        <ul>
            {% for skill in skills %}
                <li>{{ skill }}</li>
            {% endfor %}
        </ul>
        <a href="{{ url_for('home') }}">Back to Home</a>
    """
    skills_list = ["Python", "Flask", "SQLAlchemy"]
    return render_template_string(template_code, name="Sablu", skills=skills_list)


# ----------------------------------------------------
# 7. Custom 404 Handler (Direct String)
# ----------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    return "<h2>404 Error: Page not found! Check your URL.</h2>", 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)