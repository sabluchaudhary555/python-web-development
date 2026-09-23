# Flask — Forms

## 1. What is a Form in Flask?

A form is how users submit data to a Flask application — usernames, passwords, search queries, file uploads, etc. Flask itself doesn't render forms (that's plain HTML), but it provides the tools to receive and process submitted form data through the `request` object. For more advanced validation and security, Flask projects commonly add the **Flask-WTF** extension on top of plain HTML forms.

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

```python
from flask import Flask, request, render_template

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        value = request.form.get("field_name")
        return f"Received: {value}"
    return render_template("form.html")
```

- `methods=["GET", "POST"]` — lets the same route serve the empty form (GET) and handle its submission (POST).
- `request.method` — checks which HTTP method the current request used, so the route branches accordingly.
- `request.form.get("field_name")` — safely reads a submitted field's value.

### Full Example — Signup Form

`app.py`:

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

`templates/signup.html`:

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

```python
request.form.get("field_name")          # returns None if missing (safe)
request.form["field_name"]              # raises KeyError if missing (risky)
```

- `.get()` — the safe way to read a field; returns `None` (or a default) instead of crashing if the field wasn't submitted.
- `["field_name"]` — bracket access; raises `KeyError` if the field is missing, so it's riskier for real apps.

Example:

```python
username = request.form.get("username")           # safe
username = request.form["username"]                # crashes if field missing
```

Getting a default value if missing:

```python
role = request.form.get("role", "user")   # defaults to "user" if not submitted
```

### Handling Multiple Values (Checkboxes)

A checkbox group with the same `name` submits multiple values, which need `getlist()` instead of `.get()`.

```html
<input type="checkbox" name="hobbies" value="reading"> Reading
<input type="checkbox" name="hobbies" value="gaming"> Gaming
```

```python
hobbies = request.form.getlist("hobbies")
# Output: ['reading', 'gaming'] if both were checked
```

- `.getlist("name")` — returns every value submitted under that field name, as a list; needed whenever multiple inputs can share one name.

### Handling a Single Selection (Radio Buttons)

Radio buttons sharing the same `name` let the user pick only one option — read the same way as any other field, with `.get()`.

```html
<label>Gender</label>
<input type="radio" name="gender" value="Male" checked> Male
<input type="radio" name="gender" value="Female"> Female
```

```python
gender = request.form.get("gender")
# Output: "Male" or "Female", depending on which was selected
```

Checking whether a checkbox was ticked at all (no value needed):

```python
newsletter = "Yes" if request.form.get("newsletter") else "No"
# A single, un-grouped checkbox only sends a value when checked — this pattern
# safely converts "checked / not checked" into a clean Yes/No without KeyError risk
```

### File Uploads — `request.files`

Forms that upload files need `enctype="multipart/form-data"` and are read via `request.files`, not `request.form`.

```html
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="uploaded_file">
    <button type="submit">Upload</button>
</form>
```

```python
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("uploaded_file")
    if file:
        file.save(f"uploads/{file.filename}")
        return "File uploaded successfully!"
    return "No file uploaded."
```

- `enctype="multipart/form-data"` — required on the `<form>` tag itself, or the file never reaches `request.files`.
- `request.files.get("name")` — retrieves the uploaded file object (not its raw bytes) by field name.
- `file.save(path)` — writes the uploaded file to disk at the given path.

### Sanitizing Uploaded Filenames — `secure_filename()`

A file's original filename (`file.filename`) comes directly from the user's browser/OS and cannot be trusted — it may contain unsafe characters, path traversal sequences (`../../`), or unexpected symbols. `secure_filename()` from Werkzeug strips these out before the file is saved.

```python
from werkzeug.utils import secure_filename

safe_name = secure_filename(file.filename)
```

- `secure_filename(file.filename)` — takes the raw, untrusted filename and returns a cleaned version safe to save on the server's filesystem.

Example:

```python
from werkzeug.utils import secure_filename

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["uploaded_file"]
    filename = secure_filename(file.filename)
    file.save(filename)
    return f"File uploaded successfully! Saved as: {filename}"
```

**Important:** Always sanitize with `secure_filename()` before calling `file.save()` — saving a raw, unsanitized filename is a security risk (e.g. a malicious filename like `../../etc/passwd` could attempt to write outside the intended folder).

### File Upload Validation — `FileRequired` & `FileAllowed` (Flask-WTF)

