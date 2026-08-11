from flask import Flask

app = Flask(__name__)

@app.route('/hello')                            # Hello route
def hello():
    return "Welcom to Hello World"

@app.route('/user/<username>')                  # Variable in route
def user(username):
    return f'Welcome to {username}'

@app.route('/post/<int:post_id>')               # Variable converter into diff data type in route
def post(post_id):
    return f' Your Podt Id is {post_id}'

@app.route('/')             # Home Page route
def index():
    return "Home Page"


def user(username):             # Add url rule
    return f'Welcom to {username} in add url';
app.add_url_rule('/user/<username>', view_func=user)


if __name__ == '__main__':
    app.run(debug=True)