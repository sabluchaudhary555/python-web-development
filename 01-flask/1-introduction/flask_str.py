from flask import Flask  # Import the Flask class

app = Flask(__name__)  # Initialize the Flask application

@app.route("/")  # Define the root URL route
def hello():
    return "Hello, World!"  # Return text to the browser

if __name__ == "__main__":
    app.run(debug=True)  # Start the development server with auto-reload