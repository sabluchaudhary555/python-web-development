# Flask App Configuration & Environment-Specific Configurations

## 1. What is Flask App Configuration?

Flask applications rely on configuration settings to manage database connections, security options, session behavior, file uploads, and debugging features. Flask provides a flexible configuration system that allows settings to be defined directly in code, loaded from external files, or managed through environment variables.

## 2. Basic Configuration Syntax

### Method 1 — Directly Assigning to `app.config`

The simplest way to configure a Flask app is by directly assigning values to `app.config`.

**Syntax:**
```python
app.config['CONFIG_NAME'] = 'value'
```

**Parameters:**
- `CONFIG_NAME` — the name of the setting to define. Flask has built-in keys like `DEBUG`, `SECRET_KEY`, and `SQLALCHEMY_DATABASE_URI`, but custom ones can also be created.
- `value` — the actual setting, which can be a string, boolean, integer, or even a dictionary.

### Method 2 — Loading from an External File

Flask allows configurations to be loaded from an external file, such as `config.py`.

**Syntax:**
```python
app.config.from_pyfile('config.py')
```

This approach helps keep configuration settings separate from the main application logic, making the code more organized and maintainable.

## 3. Custom Configuration Variables

Besides built-in configuration options, Flask supports custom configuration variables for storing application-specific settings. This helps centralize configurable values and reduces the need to hardcode them throughout the application.

**Example:**
```python
app.config['COMPANY_NAME'] = 'GeeksforGeeks'
app.config['ITEMS_PER_PAGE'] = 20
```

Accessing these values anywhere in the application:
```python
app.config['COMPANY_NAME']
app.config.get('ITEMS_PER_PAGE')
```
```
# Output: 'GeeksforGeeks', 20
```

## 4. Common Flask Configuration Categories

Configuration in Flask refers to setting up parameters that control various aspects of the application, including:

- **Security settings** — secret keys and session handling.
- **Database settings** — to connect and manage databases.
- **Debugging options** — to enable automatic reloading and error reporting.
- **Session management** — for handling user sessions.
- **File handling & uploads** — configuring file storage.

## 5. Setting Up a Secret Key

A secret key is crucial for security-related functions in Flask, such as protecting session cookies and securing form submissions.

**Syntax:**
```python
app.config['SECRET_KEY'] = 'your_secret_key'
```

This key should always be kept private and unique. In a production environment, it's recommended to store it in an environment variable instead of hardcoding it in the script.

## 6. Configuring a Database

Most Flask applications require a database. Flask supports SQLAlchemy for database management.

**Syntax:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

- `SQLALCHEMY_DATABASE_URI` defines the database type and location. In this example, an SQLite database is stored in a file named `database.db`.
- `SQLALCHEMY_TRACK_MODIFICATIONS` is set to `False` to improve performance by disabling tracking of modifications to objects.

**Using a different database (e.g. PostgreSQL):**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db_name'
```

## 7. Session Management Configuration

Flask provides session management to store user-related information across multiple requests. The default session type stores data in cookies, but it can be configured for better security and control.

**Syntax:**
```python
from datetime import timedelta

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
```

- `SESSION_TYPE` set to `filesystem` means session data will be stored on the server's file system instead of client-side cookies.
- `PERMANENT_SESSION_LIFETIME` sets how long a session remains active before expiring — here, 1 day.

## 8. Configuring JSON Responses

Flask returns JSON responses for APIs, and how that JSON data is handled can be configured.

**Syntax:**
```python
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
```

- `JSON_SORT_KEYS = False` prevents automatic sorting of keys in JSON responses, preserving the order in which data is added.
- `JSONIFY_PRETTYPRINT_REGULAR = True` ensures the JSON output is formatted in a human-readable way.

## 9. Loading Configurations from a File

Instead of setting configurations inside `app.py`, they can be stored in a separate configuration file named `config.py`.

**config.py:**
```python
SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
DEBUG = True
```

**Loading it into the Flask app:**
```python
app.config.from_pyfile('config.py')
```

## 10. Configuration Loading Priority

Flask applies configuration settings in the order they are loaded. If the same configuration key is defined multiple times, the most recently loaded value overrides the previous one.

**Example:**
```python
app.config['DEBUG'] = False

