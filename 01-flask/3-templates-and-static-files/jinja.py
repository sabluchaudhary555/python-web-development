from flask import Flask, render_template, session

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome! Visit /yourname to see the dynamic greeting."

@app.route("/<name>")
def welcome(name):
    return render_template("jinja.html", name=name)

@app.route("/loop")
def loop():
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("jinja_loop.html", sites=sites)

@app.route("/ifelse")
def ifelse():
    is_logged_in = False
    return render_template("jinja_ifelse.html", is_logged_in=is_logged_in)


if __name__ == "__main__":
    app.run(debug=True)