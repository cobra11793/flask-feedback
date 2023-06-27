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

@app.route('/register' methods=["GET", "POST"])
def register_user():
    form = AddUserForm()
    """Register user using WTF forms"""
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, 
                    password=password, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name)
        db.session.add(user)
        db.session.commmit()
        return redirect('/secret')
    else:
        return render_template('users/register.html')