Plain `request.files` upload has no built-in way to restrict file type or enforce that a file was actually submitted. Flask-WTF's `flask_wtf.file` module adds validators specifically for `FileField`, so invalid uploads are rejected before they ever reach your save logic.

```python
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    profile_pic = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
```

- `FileField` — the Flask-WTF field type for file uploads, used instead of a plain HTML `<input type="file">`.
- `FileRequired()` — validator that fails if no file was submitted at all.
- `FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')` — validator that only accepts the listed file extensions; the second argument is the error message shown if the file type doesn't match.

Example — using it in a route:

```python
@app.route("/upload-profile", methods=["GET", "POST"])
def upload_profile():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.profile_pic.data.filename)
        form.profile_pic.data.save(f"uploads/{filename}")
        return "Profile picture uploaded!"
    return render_template("upload.html", form=form)
    # Output (on invalid file type): form.profile_pic.errors -> ['Images only!']
```

**Note:** `FileAllowed`/`FileRequired` still don't replace `secure_filename()` — extension checking and filename sanitization solve two different problems, so both are used together.

### Max File Size Limit — `MAX_CONTENT_LENGTH`

By default, Flask places no limit on how large an uploaded file (or request body) can be — a user could upload an extremely large file and exhaust server memory or disk space. Setting `MAX_CONTENT_LENGTH` caps the total request size Flask will accept.

```python
# 16 Megabytes limit
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
```

- `app.config['MAX_CONTENT_LENGTH']` — the maximum allowed size, in bytes, of an incoming request (including any uploaded file).
- `16 * 1024 * 1024` — a readable way to express 16 MB in bytes, instead of writing the raw number.

Example:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.errorhandler(413)
def too_large(e):
    return "File is too large! Max allowed size is 16MB.", 413
    # Output: Flask automatically returns HTTP 413 if the limit is exceeded,
    # this handler just customizes the response message
```

**Edge case:** if `MAX_CONTENT_LENGTH` is exceeded, Flask raises a `413 Request Entity Too Large` error automatically — the view function's code doesn't even run, so validation logic inside the route never gets a chance to reject the file first.

## 4. Basic Server-Side Validation (Plain HTML)

Without an extension, validation must be written manually.

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

Using HTML5 built-in validation (browser-side, not a substitute for server checks):

```html
<input type="email" name="email" required>
<input type="password" name="password" minlength="8" required>
```

**Important:** HTML5 `required`/`minlength` only prevents submission from a normal browser — it does not protect against malicious or scripted requests bypassing the form entirely. Server-side validation is still mandatory.

## 5. Flash Messages — Showing Feedback After Submission

Flask's `flash()` lets you show one-time messages (like "Signup successful!" or "Invalid email") after a redirect, commonly used with forms.

```python
from flask import flash

flash("message", "category")
```

- `flash("message", "category")` — queues a one-time message tied to the current session; `category` is a label (like `"success"` or `"error"`) used for styling.

Example:

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

Displaying flash messages in a template:

```jinja
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <p class="{{ category }}">{{ message }}</p>
        {% endfor %}
    {% endif %}
{% endwith %}
```

**Important:** `app.secret_key` must be set — `flash()` relies on Flask's session system, which requires a secret key to sign session cookies securely.

## 6. Flask-WTF — Form Handling with an Extension (Advanced)

Flask-WTF wraps the WTForms library to provide form classes, built-in validation, and CSRF protection — reducing manual `request.form` handling and boilerplate validation.

### Installation

```bash
pip install flask-wtf
```

### Basic Setup

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
```

- `FlaskForm` — the base class every Flask-WTF form inherits from; wires up CSRF protection automatically.
- `StringField`, `PasswordField`, `SubmitField` — field types representing different input widgets.
- `DataRequired`, `Email`, `Length` — validator classes attached to fields to enforce rules.

### Defining a Form Class

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

```jinja
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
| `RadioField` | Group of radio buttons for a single selection |
| `DecimalField` | Input field for decimal/numeric values |
| `FileField` | File upload |
| `SubmitField` | Submit button |

Example — using `RadioField` and `SelectField`:

```python
from wtforms import RadioField, SelectField

class ProfileForm(FlaskForm):
    gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female")])
    country = SelectField("Country", choices=[("IN", "India"), ("US", "United States"), ("UK", "United Kingdom")])
