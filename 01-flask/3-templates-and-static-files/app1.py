from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/about1')
def about():
    return render_template('about1.html')

@app.route('/contact1')
def contact():
    return render_template('contact1.html')

if __name__ == '__main__':
    app.run(debug=True)
