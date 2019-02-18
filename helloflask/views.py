from flask import render_template, request, Response
from datetime import datetime, date
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from collections import namedtuple
from helloflask import app
from helloflask.classes import FormInput
from helloflask.init_db import db_session
from helloflask.models import User, Song, Album, Artist, SongArtist


@app.route('/sql3')
def sql3():
    # albums = Album.query.order_by(Album.albumid.desc()).limit(5)
    # albums = Album.query.filter(Album.albumid == '10218750').all()
    albums = Album.query.options(joinedload(Album.songs)).filter_by(albumid = '10218750').all()

    return render_template('main.html', albums=albums)

# pre-load (sametime)
@app.route('/sql2')
def sql2():
    # ret = db_session.query(Song).options(subqueryload(Song.album))\
    #       .filter(Song.likecnt < 10000)

    ret = Song.query.options(joinedload(Song.album))\
              .filter(Song.likecnt < 10000)

    return render_template('main.html', ret=ret)

# select by each record
@app.route('/sql')
def sql():
    ret = Song.query.options(joinedload(Song.album)).filter(Song.likecnt < 10000).options(joinedload(Song.songartists, SongArtist.artist))
    #.options(subqueryload(Song.songartists.artist))
    return render_template('main.html', ret=ret)


@app.route('/')
def idx():
    ret = 'OK'
    try:
        # u = User('abc@efg.com', 'hong')
        # db_session.add(u)
        # u = User.query.filter(User.id == 10).first()
        # print("user.id=", u.id)
        # db_session.delete(u)
        # u.email = 'indiflex1@gmail.com'
        # db_session.add(u)

        s = db_session()
        result = s.execute('select id, email, nickname from User where id > :id', {'id': 10})
        Record = namedtuple('User', result.keys())
        rrr = result.fetchall()
        print(">>", type(result), result.keys(), rrr)
        records = [Record(*r) for r in rrr]
        for r in records:
            print(r, r.nickname, type(r))

        s.close()

        ret = records

        db_session.commit()

        # ret = User.query.all()
        # ret = User.query.filter(User.id > 5)
        
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        print("SqlError>>", sqlerr)

    # except:
    #     print("Error!!")

    # finally:
    #     db_session.close()

    # return "RET=" + str(ret)
    return render_template('main.html', userlist=ret)