```

### Dynamic Choices in `SelectField`

Real apps rarely hardcode dropdown options — they're usually populated from the database, and the list of valid choices can change over time. `SelectField.choices` can be assigned dynamically, after the form object is created, instead of being fixed inside the class definition.

```python
form = ProfileForm()
# Form display se pehle database se populate karna
form.country.choices = [(c.id, c.name) for c in Country.query.all()]
```

- `form.country.choices` — a list of `(value, label)` tuples; reassigning it after creating the form instance overrides whatever was set (or left empty) in the class definition.
- `[(c.id, c.name) for c in Country.query.all()]` — builds the choices list from database rows, so the dropdown always reflects current data instead of a fixed hardcoded list.

Example — full route with dynamic choices:

```python
@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProfileForm()
    form.country.choices = [(c.id, c.name) for c in Country.query.all()]

    if form.validate_on_submit():
        selected_country_id = form.country.data
        return f"Selected country ID: {selected_country_id}"
    return render_template("profile.html", form=form)
```

**Edge case:** `choices` must be set on every request before the form is validated or rendered — if it's left empty (e.g. only set on GET but not POST), `validate_on_submit()` will fail because the submitted value won't match any valid choice.

### Common Validators

| Validator | Purpose |
|---|---|
| `DataRequired()` / `InputRequired()` | Field must not be empty (either name works; `InputRequired` checks raw input, `DataRequired` checks processed data) |
| `Email()` | Must be a valid email format |
| `Length(min=, max=)` | Restricts input length |
| `EqualTo("field_name")` | Must match another field (e.g. confirm password) |
| `NumberRange(min=, max=)` | Restricts numeric range |

Example — password confirmation:

```python
from wtforms.validators import EqualTo

class SignupForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
```

### Custom Validators

Beyond the built-in validators, a custom validator function can enforce application-specific rules that don't have a ready-made validator.

```python
from wtforms.validators import ValidationError

def validate_function_name(form, field):
    if <condition fails>:
        raise ValidationError("Error message")
```

- `def validate_function_name(form, field)` — a plain function taking the whole form and the specific field being validated.
- `raise ValidationError("message")` — raising this inside the function is how WTForms registers a failed validation, with the given message shown as the field's error.

Example — restricting a username to letters only:

```python
from wtforms import StringField
from wtforms.validators import ValidationError

def validate_username(form, field):
    if not field.data.isalpha():
        raise ValidationError("Username must contain only letters.")

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[validate_username])
```

The function receives the form and field objects, checks a condition against `field.data`, and raises `ValidationError` with a message if validation fails — it's attached to a field the same way a built-in validator is, just passed as a plain function instead of a class instance.

### Securing Passwords Before Storage

Raw passwords should never be stored as plain text. `generate_password_hash()` from Werkzeug converts a password into a secure hash before saving it.

```python
from werkzeug.security import generate_password_hash

hashed = generate_password_hash(password)
```

- `generate_password_hash(password)` — takes a plain-text password and returns a one-way hashed string, safe to store in a database.

Example:

```python
from werkzeug.security import generate_password_hash

if form.validate_on_submit():
    hashed_password = generate_password_hash(form.password.data)
    # Store hashed_password in the database — never the raw password
```

### Why Flask-WTF Over Plain HTML Forms

- **Built-in CSRF protection** — `form.hidden_tag()` automatically includes a CSRF token, protecting against cross-site request forgery attacks.
- **Server-side validation baked in** — `form.validate_on_submit()` runs all validators automatically; no manual `if not username` checks needed.
- **Error messages included** — `form.field.errors` gives ready-made error lists per field.
- **Less boilerplate** — one form class replaces repetitive `request.form.get()` + manual validation blocks.

## 7. CSRF Protection — What It Is and Explicit Setup

### What is CSRF?

Cross-Site Request Forgery (CSRF) is an attack where a malicious site tricks a logged-in user's browser into submitting a request to another site (where they're authenticated) without their knowledge — potentially performing unwanted actions like changing account settings or making transactions on their behalf.

### How CSRF Tokens Prevent This

A CSRF token is a unique, server-generated value embedded in a form. On submission, the server checks that the token matches — a forged request from an attacker's site won't have this valid token, so it gets rejected automatically.

### Enabling CSRF Protection Explicitly — `CSRFProtect`

While `FlaskForm` + `form.hidden_tag()` already handles CSRF automatically for its own forms, `CSRFProtect(app)` enables app-wide CSRF protection, covering the whole application consistently.

```python
from flask_wtf import CSRFProtect

