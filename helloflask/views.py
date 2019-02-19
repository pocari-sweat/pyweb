from flask import render_template, request, Response
from datetime import datetime, date
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from helloflask import app
from helloflask.classes import FormInput
from helloflask.init_db import db_session
from helloflask.models import User, Song, Album, Artist, SongArtist

@app.route('/')
def idx():
    return render_template("app.html")

@app.route('/songinfo/<songno>')
def songinfo():
    return render_template("app.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return render_template("app.html")
