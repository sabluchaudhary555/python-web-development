# Flask Installation Guide (Windows)

## What is Flask?

Flask is a lightweight Python web framework used to build web applications and APIs. It gives developers the essential tools needed for web development while keeping the overall structure simple and flexible, which is why it's popular among beginners as well as experienced developers building scalable web apps.

## Features of Flask

- **Built-in Development Server** — lets you run and test applications locally without any extra setup or third-party server software.
- **Routing Support** — maps URLs to specific Python functions easily using decorators like `@app.route()`.
- **Template Engine (Jinja2)** — helps create dynamic HTML pages using reusable templates instead of hardcoding HTML in Python.
- **Extension Support** — integrates smoothly with extensions such as Flask-SQLAlchemy for database handling and other added functionality.
- **RESTful Request Handling** — provides built-in tools to handle HTTP methods like GET, POST, PUT, and DELETE, making it suitable for building REST APIs.
- **Debug Mode** — automatically reloads the server on code changes and shows detailed error pages during development.

## Step 1: Check Python Installation

Before installing Flask, make sure Python is already installed on your system, since Flask depends on it. Run this in Command Prompt:

**Syntax:**
```bash
python --version
```

**Example:**
```bash
python --version
# Output: Python 3.12.4
```

If Python isn't installed, download it from the official Python website first and make sure it's added to your system PATH during setup.

## Step 2: Install Flask

Once Python is confirmed, open Command Prompt and install Flask using pip, Python's package manager. This command also pulls in Flask's required dependencies automatically.

**Syntax:**
```bash
pip install flask
```

**Example:**
```bash
pip install flask
# Output: Successfully installed flask-3.x.x Werkzeug-x.x.x Jinja2-x.x.x ...
```

If you're using a virtual environment (recommended), activate it first, then run the same command inside that environment so Flask installs locally to the project instead of system-wide.

## Step 3: Verify Installation

After installation finishes, confirm Flask was installed correctly by opening the Python interactive shell and importing it.

**Syntax:**
```python
import flask
```

**Example:**
```python
python
>>> import flask
>>> print(flask.__version__)
# Output: 3.0.3
```

If no error appears when importing, Flask has been installed successfully and is ready to use in your projects.

## Notes / Edge Cases

- If you get `pip is not recognized`, Python's Scripts folder isn't in your PATH — reinstall Python and check "Add Python to PATH," or use `py -m pip install flask` instead.
- Installing Flask without an active virtual environment installs it globally, which can cause version conflicts between different projects — always prefer a venv for real project work.
- A successful `import flask` with no output/errors is the confirmation — Flask doesn't print a success message on import.

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Check Python version | `python --version` | Confirms Python is installed before proceeding |
| Install Flask | `pip install flask` | Installs Flask + required dependencies via pip |
| Verify installation | `import flask` (in Python shell) | No error = successful installation |
| Check Flask version | `flask.__version__` | Confirms exact installed version |
| Virtual environment install | `venv\Scripts\activate` then `pip install flask` | Keeps Flask isolated to the current project |