app.secret_key = "your_secret_key"   # required
csrf = CSRFProtect(app)
```

- `CSRFProtect(app)` — attaches CSRF checking to every state-changing request in the app, not just routes that use `FlaskForm`.
- `app.secret_key` — required so Flask can sign the CSRF token securely; without it, CSRF checks can't function.

Example — comparing a protected form vs an unprotected one:

```python
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "your_secret_key"
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        flash(f"Hello {form.name.data}!", "success")
    return render_template("index.html", form=form)

# A plain route NOT using FlaskForm has no CSRF protection by default
@app.route("/unprotected_form", methods=["POST"])
def unprotected_form():
    name = request.form.get("Name", "").strip()
    return f"Hello {name} from Unprotected Form!"
```

```html
<!-- Protected: uses FlaskForm + hidden_tag(), CSRF-checked automatically -->
<form action="{{ url_for('index') }}" method="POST">
    {{ form.hidden_tag() }}
    {{ form.name() }}
    {{ form.submit() }}
</form>

<!-- Unprotected: plain HTML form, no CSRF token, no validation against forgery -->
<form action="{{ url_for('unprotected_form') }}" method="POST">
    <input type="text" name="Name" required>
    <button type="submit">Submit</button>
</form>
```

Submitting the protected form without a valid CSRF token (e.g. a forged request from elsewhere) results in a rejection error — this is the protection working as intended.

### CSRF Token with AJAX / JavaScript (Fetch API)

A form can return JSON directly (see the section below), but when the frontend sends data via JavaScript (`fetch` or `axios`) instead of a normal form submission, there's no `form.hidden_tag()` involved — so the CSRF token must be sent manually as a request header whenever `CSRFProtect(app)` is enabled.

```javascript
// Header required when CSRFProtect(app) is enabled
fetch('/submit', {
    method: 'POST',
    headers: {
        'X-CSRFToken': '{{ csrf_token() }}',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ data: "value" })
});
```

- `'X-CSRFToken': '{{ csrf_token() }}'` — `csrf_token()` is a Jinja-available function that generates a valid CSRF token; it's embedded here as a request header instead of a hidden form field.
- `'Content-Type': 'application/json'` — tells Flask the request body is JSON, not standard form-encoded data, so it should be read via `request.get_json()` server-side rather than `request.form`.
- `body: JSON.stringify({...})` — converts the JavaScript object into a JSON string to send in the request body.

Example — matching server-side route:

```python
@app.route("/submit", methods=["POST"])
def submit_ajax():
    data = request.get_json()
    return {"received": data.get("data")}
    # Output (JSON): {"received": "value"}
```

**Edge case:** without sending `X-CSRFToken` on an AJAX request, `CSRFProtect(app)` rejects the request with a 400 error (`CSRF token is missing`) even though no visible `<form>` was involved — the token requirement applies to the request itself, not just HTML forms.

### Returning a Dictionary Directly (Auto-JSON Response)

A Flask route can return a plain Python `dict` directly — Flask automatically converts it into a JSON response, without needing to call `jsonify()` manually.

```python
@app.route("/read-form", methods=["POST"])
def read_form():
    email = request.form.get("userEmail")
    return {
        "email": email,
        "message": "Form submitted successfully!"
    }
    # Automatically sent to the browser as a JSON response
```

Useful when a form is submitted via JavaScript/AJAX and the frontend expects a structured JSON reply instead of an HTML page.

## 8. Redirect After POST (Post/Redirect/Get Pattern)

A common best practice: after processing a form submission, redirect to another page instead of directly returning a response. This prevents duplicate submissions if the user refreshes the page.

```python
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # process form data
        return redirect(url_for("dashboard"))   # redirect instead of returning directly
    return render_template("signup.html")
