from flask import Flask                   # Import the Flask class
app = Flask(__name__)                     # Create the Flask app instance
@app.route('/')                           # Map URL '/' to the function below
def hello_world():                        # Define the view function for '/'
    return 'Hello World'                  # Send this text as the response
if __name__ == '__main__':                # Run only if this file is executed directly
   # app.run()                            # Start the Flask development server (This line is by default)

    app.run(debug=True)
        # Starts the Flask development server with debug mode enabled.
        # debug=True, auto-reloads the server on code changes and shows detailed error pages in the browser.