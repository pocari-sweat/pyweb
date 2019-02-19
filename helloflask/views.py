from flask import render_template, request, Response, session, jsonify, make_response, redirect
from datetime import datetime, date
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from helloflask import app
from helloflask.classes import FormInput
from helloflask.init_db import db_session
from helloflask.models import User, Song, Album, Artist, SongArtist, SongRank

def songlist(dt):
    sr = SongRank.query.filter_by(rankdt=dt).options(joinedload(SongRank.song))
    sr = sr.options(joinedload(SongRank.song, Song.album))
    sr = sr.options(joinedload(SongRank.song, Song.songartists))
    sr = sr.filter("atype=0")
    return sr

@app.route('/')
def idx():
    lives = songlist('2019-01-29')
    todays = songlist('2019-01-28')

    return render_template("app.html", lives=lives, todays=todays)

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    u = User.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
    print("uuuuuuuuuuuuuu>>", u)
    if u is not None:
        session['loginUserId'] = u.id
        session['loginUserName'] = u.nickname
        return redirect('/')
    else:
        return render_template("login.html", email=email)

@app.route('/logout')
def logout():
    if session.get('loginUserId'):
        del session['loginUserId']
        del session['loginUserName']

    return redirect('/')








# @app.route('/songinfo/<songno>')
# def songinfo(songno):
    # return render_template("app.html")
    # s = SongArtist.query.filter_by(songno=songno).order_by(SongArtist.atype).options(joinedload(SongArtist.artist)).all()
    # ll = [ss.json() for ss in s]
    # print("ssssssssssSS>>", s)
    # return make_response(jsonify(ll))