app.config.from_pyfile('config.py')

app.config.from_envvar('APP_CONFIG')
```
```
# Output: final DEBUG value comes from whichever source loaded last
```

Values loaded from `APP_CONFIG` will override any matching settings from `config.py`, and values from `config.py` will override those defined directly in the application. The load order, in this example, from lowest to highest priority is: **direct assignment → config.py → APP_CONFIG environment variable file**.

## 11. Enabling Debug Mode

During development, enabling debug mode helps catch errors quickly by allowing automatic reloading of the server and displaying detailed error messages.

**Syntax:**
```python
app.config['DEBUG'] = True
```

With `DEBUG = True`, Flask will automatically restart when it detects changes in the code — useful for development but should never be enabled in production.

## 12. File Upload Configurations

If an application allows users to upload files, a folder must be specified to store these files, along with a size limit.

**Syntax:**
```python
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
```

- `UPLOAD_FOLDER` specifies where uploaded files will be stored.
- `MAX_CONTENT_LENGTH` limits the file upload size (here, 16MB) — this prevents users from uploading excessively large files.

## 13. Environment-Specific Configurations (Overview)

Flask supports different configurations for development, testing, and production environments — for example, debugging enabled in development, but stricter security settings needed in production. Flask allows the app to be configured based on the environment, ensuring smooth transitions from development to deployment.

**Steps to Set Environment-Specific Configurations:**
- Using Configuration Objects (e.g., `config.py`)
- Loading from Environment Variables
- Using `Flask.config.from_object()` or `Flask.config.from_envvar()`

## 14. Method 1 — Using Configuration Objects (Classes)

A common approach is to create a separate `config.py` file and define different configurations as Python classes.

**config.py:**
```python
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.db'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/production_db'
```

- `Config` is a base class that holds default settings.
- `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig` inherit from `Config` and override specific settings based on the environment.
- **Important:** In production environments, sensitive values such as secret keys should be loaded from environment variables instead of being hardcoded.

**Applying a specific configuration in the Flask app:**
```python
from flask import Flask
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
```
```
# Output: app now runs with DevelopmentConfig settings (DEBUG=True, SQLite dev DB)
```

This applies the `DevelopmentConfig` environment to the app — using `app.config.from_object()`, different environment settings can be applied whenever required, simply by swapping which class is passed in.

## 15. Method 2 — Loading Configurations from Environment Variables

Another way to configure a Flask application is by using environment variables. This method helps keep sensitive information, such as secret keys and database credentials, secure while allowing different settings to be used across development, testing, and production environments.

**Syntax:**
```python
import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
```

**Setting the environment variables in the terminal:**
```bash
export SECRET_KEY='my_production_secret'
export DATABASE_URL='postgresql://user:password@localhost/prod_db'
```

## 16. Method 3 — Loading Configurations Dynamically

Flask provides built-in methods such as `from_object()` and `from_envvar()` for loading configuration settings dynamically. These methods simplify configuration management across different environments.

### `from_object()`

Loads configuration settings from a Python object or module, useful when managing multiple environment configurations.

**Syntax:**
```python
app.config.from_object('config.ProductionConfig')  # Loads settings from ProductionConfig
```

Here, `config.ProductionConfig` refers to the `ProductionConfig` class inside the `config.py` file. This can be changed dynamically by passing a different class, such as `DevelopmentConfig` or `TestingConfig`, based on the environment.

**Dynamically choosing which config to load based on an environment variable:**
```python
import os

env = os.getenv('FLASK_ENV', 'development')

if env == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif env == 'production':
    app.config.from_object('config.ProductionConfig')
