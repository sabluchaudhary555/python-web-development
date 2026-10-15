from flask import Flask, render_template

app = Flask(__name__)


# 1. Context Processor (Variables available globally in ALL templates)
@app.context_processor
def inject_site_name():
    return dict(site_name="Jinja2 Master Class")


# 2. Custom Filter (Used to reverse a string)
@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]


# Route to demonstrate advanced Jinja features
@app.route("/")
def jinja_concepts():
    # Complex data structures to pass to the template
    user_info = {"name": "Hacker", "role": "admin", "active": True}
    tech_stack = ["Flask", "Python", "Jinja2", "Docker"]

    return render_template(
        "jinja_page.html",
        user_info=user_info,
        tech_stack=tech_stack,
        is_logged_in=True
    )


if __name__ == "__main__":
    # Running on port 5003 to avoid conflicts
    app.run(debug=True, port=5003)