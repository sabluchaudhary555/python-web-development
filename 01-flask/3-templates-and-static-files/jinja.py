from flask import Flask, render_template

app = Flask(__name__)


# Context Processor (Injects variables globally into ALL templates)
@app.context_processor
def inject_site_name():
    return dict(site_name="Jinja2 Complete Masterclass")


# Custom Filter (Reverses a string)
@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]


@app.route("/")
def jinja_concepts():
    # Complex data to test Jinja2 features
    user_info = {"name": "Hacker", "role": "Cybersecurity Lead"}
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    html_snippet = "<b>This is Bold Content</b>"

    return render_template(
        "jinja_page.html",
        user_info=user_info,
        sites=sites,
        is_logged_in=True,
        price=99.995,
        html_snippet=html_snippet,
        number=8
    )


if __name__ == "__main__":
    app.run(debug=True, port=5003)