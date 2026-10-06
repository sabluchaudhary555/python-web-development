from flask import Flask

app = Flask(__name__)
# hello flask
@app.route('/')
def home():
    return "hello Flask"

# STATIC ROUTE
@app.route('/about')
def about():
    return 'welcome to about page'

# DYNAMIC ROUTE
@app.route('/user/<name>')
def user(name):
    return f' Hello {name}'

# MULTIPLE DYNAMIC ROUTING WITH URL CONVERTER
@app.route('/user/<name>/<int:id>')
def post(name, id):
    return f'name is {name}, id is {id}'

if __name__ == '__main__':
    app.run(debug=True)

