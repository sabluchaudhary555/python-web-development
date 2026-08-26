# Flask — Routing & render_template (Complete Notes)

## 1. Routing in Flask

### What is Routing?

Routing is the mechanism that maps a specific URL to a Python function (called a **view function**). When a request comes in for a given URL, Flask checks its internal URL map and calls the matching function, whose return value becomes the HTTP response sent back to the browser.

### Basic Route

**Syntax:**
```python
@app.route(rule)
def view_function():
    return "response"
```

**Example:**
```python
@app.route("/")
def home():
    return "Welcome to the homepage!"
```
```
Visiting http://127.0.0.1:5000/ → "Welcome to the homepage!"
```

### Multiple Routes for the Same Function

A single view function can be bound to more than one URL by stacking decorators.

**Example:**
```python
@app.route("/")
@app.route("/home")
def home():
    return "Welcome!"
```
```
Both http://127.0.0.1:5000/ and http://127.0.0.1:5000/home return "Welcome!"
```

### Dynamic Routing (Variable Rules)

URL segments can be captured directly and passed into the view function as arguments, using angle brackets.

**Syntax:**
```python
@app.route("/<variable_name>")
def view_function(variable_name):
    return f"Value: {variable_name}"
```

**Example:**
```python
@app.route("/user/<username>")
def show_user(username):
    return f"Hello, {username}!"
```
```
Visiting /user/Sablu → "Hello, Sablu!"
```

### Type Converters in Dynamic Routes

By default, dynamic segments are treated as strings. Converters can restrict/convert the type of the captured value.

**Syntax:**
```python
@app.route("/<converter:variable_name>")
```

**Example:**
```python
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post ID: {post_id}"

@app.route("/price/<float:amount>")
def show_price(amount):
    return f"Price: {amount}"
```

| Converter | Accepts |
|---|---|
| `string` (default) | Any text without a slash |
| `int` | Positive integers |
| `float` | Positive floating-point numbers |
| `path` | Like `string`, but also accepts slashes |
| `uuid` | UUID strings |

**Example (`path` converter):**
```python
@app.route("/files/<path:filepath>")
def show_file(filepath):
    return f"File path: {filepath}"
```
```
Visiting /files/docs/2024/report.pdf → "File path: docs/2024/report.pdf"
(without 'path', the slashes would break the match)
```

### Restricting HTTP Methods

By default, a route only responds to `GET` requests. Other methods (like `POST`, for form submissions) must be explicitly allowed.

**Syntax:**
```python
@app.route(rule, methods=["GET", "POST"])
```

**Example:**
```python
from flask import request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Form submitted!"
    return "Login form here."
```

| Method | Purpose |
|---|---|
| `GET` | Retrieve data (default) |
| `POST` | Submit data (e.g. forms) |
| `PUT` | Update existing data |
| `DELETE` | Remove data |
| `PATCH` | Partially update data |

### `url_for()` — Generating URLs from Function Names

Instead of hardcoding URLs in links or redirects, `url_for()` builds the correct URL by referencing the view function's name — so if the route path changes later, everything using `url_for()` updates automatically.

**Syntax:**
```python
url_for('function_name', **kwargs)
```

**Example:**
```python
@app.route("/about")
def about():
    return "About page"

@app.route("/")
def home():
    return f"Go to About: {url_for('about')}"
```
```
Output: Go to About: /about
```

**With dynamic arguments:**
```python
url_for('show_user', username='Sablu')
# Output: /user/Sablu
```

**In templates:**
```html
<a href="{{ url_for('about') }}">About</a>
```

### Redirects

`redirect()` sends the browser to a different URL, commonly paired with `url_for()`.

**Syntax:**
```python
from flask import redirect, url_for

@app.route("/old-page")
def old_page():
    return redirect(url_for('new_page'))
```

**Example:**
```python
@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    return "Login page"
```
```
Visiting / immediately redirects to /login
```

### Query Parameters (`request.args`)

Data passed in the URL after a `?` (e.g. `/search?q=flask`) is accessed via `request.args`.

**Example:**
```python
from flask import request

@app.route("/search")
def search():
    query = request.args.get("q")
    return f"Searching for: {query}"
```
```
Visiting /search?q=flask → "Searching for: flask"
```

### Custom Error Pages

Routes can be defined for specific HTTP error codes using `@app.errorhandler()`.

**Example:**
```python
@app.errorhandler(404)
def page_not_found(e):
    return "Custom 404 page — page not found!", 404
```

### Strict Slashes Behavior

Flask treats trailing slashes as meaningful by default.

```python
@app.route("/about/")   # note trailing slash
def about():
    return "About page"
```
- Visiting `/about/` → works normally
- Visiting `/about` (no slash) → Flask automatically redirects to `/about/`
- If the route is defined **without** a trailing slash (`/about`), visiting `/about/` instead returns a 404

---

## 2. `render_template()`

### What is `render_template()`?

