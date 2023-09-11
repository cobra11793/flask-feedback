from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators  import InputRequired

class AddUserForm(FlaskForm):

    username = StringField("username")
    password = PasswordField("password")
    email = EmailField("email")
    first_name = StringField("first_name")
    last_name = StringField("last_name")


class LoginForm(FlaskForm):

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("title", [InputRequired()])
    content = StringField("content", [InputRequired()])