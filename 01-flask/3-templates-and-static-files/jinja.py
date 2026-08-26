from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome! Visit /yourname to see the dynamic greeting."

@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)

@app.route("/about2")
def about():
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("about2.html", sites=sites)

if __name__ == "__main__":
    app.run(debug=True)