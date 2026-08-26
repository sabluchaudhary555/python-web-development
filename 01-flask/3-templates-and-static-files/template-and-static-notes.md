# Flask — Templates & Static Files (Complete Notes)

## 1. Templates in Flask

### What are Templates?

Templates are HTML files that Flask renders dynamically using the **Jinja2** templating engine. Instead of writing raw HTML strings inside Python code, templates let you keep HTML separate from application logic — Python passes data into the template, and Jinja2 syntax inside the HTML displays that data, loops over it, or conditionally shows content.

### The `templates/` Folder Requirement

Flask automatically looks for a folder named **exactly** `templates`, located in the **same directory** as the running Python file. This is a hard requirement — `render_template()` will raise `jinja2.exceptions.TemplateNotFound` if the folder is missing, misnamed, or in the wrong location.

**Required structure:**
```
project-folder/
├── app.py
└── templates/
    └── index.html
```

### Basic Template Rendering

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

### Passing Data into Templates

**Example:**
```python
@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)
```
```html
<!-- templates/welcome.html -->
<h1>Welcome, {{ name }}!</h1>
```

### Organizing Templates in Subfolders

For larger projects, templates can be grouped into subfolders inside `templates/` — the subfolder path is included when calling `render_template()`.

**Structure:**
```
templates/
├── index.html
└── auth/
    ├── login.html
    └── register.html
```

**Example:**
```python
@app.route("/login")
def login():
    return render_template("auth/login.html")
```

### Template Inheritance

