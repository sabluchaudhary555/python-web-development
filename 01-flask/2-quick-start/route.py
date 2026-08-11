from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Welcom to Hello World"

@app.route('/user/<username>')
def user(username):
    return f'Welcome to {username}'

@app.route('/post/<int:post_id>')
def post(post_id):
    return f' Your Podt Id is {post_id}'

@app.route('/')
def index():
    return "Home Page"

if __name__ == '__main__':
    app.run(debug=True)