`render_template()` is a Flask function that loads an HTML file from the `templates/` folder, processes any Jinja2 syntax inside it, and returns the final rendered HTML as the response — this is how Flask serves real web pages instead of plain text strings.

### Basic Usage

**Syntax:**
```python
from flask import render_template

@app.route(rule)
def view_function():
    return render_template("filename.html")
```

**Example:**
```python
@app.route("/")
def home():
    return render_template("index.html")
```
```html
<!-- templates/index.html -->
<h1>Welcome to my Flask site!</h1>
```

**Requirement:** `index.html` must exist inside a folder literally named `templates/`, sitting directly next to the running `.py` file — otherwise Flask raises `jinja2.exceptions.TemplateNotFound`.

### Passing a Single Variable

**Syntax:**
```python
return render_template("file.html", variable_name=value)
```

**Example:**
```python
@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)
```
```html
<!-- welcome.html -->
<h1>Welcome, {{ name }}!</h1>
```

### Passing Multiple Variables

**Syntax:**
```python
return render_template("file.html", var1=value1, var2=value2)
```

**Example:**
```python
@app.route("/profile")
def profile():
    return render_template("profile.html", name="Sablu", role="Cybersecurity Lead")
```
```html
<p>Name: {{ name }}</p>
<p>Role: {{ role }}</p>
```

### Passing a List

**Example:**
```python
@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("about.html", sites=sites)
```
```html
<ul>
{% for site in sites %}
    <li>{{ site }}</li>
{% endfor %}
</ul>
```

### Passing a Dictionary

**Example:**
```python
@app.route("/user-info")
def user_info():
    info = {"name": "Sablu", "role": "Cybersecurity Lead"}
    return render_template("info.html", info=info)
```
```html
<ul>
{% for key, value in info.items() %}
    <li>{{ key }}: {{ value }}</li>
{% endfor %}
</ul>
```

### Passing Multiple Data Types Together

**Example:**
```python
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        username="Sablu",
        is_admin=True,
        notifications=["New message", "Profile updated"]
    )
```
```html
<h1>Hello, {{ username }}</h1>
{% if is_admin %}
    <p>Admin access granted.</p>
{% endif %}
<ul>
{% for note in notifications %}
    <li>{{ note }}</li>
{% endfor %}
</ul>
```

### `render_template_string()` — Rendering Without a File

Instead of loading a `.html` file, this renders a Jinja2 template directly from a string — useful for quick testing or dynamically generated templates.

**Syntax:**
```python
from flask import render_template_string

render_template_string(template_string, **context)
```

**Example:**
```python
@app.route("/quick-test")
def quick_test():
    return render_template_string("<h1>Hello, {{ name }}!</h1>", name="Sablu")
```
```
Output: Hello, Sablu! (rendered directly, no separate HTML file needed)
```

### Combining Routing + render_template (Full Example)

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/user/<username>")
def user_profile(username):
    return render_template("profile.html", username=username)

@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram']
    return render_template("about.html", sites=sites)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Notes / Edge Cases

- Route order matters when multiple rules could match — Flask checks routes in the order they're registered, though fixed paths (`/about`) and dynamic paths (`/<name>`) rarely truly conflict since Flask matches the most specific static rule first.
- `render_template()` file paths are relative to the `templates/` folder — you don't write `templates/index.html`, just `index.html`.
- Variables passed to `render_template()` are only accessible in **that specific render call** — they don't persist across other routes or requests.
- `url_for()` requires the exact **function name**, not the URL string — e.g. `url_for('about')`, not `url_for('/about')`.
- A dynamic route like `/<int:id>` will return a 404 (not a Python error) if a non-integer value is passed in the URL, since the converter rejects the match entirely.
- `render_template_string()` should generally be avoided for user-supplied input, since rendering untrusted strings as templates can introduce Server-Side Template Injection (SSTI) vulnerabilities.

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Basic route | `@app.route("/")` | Maps URL to function |
| Multiple routes, one function | Stack `@app.route()` decorators | One function, multiple URLs |
| Dynamic route | `@app.route("/<name>")` | Captures URL segment as function argument |
| Type converter | `@app.route("/<int:id>")` | Restricts/converts captured value's type |
| Path converter | `@app.route("/<path:filepath>")` | Allows slashes inside the captured segment |
| Restrict HTTP methods | `@app.route("/", methods=["GET","POST"])` | Defaults to GET only if unspecified |
| Generate URL by function name | `url_for('function_name')` | Avoids hardcoding URLs |
| Redirect | `redirect(url_for('function_name'))` | Sends browser to a different route |
| Query parameters | `request.args.get("key")` | Reads `?key=value` from the URL |
| Custom error page | `@app.errorhandler(404)` | Defines a custom response for an HTTP error code |
| Render a template file | `render_template("file.html")` | Loads and renders HTML from `templates/` |
| Pass one variable | `render_template("f.html", x=value)` | Injects a variable into the template |
| Pass multiple variables | `render_template("f.html", a=1, b=2)` | Multiple named variables in one call |
| Render from a string | `render_template_string("...")` | Renders Jinja2 without a separate file |