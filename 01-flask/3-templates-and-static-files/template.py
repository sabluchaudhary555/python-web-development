from flask import Flask, render_template

app = Flask(__name__)

# Basic route to demonstrate rendering a simple template and passing a variable
@app.route("/")
def basic_template():
    # render_template looks inside the 'templates' folder automatically
    return render_template("template_page.html", message="Welcome to Template Basics!")

if __name__ == "__main__":
    # Running on port 5001 to avoid conflicts with other files
    app.run(debug=True, port=5001)