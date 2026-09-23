import os
from flask import Flask, jsonify

app = Flask(__name__)

# -------------------------------------------------------------------------
# 1. Dynamic Configuration Loading via Environment Variable
# Set FLASK_ENV in terminal: 'development', 'production', or 'testing'
# -------------------------------------------------------------------------
env_name = os.getenv("FLASK_ENV", "development").lower()

config_map = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig",
}

# Dynamically loads class using string import path
selected_config = config_map.get(env_name, "config.DevelopmentConfig")
app.config.from_object(selected_config)

# -------------------------------------------------------------------------
# 2. Priority Override / Direct Assignment Demonstration
# Direct assignment runs AFTER from_object(), overriding the class value.
# -------------------------------------------------------------------------
app.config["CUSTOM_OVERRIDE_FLAG"] = "Applied directly inside app.py"
# app.config['ITEMS_PER_PAGE'] = 50  # Uncomment to override class default


# -------------------------------------------------------------------------
# 3. Informational Endpoints (Direct String & Auto-JSON Responses)
# -------------------------------------------------------------------------
@app.route("/")
def home():
    # Reading config values using .get() to prevent KeyErrors
    env_title = app.config.get("ENVIRONMENT_NAME", "Unknown Environment")
    company = app.config.get("COMPANY_NAME")
    is_debug = app.config.get("DEBUG")

    return f"""
    <h1>Flask Configuration System Running</h1>
    <p><b>Active Environment:</b> {env_title}</p>
    <p><b>Company:</b> {company}</p>
    <p><b>Debug Status:</b> {is_debug}</p>
    <p>Visit <a href="/config-summary">/config-summary</a> to inspect all active settings via JSON.</p>
    """


@app.route("/config-summary", methods=["GET"])
def config_summary():
    """
    Returns an auto-converted JSON dictionary reflecting current configuration.
    Demonstrates reading built-in and custom config keys directly from app.config.
    """
    return {
        "active_environment": app.config.get("ENVIRONMENT_NAME"),
        "debug_mode": app.config["DEBUG"],
        "testing_mode": app.config["TESTING"],
        "database_uri": app.config["SQLALCHEMY_DATABASE_URI"],
        "track_modifications": app.config["SQLALCHEMY_TRACK_MODIFICATIONS"],
        "company_name": app.config.get("COMPANY_NAME"),
        "items_per_page": app.config.get("ITEMS_PER_PAGE"),
        "max_content_length_bytes": app.config["MAX_CONTENT_LENGTH"],
        "secret_key_status": "Loaded and Protected" if app.config.get("SECRET_KEY") else "Missing",
        "override_test": app.config.get("CUSTOM_OVERRIDE_FLAG"),
    }


# -------------------------------------------------------------------------
# 4. Error Handling (413 Request Entity Too Large)
# -------------------------------------------------------------------------
@app.errorhandler(413)
def entity_too_large(error):
    max_mb = app.config["MAX_CONTENT_LENGTH"] / (1024 * 1024)
    return jsonify({
        "error": "Payload exceeds allowed limit",
        "allowed_max_mb": max_mb
    }), 413


if __name__ == "__main__":
    # App starts using settings loaded from the chosen environment class
    app.run(
        port=5000,
        debug=app.config["DEBUG"]
    )