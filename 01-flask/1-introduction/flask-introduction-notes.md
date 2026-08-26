# Flask — Introduction, Django vs Flask, and Installation & Setup

## 1. Introduction to Flask

### What is Flask?

Flask is a lightweight, open-source Python web framework used to build web applications and APIs. It's classified as a **micro-framework**, meaning it provides only the core essentials needed to build a web app — routing, request handling, and templating — without bundling in extra tools like an ORM, authentication system, or admin panel by default. Anything beyond the basics is added through extensions, giving the developer full control over what goes into the project.

Flask was created by Armin Ronacher and built on top of two key components:
- **Werkzeug** — a WSGI (Web Server Gateway Interface) toolkit that handles the low-level details of receiving HTTP requests and sending responses.
- **Jinja2** — the templating engine used to generate dynamic HTML pages.

### Why Flask is Popular

- **Minimal and unopinionated** — Flask doesn't force a specific project structure or way of doing things, unlike more rigid frameworks.
- **Easy to learn** — a working Flask app can be written in just a few lines of code, making it beginner-friendly.
- **Highly extensible** — through Flask extensions (Flask-SQLAlchemy for databases, Flask-Login for authentication, Flask-Mail for emails, etc.), it can scale up to handle complex applications.
- **Great for APIs** — Flask is widely used to build RESTful APIs due to its simplicity and flexibility with request/response handling.
- **Built-in development server** — comes with a lightweight server for local testing, so no external server software is needed during development.

### Key Features

- **Built-in Development Server & Debugger** — run and test the app locally with `app.run()`; the debugger shows detailed error tracebacks in the browser when `debug=True`.
- **Routing System** — URLs are mapped to Python functions using the `@app.route()` decorator, making endpoint definitions clean and readable.
- **Jinja2 Templating** — allows embedding Python-like logic (loops, conditionals, variables) directly inside HTML files to generate dynamic pages.
- **RESTful Request Handling** — built-in support for handling HTTP methods (GET, POST, PUT, DELETE, etc.), making it suitable for both websites and APIs.
- **Extension Ecosystem** — official and community-built extensions add features like database ORM, form validation, authentication, and more, only when needed.
- **WSGI Compliant** — Flask apps can be deployed on any WSGI-compatible server (like Gunicorn or uWSGI) for production use.
- **Built-in Development Server** — quick local testing without needing to configure a separate web server.

### Where Flask is Used

- Small to medium web applications
- RESTful APIs and microservices
- Prototypes and MVPs (Minimum Viable Products)
- Backend for single-page applications (paired with a frontend framework like React)
- Machine learning model deployment (commonly used to serve ML models as APIs)