```

Without this, refreshing the result page would re-trigger the browser's "Resubmit form?" prompt and could cause duplicate submissions (e.g. double account creation).

## Notes / Edge Cases

- Always use `.get()` instead of `["key"]` on `request.form` — missing fields raise `KeyError` with the bracket syntax, crashing the app instead of failing gracefully.
- `enctype="multipart/form-data"` is required on the `<form>` tag for file uploads to work — without it, `request.files` will be empty even if a file was selected.
- `app.secret_key` is required for both `flash()` and Flask-WTF's CSRF protection — without it, you'll get a `RuntimeError: The session is unavailable` or similar error.
- Never rely solely on HTML5 `required`/`pattern` attributes for validation — they're easily bypassed by disabling JavaScript or sending requests directly (e.g. via curl/Postman).
- `form.validate_on_submit()` only returns `True` on a POST request where all validators pass — on a GET request, it's always `False`, which is why the same route can safely serve both the empty form and handle its submission.
- Checkbox fields not checked at all are not included in `request.form` — always account for this with `.get()` or `getlist()`, never assume a key will exist.
- Never save an uploaded file using its raw `file.filename` — always pass it through `secure_filename()` first to strip unsafe characters and path traversal attempts.
- A route can return `{...}` (a plain dict) directly for a JSON response — Flask auto-converts it, no manual `jsonify()` call needed.
- `CSRFProtect(app)` protects the whole app broadly; `FlaskForm` + `form.hidden_tag()` already covers CSRF for its own forms — a plain `request.form`-based route (not using `FlaskForm`) has no CSRF protection unless `CSRFProtect(app)` is explicitly applied.
- Passwords must be hashed with `generate_password_hash()` before storage — never save or compare raw plain-text passwords.
- `FileAllowed`/`FileRequired` restrict file type and presence at the form-validation level, but don't replace `secure_filename()` — both are needed together for safe uploads.
- `MAX_CONTENT_LENGTH` rejects oversized requests before the view function even runs — a custom `413` error handler can be added, but the limit itself is enforced by Flask/Werkzeug automatically.
- AJAX/fetch requests bypass `form.hidden_tag()` entirely, so the CSRF token has to be sent manually as a header (`X-CSRFToken`) whenever `CSRFProtect(app)` is active — forgetting this is a common source of "CSRF token missing" errors on JS-driven forms.
- `SelectField.choices` must be (re)assigned on every request, not just once — if it's only set on GET, POST validation will fail since the submitted value won't be found in an empty choices list.

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Basic form tag | `<form method="POST" action="/url">` | POST for sensitive/data-modifying forms |
| Read form field | `request.form.get("name")` | Safe — returns `None` if missing |
| Read with default | `request.form.get("name", "default")` | Fallback value if field missing |
| Read multiple checkbox values | `request.form.getlist("name")` | For checkboxes sharing the same name |
| Read uploaded file | `request.files.get("name")` | Requires `enctype="multipart/form-data"` |
| Save uploaded file | `file.save("path/filename")` | Writes uploaded file to disk |
| Sanitize filename | `secure_filename(file.filename)` | Strips unsafe characters before saving a file |
| Restrict file type (Flask-WTF) | `FileAllowed(['jpg','png'], 'Images only!')` | Validator on `FileField`, rejects other extensions |
| Require a file (Flask-WTF) | `FileRequired()` | Fails validation if no file submitted |
| Limit upload/request size | `app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024` | Raises 413 automatically if exceeded |
| Show flash message | `flash("message", "category")` | Requires `app.secret_key` to be set |
| Display flash messages | `{% with messages = get_flashed_messages() %}` | Used in template to render flash output |
| Install Flask-WTF | `pip install flask-wtf` | Adds form classes + CSRF protection |
| Define a form class | `class MyForm(FlaskForm): ...` | Fields defined as class attributes |
| Validate submission | `form.validate_on_submit()` | True only on valid POST |
| CSRF token in template | `{{ form.hidden_tag() }}` | Required for Flask-WTF forms |
| CSRF token for AJAX/fetch | `headers: {'X-CSRFToken': '{{ csrf_token() }}'}` | Manual header needed since no `hidden_tag()` is rendered |
| Field errors in template | `{{ form.field.errors }}` | List of validation error messages |
| Match another field | `EqualTo("password")` | Used for confirm-password fields |
| Custom validator | `def validate_x(form, field): raise ValidationError(...)` | Enforces app-specific rules |
| Dynamic dropdown choices | `form.field.choices = [(c.id, c.name) for c in Model.query.all()]` | Populates `SelectField` from the database, not hardcoded |
| Hash a password | `generate_password_hash(password)` | Never store raw plain-text passwords |
| Return JSON directly | `return {"key": "value"}` | Flask auto-converts a dict to a JSON response |
| App-wide CSRF protection | `csrf = CSRFProtect(app)` | Protects all routes, not just FlaskForm-based ones |
| Prevent duplicate submission | `redirect(url_for(...))` after POST | Post/Redirect/Get pattern |