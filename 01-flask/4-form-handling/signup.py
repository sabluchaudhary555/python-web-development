from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(),
        Length(min=5, max=25, message='Username must be in 5 to 25 characters')
    ])
    password = PasswordField('Password', validators=[InputRequired('Password required')])
    submit = SubmitField('Submit')

@app.route('/Signup', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        return f'Hi {form.username.data}!!'
    return render_template('Signup.html', form=form)

if __name__ == '__main__':
    # Port 5001 is use kiya hai taaki index wale form se conflict na ho
    app.run(debug=True, port=5001)