Instead of repeating shared HTML (navbar, footer, layout) across every page, Jinja2 lets you define a **base/parent template** that other templates extend — keeping the codebase DRY (Don't Repeat Yourself).

**`templates/base.html` (parent template):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <nav>Home | About | Contact</nav>
    {% block content %}{% endblock %}
</body>
</html>
```

**`templates/about.html` (child template):**
```html
{% extends "base.html" %}

{% block title %}About Us{% endblock %}

{% block content %}
    <h2>About Us</h2>
    <p>This is the about page.</p>
{% endblock %}
```

**How it works:**
- `{% extends "base.html" %}` tells Jinja2 this template inherits the layout from `base.html`.
- `{% block name %}{% endblock %}` in the parent defines a **replaceable section**.
- The child template only needs to fill in its own `{% block %}` content — everything else (nav, structure) is inherited automatically.
- Changing the navbar in `base.html` updates it across every page that extends it, with no repeated edits.

**Extending a block instead of replacing it (`super()`):**
```html
{% block content %}
    {{ super() }}
    <p>Extra content added on top of the parent's block.</p>
{% endblock %}
```

### Including Other Templates

Unlike inheritance (which fills in blocks), `include` directly inserts one template's content into another — useful for reusable snippets like a navbar or footer that don't need block-based overriding.

**Example:**
```html
<!-- templates/navbar.html -->
<nav>Home | About | Contact</nav>

<!-- templates/index.html -->
{% include "navbar.html" %}
<h1>Welcome!</h1>
```

### Common Template Errors

| Error | Cause | Fix |
|---|---|---|
| `jinja2.exceptions.TemplateNotFound: file.html` | File doesn't exist inside `templates/`, or `templates/` isn't next to the running `.py` file | Create the file / move it to the correct folder |
| Variable shows blank | Variable name mismatch between Python and template | Ensure `render_template("f.html", x=value)` matches `{{ x }}` exactly |
| HTML tags shown as plain text | Auto-escaping is active (default, for security) | Use `{{ variable | safe }}` only for trusted content |

---

## 2. Static Files in Flask

### What are Static Files?

Static files are assets that don't change per request — CSS stylesheets, JavaScript files, images, videos, audio, fonts, etc. Flask serves these separately from templates, through a dedicated `static/` folder.

### The `static/` Folder Requirement

Just like `templates/`, Flask automatically looks for a folder named **exactly** `static`, located in the same directory as the running Python file.

**Required structure:**
```
project-folder/
├── app.py
├── static/
│   ├── style.css
│   ├── script.js
│   ├── images/
│   │   └── logo.png
│   ├── videos/
│   │   └── demo.mp4
│   └── audios/
│       └── sound.mp3
└── templates/
    └── index.html
```

### Referencing Static Files with `url_for()`

Static files should **never** be hardcoded (e.g. `<link href="/static/style.css">`). Instead, use `url_for('static', filename=...)`, which builds the correct path automatically and stays correct even if the app is deployed under a different base path later.

**Syntax:**
```html
{{ url_for('static', filename='path/inside/static/folder') }}
```

### Linking CSS

**Example:**
```html
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
```

### Linking JavaScript

**Example:**
```html
<body>
    ...
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
```

### Displaying an Image

**Example:**
```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

### Embedding a Video

**Example:**
```html
<video controls width="400">
    <source src="{{ url_for('static', filename='videos/demo.mp4') }}" type="video/mp4">
    Your browser does not support the video tag.
</video>
```

### Embedding Audio

**Example:**
```html
<audio controls>
    <source src="{{ url_for('static', filename='audios/sound.mp3') }}" type="audio/mpeg">
    Your browser does not support the audio tag.
</audio>
```

### Full Example — Template + Static Files Combined

**`app.py`:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

**`templates/index.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Static Demo</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Welcome to my Flask site</h1>
    <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="logo">
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

**`static/style.css`:**
```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
}
.logo {
    width: 150px;
}
```

**`static/script.js`:**
```javascript
console.log("Static JS loaded!");
```

### Custom Static Folder Name (Advanced)

By default Flask assumes `static/`, but this can be overridden when creating the app instance.

**Syntax:**
```python
app = Flask(__name__, static_folder="assets", static_url_path="/assets")
```

**Example:**
```python
app = Flask(__name__, static_folder="assets")
# Now Flask looks for a folder named "assets" instead of "static"
```

### Custom Templates Folder Name (Advanced)

Similarly, the templates folder name can be overridden too.

**Syntax:**
```python
app = Flask(__name__, template_folder="views")
```

---

## Notes / Edge Cases

- Both `templates/` and `static/` **must sit directly next to the Python file that's actually being run** — Flask does not search parent folders or subfolders for them automatically.
- `render_template()` paths are relative to `templates/` — you never write `templates/index.html`, just `index.html`.
- `url_for('static', filename=...)` paths are relative to `static/` — same rule, never include `static/` in the `filename` argument itself.
- If a static file (CSS/JS) doesn't seem to update after editing, it's often a **browser caching issue** — hard refresh (`Ctrl+Shift+R`) or clear cache, since static assets are cached more aggressively than dynamic pages.
- Renaming a Python file or moving it to a different folder breaks its link to `templates/`/`static/` unless those folders move with it — this is one of the most common beginner mistakes (confirmed from real troubleshooting sessions).
- Auto-escaping in Jinja2 is **on by default** for security (prevents XSS) — don't disable it (`| safe`) on any untrusted or user-submitted content.

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Render a template | `render_template("file.html")` | Loads HTML from `templates/` folder |
| Pass a variable | `render_template("f.html", x=value)` | Makes `x` available as `{{ x }}` in the template |
| Template inheritance | `{% extends "base.html" %}` | Reuses a shared parent layout |
| Define block | `{% block name %}...{% endblock %}` | Marks a replaceable section |
| Extend parent block | `{{ super() }}` | Keeps parent content, adds more to it |
| Include a template | `{% include "file.html" %}` | Inserts another template's content directly |
| Organize templates | `render_template("folder/file.html")` | Supports subfolders inside `templates/` |
| Reference static file | `{{ url_for('static', filename='x') }}` | Builds correct path to any file in `static/` |
| Link CSS | `<link href="{{ url_for('static', filename='style.css') }}">` | Loads stylesheet from static folder |
| Link JS | `<script src="{{ url_for('static', filename='script.js') }}">` | Loads JavaScript from static folder |
| Display image | `<img src="{{ url_for('static', filename='images/x.png') }}">` | Serves image from `static/images/` |
| Embed video | `<video><source src="{{ url_for('static', filename='videos/x.mp4') }}"></video>` | Serves video from `static/videos/` |
| Embed audio | `<audio><source src="{{ url_for('static', filename='audios/x.mp3') }}"></audio>` | Serves audio from `static/audios/` |
| Custom static folder | `Flask(__name__, static_folder="assets")` | Overrides default `static/` folder name |
| Custom templates folder | `Flask(__name__, template_folder="views")` | Overrides default `templates/` folder name |