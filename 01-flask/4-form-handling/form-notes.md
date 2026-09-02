# Flask — Forms 

## 1. What is a Form in Flask?

A form is how users submit data to a Flask application — usernames, passwords, search queries, file uploads, etc. Flask itself doesn't render forms (that's plain HTML), but it provides the tools to **receive and process** submitted form data through the `request` object. For more advanced validation and security, Flask projects commonly add the **Flask-WTF** extension on top of plain HTML forms.

## 2. Basic HTML Form (Plain, No Extension)

### Anatomy of a Form

```html
<form method="POST" action="/submit">
    <input type="text" name="username">
    <button type="submit">Submit</button>
</form>
```

| Attribute | Purpose |
|---|---|
| `method` | HTTP method used to send data — usually `GET` or `POST` |
| `action` | The URL the form data is sent to |
| `name` (on input) | The key used to retrieve that field's value in Flask |

### GET vs POST for Forms

- **GET** — form data is appended to the URL as query parameters (`?key=value`). Visible in the address bar, cacheable, should never be used for sensitive data (passwords).
- **POST** — form data is sent in the request body, not visible in the URL. Standard choice for login, signup, and any data-modifying form.

```html
<form method="GET" action="/search">     <!-- fine for search -->
<form method="POST" action="/login">     <!-- required for sensitive data -->
```

## 3. Handling a Form in Flask (Plain HTML)

### Basic Setup

**Syntax:**
```python
from flask import Flask, request, render_template

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        value = request.form.get("field_name")
        return f"Received: {value}"
    return render_template("form.html")
```

### Full Example — Signup Form

**`app.py`:**
```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        return f"Signup successful! Welcome, {username} ({email})"
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
```

**`templates/signup.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head><title>Sign Up</title></head>
<body>
    <h1>Create an Account</h1>
    <form method="POST" action="{{ url_for('signup') }}">
        <label>Username:</label>
        <input type="text" name="username" required><br>

        <label>Email:</label>
        <input type="email" name="email" required><br>

        <label>Password:</label>
        <input type="password" name="password" required><br>

        <button type="submit">Sign Up</button>
    </form>
</body>
</html>
```

### `request.form` — Reading Form Data

**Syntax:**
```python
request.form.get("field_name")          # returns None if missing (safe)
request.form["field_name"]              # raises KeyError if missing (risky)
```

**Example:**
```python
username = request.form.get("username")           # safe
username = request.form["username"]                # crashes if field missing
```

**Getting a default value if missing:**
```python
role = request.form.get("role", "user")   # defaults to "user" if not submitted
```

### Handling Multiple Values (Checkboxes)

A checkbox group with the same `name` submits multiple values, which need `getlist()` instead of `.get()`.

**Example:**
```html
<input type="checkbox" name="hobbies" value="reading"> Reading
<input type="checkbox" name="hobbies" value="gaming"> Gaming
```
```python
hobbies = request.form.getlist("hobbies")
# Output: ['reading', 'gaming'] if both were checked
```

### File Uploads — `request.files`

Forms that upload files need `enctype="multipart/form-data"` and are read via `request.files`, not `request.form`.

**HTML:**
```html
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="uploaded_file">
    <button type="submit">Upload</button>
</form>
```

**Python:**
```python
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("uploaded_file")
    if file:
        file.save(f"uploads/{file.filename}")
        return "File uploaded successfully!"
    return "No file uploaded."
```

## 4. Basic Server-Side Validation (Plain HTML)

Without an extension, validation must be written manually.

**Example:**
```python
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        if not username or not email:
            return "Error: All fields are required!", 400

        if "@" not in email:
            return "Error: Invalid email format!", 400

        return f"Welcome, {username}!"
    return render_template("signup.html")
```

**Using HTML5 built-in validation (browser-side, not a substitute for server checks):**
```html
<input type="email" name="email" required>
<input type="password" name="password" minlength="8" required>
```
**Important:** HTML5 `required`/`minlength` only prevents submission from a normal browser — it does **not** protect against malicious or scripted requests bypassing the form entirely. Server-side validation is still mandatory.

## 5. Flash Messages — Showing Feedback After Submission

Flask's `flash()` lets you show one-time messages (like "Signup successful!" or "Invalid email") after a redirect, commonly used with forms.

**Syntax:**
```python
from flask import flash

flash("message", "category")
```

**Example:**
```python
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your-secret-key"   # required for flash() to work

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Username is required!", "error")
            return redirect(url_for("signup"))
        flash("Signup successful!", "success")
        return redirect(url_for("home"))
    return render_template("signup.html")
```

**Displaying flash messages in a template:**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <p class="{{ category }}">{{ message }}</p>
        {% endfor %}
    {% endif %}
{% endwith %}
```

**Important:** `app.secret_key` **must** be set — `flash()` relies on Flask's session system, which requires a secret key to sign session cookies securely.

## 6. Flask-WTF — Form Handling with an Extension (Advanced)

Flask-WTF wraps the WTForms library to provide form classes, built-in validation, and CSRF protection — reducing manual `request.form` handling and boilerplate validation.

### Installation

```bash
pip install flask-wtf
```

### Basic Setup

**Syntax:**
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
```