```

### `from_envvar()`

Instead of hardcoding configuration file names, the file path can be stored in an environment variable and loaded using `from_envvar()`.

**Syntax:**
```python
import os
app.config.from_envvar('FLASK_CONFIG_FILE')
```

**Example configuration file — settings.py:**
```python
DEBUG = False
TESTING = False
SECRET_KEY = 'my-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
```

The `from_envvar()` method reads the file path stored in the environment variable and loads all configuration settings defined in that file.

**Setting the environment variable before running the app:**
```bash
export FLASK_CONFIG_FILE='/path/to/settings.py'
```

## Notes / Edge Cases

- Configuration keys are case-sensitive and conventionally written in `ALL_CAPS` (e.g. `SECRET_KEY`, `DEBUG`) — this is Flask's own convention, not just a stylistic choice.
- `app.config` behaves like a Python dictionary — supports `.get()`, direct key access, `.update()`, and other dict methods.
- Never hardcode a `SECRET_KEY` or database credentials directly in source code that gets pushed to GitHub — use environment variables, especially in production.
- `DEBUG = True` should never be enabled in a production environment — it can expose sensitive internal information (stack traces, source code snippets) to anyone who triggers an error.
- Configuration loading priority matters: whichever method is called last wins if the same key is set by multiple methods (direct assignment, `from_pyfile()`, `from_object()`, `from_envvar()`).
- `from_object()` accepts either a string path (`'config.ProductionConfig'`) or the actual imported class/object itself — both forms work.
- Environment variables set via `export` (Linux/Mac) or `set`/`$env:` (Windows) only persist for that terminal session unless added to a permanent shell profile or `.env` file loaded by the app.
- Using class-based inheritance (`DevelopmentConfig(Config)`, `ProductionConfig(Config)`) avoids repeating shared settings — only the values that differ per environment need to be overridden in each subclass.

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Direct config assignment | `app.config['KEY'] = value` | Simplest way to set a config value |
| Load from a file | `app.config.from_pyfile('config.py')` | Keeps config separate from app logic |
| Custom config variable | `app.config['MY_KEY'] = value` | Not a built-in key — application-specific |
| Access a config value | `app.config['KEY']` or `app.config.get('KEY')` | `.get()` is safer, avoids `KeyError` |
| Secret key | `app.config['SECRET_KEY'] = 'x'` | Required for sessions, CSRF, secure cookies |
| Database URI | `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'` | Defines DB type + location for SQLAlchemy |
| Disable modification tracking | `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` | Improves performance |
| Session storage type | `app.config['SESSION_TYPE'] = 'filesystem'` | Stores session data server-side, not in cookies |
| Session lifetime | `app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)` | How long a session stays active |
| JSON key order | `app.config['JSON_SORT_KEYS'] = False` | Preserves insertion order in JSON responses |
| Pretty-print JSON | `app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True` | Human-readable JSON output |
| Enable debug mode | `app.config['DEBUG'] = True` | Dev only — never in production |
| Upload folder | `app.config['UPLOAD_FOLDER'] = 'uploads/'` | Where uploaded files are stored |
| Max upload size | `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024` | Limits file size (bytes) — here, 16MB |
| Config class (base) | `class Config: DEBUG = False` | Holds shared/default settings |
| Config class (environment-specific) | `class DevelopmentConfig(Config): DEBUG = True` | Inherits base, overrides what differs |
| Apply a config class | `app.config.from_object(DevelopmentConfig)` | Loads settings from a class/object |
| Apply by string path | `app.config.from_object('config.ProductionConfig')` | Same as above, using a string reference |
| Read an environment variable | `os.environ.get('KEY', 'default')` | Fallback value if variable isn't set |
| Load config from env-defined file path | `app.config.from_envvar('FLASK_CONFIG_FILE')` | File path itself comes from an env variable |
| Set an environment variable (terminal) | `export KEY='value'` | Persists only for that terminal session |