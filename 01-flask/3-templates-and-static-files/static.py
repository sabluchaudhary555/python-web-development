from flask import Flask, render_template

app = Flask(__name__)

# Route to demonstrate loading CSS, JS, Images, Audios, and Videos
@app.route("/")
def load_statics():
    return render_template("static_page.html")

if __name__ == "__main__":
    # Running on port 5002 to avoid conflicts
    app.run(debug=True, port=5002)