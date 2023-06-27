import os
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2
from dotenv import load_dotenv

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