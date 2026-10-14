from flask import Flask, render_template

app = Flask(__name__)


# 1. Context Processor (Variables available globally in ALL templates)
@app.context_processor
def inject_site_name():
    return dict(site_name="Jinja2 Master Class")


# 2. Custom Filter (Can be used anywhere as |reverse_string)
@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]


@app.route("/")
def home():
    # Data to pass to the template
    user_info = {"name": "Hacker", "role": "admin", "active": True}
    tech_stack = ["Flask", "Python", "Jinja2", "Docker"]

    return render_template(
        "index.html",
        user_info=user_info,
        tech_stack=tech_stack,
        is_logged_in=True,
        price=49.995
    )


if __name__ == "__main__":
    app.run(debug=True)