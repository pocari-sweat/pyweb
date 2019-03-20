from flask import render_template, request, Response, session, jsonify, make_response, redirect, flash, url_for
from datetime import datetime, date
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from helloflask import app
from helloflask.classes import FormInput
from helloflask.init_db import db_session
from helloflask.models import User, Song, Album, Artist, SongArtist, SongRank, SongInfo, Myalbum, Mycom

from helloflask.models import Ttt

def songlist(dt):
    sr = SongRank.query.filter_by(rankdt=dt).options(joinedload(SongRank.song))
    sr = sr.options(joinedload(SongRank.song, Song.album))
    sr = sr.options(joinedload(SongRank.song, Song.songartists))
    sr = sr.filter("atype=0")
    return sr


@app.route('/mycoms/<myalbumid>', methods=['GET'])
def mycoms(myalbumid):
    cmts = Mycom.query.filter('myalbumid=:myalbumid').params(
        myalbumid=myalbumid).order_by(Mycom.id.desc()).all()
    return jsonify([s.json() for s in cmts])

@app.route('/myalbum', methods=['GET'])
def myalbum():
    if not session.get('loginUser'):
        session['next'] = request.url
        return redirect('/login')
        # return redirect( url_for('login', next=request.url) )

    loginUser = session.get('loginUser')
    songs = Myalbum.query.filter('userid=:userid').params(userid=loginUser.get('userid')).all()

    if request.is_xhr:
        return jsonify([s.json() for s in songs])
        
    return render_template("myalbum.html", songs=songs)


@app.route('/myalbum', methods=['POST'])
def myalbum_post():
    songno = request.form.get('songno')
    myalbum = Myalbum(session.get('loginUser').get('userid'), songno)
    try:
        db_session.add(myalbum)
        db_session.commit();
        
    except SQLAlchemyError as err:
        db_session.rollback()
        print("Error!!", err)

    return jsonify({"result": 'OK'})

@app.route('/')
def idx():
    lives = songlist('2019-01-29')
    todays = songlist('2019-01-28')
    return render_template("app.html", lives=lives, todays=todays)

@app.route('/regist', methods=['GET'])
def regist():
    return render_template("regist.html")

@app.route('/regist', methods=['POST'])
def regist_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    nickname = request.form.get('nickname')

    if passwd != passwd2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("regist.html", email=email, nickname=nickname)
    else:
        u = User(email, passwd, nickname, True)
        try:
            db_session.add(u)
            db_session.commit()

        except:
            db_session.rollback();

        flash("%s 님, 가입을 환영합니다!" % nickname)
        return redirect("/login")

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    u = User.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
    if u is not None:
        session['loginUser'] = { 'userid': u.id, 'name': u.nickname }
        if session.get('next'):
            next = session.get('next')
            del session['next']
            return redirect(next)
        return redirect('/')
    else:
        flash("해당 사용자가 없습니다!!")
        return render_template("login.html", email=email)

@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']

    return redirect('/')


@app.route('/songinfo/<songno>')
def songinfo(songno):
    song = Song.query.filter_by(songno = songno).first()
    songinfos = SongInfo.query.filter_by(songno = songno)
    print("===>", songinfos.count())
    return render_template("songinfo.html", song=song, songinfos=songinfos)


@app.route('/ttt2/<myal>', methods=['GET'])
def ttt2(myal):

    ttts = Ttt.query.filter('myalbum=:myalid').params(
        myalid=myal).order_by(Ttt.id).all()

    return jsonify([s.json() for s in ttts])

@app.route('/ttt', methods=['GET'])
def myalbums():
    if not session.get('loginUser'):
        session['next'] = request.url
        return redirect('/login')
        # return redirect( url_for('login', next=request.url) )

    loginUser = session.get('loginUser')
    songs = Myalbum.query.filter('userid=:userid').params(
        userid=loginUser.get('userid')).all()

    if request.is_xhr:
        return jsonify([s.json() for s in songs])

    return render_template("ttt2.html", songs=songs)