### Defining a Form Class

**Example:**
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign Up")
```

### Using the Form in a Route

```python
app.secret_key = "your-secret-key"   # required by Flask-WTF for CSRF protection

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        return f"Signup successful! Welcome, {username}"
    return render_template("signup.html", form=form)
```

### Rendering the Form in a Template

```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- CSRF token, required -->

    {{ form.username.label }} {{ form.username() }}
    {% for error in form.username.errors %}
        <span class="error">{{ error }}</span>
    {% endfor %}

    {{ form.email.label }} {{ form.email() }}
    {% for error in form.email.errors %}
        <span class="error">{{ error }}</span>
    {% endfor %}

    {{ form.password.label }} {{ form.password() }}
    {% for error in form.password.errors %}
        <span class="error">{{ error }}</span>
    {% endfor %}

    {{ form.submit() }}
</form>
```

### Common WTForms Field Types

| Field | Purpose |
|---|---|
| `StringField` | Single-line text input |
| `PasswordField` | Password input (masked) |
| `TextAreaField` | Multi-line text input |
| `BooleanField` | Checkbox |
| `SelectField` | Dropdown menu |
| `FileField` | File upload |
| `SubmitField` | Submit button |

### Common Validators

| Validator | Purpose |
|---|---|
| `DataRequired()` | Field must not be empty |
| `Email()` | Must be a valid email format |
| `Length(min=, max=)` | Restricts input length |
| `EqualTo("field_name")` | Must match another field (e.g. confirm password) |
| `NumberRange(min=, max=)` | Restricts numeric range |

**Example — password confirmation:**
```python
from wtforms.validators import EqualTo

class SignupForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
```

### Why Flask-WTF Over Plain HTML Forms

- **Built-in CSRF protection** — `form.hidden_tag()` automatically includes a CSRF token, protecting against cross-site request forgery attacks.
- **Server-side validation baked in** — `form.validate_on_submit()` runs all validators automatically; no manual `if not username` checks needed.
- **Error messages included** — `form.field.errors` gives ready-made error lists per field.
- **Less boilerplate** — one form class replaces repetitive `request.form.get()` + manual validation blocks.

## 7. Redirect After POST (Post/Redirect/Get Pattern)

A common best practice: after processing a form submission, **redirect** to another page instead of directly returning a response. This prevents duplicate submissions if the user refreshes the page.

**Example:**
```python
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # process form data
        return redirect(url_for("dashboard"))   # redirect instead of returning directly
    return render_template("signup.html")
```
Without this, refreshing the result page would re-trigger the browser's "Resubmit form?" prompt and could cause duplicate submissions (e.g. double account creation).

---

## Notes / Edge Cases

- Always use `.get()` instead of `["key"]` on `request.form` — missing fields raise `KeyError` with the bracket syntax, crashing the app instead of failing gracefully.
- `enctype="multipart/form-data"` is **required** on the `<form>` tag for file uploads to work — without it, `request.files` will be empty even if a file was selected.
- `app.secret_key` is required for both `flash()` and Flask-WTF's CSRF protection — without it, you'll get a `RuntimeError: The session is unavailable` or similar error.
- Never rely solely on HTML5 `required`/`pattern` attributes for validation — they're easily bypassed by disabling JavaScript or sending requests directly (e.g. via curl/Postman).
- `form.validate_on_submit()` only returns `True` on a `POST` request where all validators pass — on a `GET` request, it's always `False`, which is why the same route can safely serve both the empty form and handle its submission.
- Checkbox fields not checked at all are **not included** in `request.form` — always account for this with `.get()` or `getlist()`, never assume a key will exist.

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Basic form tag | `<form method="POST" action="/url">` | POST for sensitive/data-modifying forms |
| Read form field | `request.form.get("name")` | Safe — returns `None` if missing |
| Read with default | `request.form.get("name", "default")` | Fallback value if field missing |
| Read multiple checkbox values | `request.form.getlist("name")` | For checkboxes sharing the same `name` |
| Read uploaded file | `request.files.get("name")` | Requires `enctype="multipart/form-data"` |
| Save uploaded file | `file.save("path/filename")` | Writes uploaded file to disk |
| Show flash message | `flash("message", "category")` | Requires `app.secret_key` to be set |
| Display flash messages | `{% with messages = get_flashed_messages() %}` | Used in template to render flash output |
| Install Flask-WTF | `pip install flask-wtf` | Adds form classes + CSRF protection |
| Define a form class | `class MyForm(FlaskForm): ...` | Fields defined as class attributes |
| Validate submission | `form.validate_on_submit()` | True only on valid POST |
| CSRF token in template | `{{ form.hidden_tag() }}` | Required for Flask-WTF forms |
| Field errors in template | `{{ form.field.errors }}` | List of validation error messages |
| Match another field | `EqualTo("password")` | Used for confirm-password fields |
| Prevent duplicate submission | `redirect(url_for(...))` after POST | Post/Redirect/Get pattern |