### A Minimal Flask App (Preview)

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```
This tiny snippet is enough to start a working local web server — a good illustration of how minimal Flask's core actually is.

---

## 2. Flask vs Django

### Overview

Both Flask and Django are Python web frameworks, but they take fundamentally different approaches to how much structure and built-in functionality they provide.

- **Django** is a high-level, full-stack web framework following the "batteries-included" philosophy — it ships with authentication, an ORM, an admin interface, and more, all built in.
- **Flask** is a lightweight, micro web framework that provides only the essentials, leaving the rest of the architecture and tooling decisions to the developer.

### Detailed Comparison

| Aspect | Django | Flask |
|---|---|---|
| **Framework Type** | Full-stack web framework | Micro web framework |
| **Architecture** | Enforces Model-View-Template (MVT) | No enforced architecture — developer decides |
| **Built-in Features** | Many (auth, admin, ORM, forms) included by default | Minimalistic — only essentials, extensions for the rest |
| **Admin Panel** | Built-in, auto-generated | Not built-in — needs third-party extension |
| **ORM** | Built-in, powerful (Django ORM) | Not built-in — commonly uses Flask-SQLAlchemy |
| **Template Engine** | Django Template Language (DTL) | Jinja2 (which DTL was inspired by) |
| **Security** | Built-in protections (CSRF, XSS, SQL injection) enabled by default | Requires manual implementation or extensions |
| **Scalability** | Well-suited for large-scale applications | Best for small to medium projects (can scale with effort) |
| **Community Support** | Large, long-established | Strong, but generally smaller in scope |
| **Flexibility** | Less flexible, more opinionated | Highly flexible, unopinionated |
| **Learning Curve** | Steeper — many conventions to learn | Easier — simpler to start with |
| **Project Structure** | Fixed structure enforced (apps, settings.py, etc.) | No fixed structure — organize however you prefer |
| **Routing** | URL patterns defined in `urls.py` | Routes defined directly via `@app.route()` decorators |
| **Best Fit** | Large applications, content-heavy sites, admin-driven systems | APIs, microservices, small apps, learning projects |

### When to Choose Which

- **Choose Django** when building a large-scale application that needs built-in authentication, an admin panel, and strong security defaults without assembling every piece manually — e.g., a content management system, e-commerce platform, or enterprise application.
- **Choose Flask** when building something smaller, a REST API, or a project where full control over architecture and third-party libraries matters more than built-in convenience — e.g., a microservice, a prototype, or a machine learning model API.

### Analogy
Django is like buying a fully furnished house — everything is included, but you live by the existing layout. Flask is like buying an empty plot of land — you decide exactly what goes where, but you're responsible for building it all yourself.

---

## 3. Installation & Setup of Flask (Windows)

### Prerequisite: Verify Python Installation

Flask requires Python to already be installed on the system.

**Syntax:**
```bash
python --version
```

**Example:**
```bash
python --version
# Output: Python 3.12.4
```

If Python isn't installed, download it from the official Python website and make sure **"Add Python to PATH"** is checked during setup — this avoids `pip is not recognized` errors later.

### Step 1: Create a Virtual Environment (Recommended)

A virtual environment keeps Flask and its dependencies isolated to a single project, preventing version conflicts between different projects on the same machine.

**Syntax:**
```bash
python -m venv <environment_name>
```

**Example:**
```bash
python -m venv venv
```
This creates a `venv/` folder containing an isolated Python environment.

### Step 2: Activate the Virtual Environment

**Syntax (Windows - PowerShell/CMD):**
```bash
venv\Scripts\activate
```

**Example:**
```bash
venv\Scripts\activate
# Prompt changes to show (venv) prefix, confirming it's active
```

To deactivate later:
```bash
deactivate
```

### Step 3: Install Flask

With the virtual environment active, install Flask using pip.

**Syntax:**
```bash
pip install flask
```

**Example:**
```bash
pip install flask
# Output: Successfully installed flask-3.x.x Werkzeug-x.x.x Jinja2-x.x.x ...
```

### Step 4: Verify the Installation

Open the Python interactive shell and import Flask to confirm it installed correctly.

**Syntax:**
```python
import flask
print(flask.__version__)
```

**Example:**
```python
python
>>> import flask
>>> print(flask.__version__)
# Output: 3.0.3
```
No errors on import = Flask is successfully installed.

### Step 5: Create a Minimal App and Run It

**`app.py`:**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

**Run it:**
```bash
python app.py
```

**Expected output:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Open a browser and visit `http://127.0.0.1:5000` — the page should display **"Hello, Flask!"**.

### Project Folder Structure (Standard Convention)

```
project-folder/
├── venv/                  ← virtual environment (not pushed to GitHub)
├── app.py                 ← main Flask application file
├── templates/              ← HTML files (Flask looks for this folder by name)
│   └── index.html
├── static/                 ← CSS, JS, images, videos, audio
│   ├── style.css
│   └── script.js
└── requirements.txt        ← list of installed dependencies (for sharing/deploying)
```

### Generating `requirements.txt` (for sharing the project)

**Syntax:**
```bash
pip freeze > requirements.txt
```
This creates a file listing all installed packages and their versions, so anyone else can recreate the same environment using:
```bash
pip install -r requirements.txt
```

---

## Notes / Edge Cases

- If `pip` isn't recognized, use `py -m pip install flask` instead, or reinstall Python with "Add to PATH" checked.
- Installing Flask **without** an active virtual environment installs it system-wide (globally) — this works but risks version conflicts across unrelated projects; always prefer a `venv`.
- A successful `import flask` produces **no output** — the absence of an error is the confirmation, not a printed success message.
- The `templates/` and `static/` folder names are **not arbitrary conventions** — Flask's `Flask(__name__)` constructor looks for these exact folder names automatically; renaming them requires explicitly overriding `template_folder`/`static_folder` in the constructor.

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Check Python version | `python --version` | Confirms Python is installed |
| Create virtual environment | `python -m venv venv` | Isolates dependencies per project |
| Activate venv (Windows) | `venv\Scripts\activate` | Must be active before installing packages |
| Deactivate venv | `deactivate` | Exits the virtual environment |
| Install Flask | `pip install flask` | Installs Flask + dependencies |
| Verify installation | `import flask` (Python shell) | No error = success |
| Check Flask version | `flask.__version__` | Confirms exact version installed |
| Run a Flask app | `python app.py` | Starts the development server |
| Default local URL | `http://127.0.0.1:5000` | Where the dev server runs by default |
| Enable auto-reload + debug info | `app.run(debug=True)` | Auto-restarts server on code changes |
| Export dependencies | `pip freeze > requirements.txt` | Lists installed packages for sharing |
| Install from requirements | `pip install -r requirements.txt` | Recreates the same environment elsewhere |
| Django vs Flask — full-stack vs micro | N/A | Django = batteries-included; Flask = minimal, extend as needed |