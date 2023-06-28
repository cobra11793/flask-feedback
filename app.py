import os
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2
from dotenv import load_dotenv
from forms import LoginForm, AddUserForm

load_dotenv()
MY_PASSWORD = os.getenv("MY_PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLO123"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{MY_PASSWORD}@localhost/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = AddUserForm()
    """Register user using WTF forms"""
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        User.register(username, password, email, first_name, last_name)
        db.session.commit()
        return redirect(f"/users/{username}")
    else:
        return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login form for user"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route('/users/<username>')
def display_user(username):
    if "username" in session:
        user = User.query.get_or_404(username)
        return render_template('users/details.html', user=user)
    else:
        flash(f'Must be logged in as {username} to view!')
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')