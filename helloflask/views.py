from flask import render_template, request, Response
from datetime import datetime, date
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from helloflask import app
from helloflask.classes import FormInput
from helloflask.init_db import db_session
from helloflask.models import User, Song, Album, Artist, SongArtist, SongRank

@app.route('/')
def idx():
    livedt = '2019-01-29'
    today = '2019-01-25'

    lives = SongRank.query.filter_by(rankdt = livedt).options(joinedload(SongRank.song))
    lives = lives.options(joinedload(SongRank.song, Song.album))
    lives = lives.options(joinedload(SongRank.song, Song.songartists))
    lives = lives.filter("atype=0")
    return render_template("app.html", lives=lives)

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
