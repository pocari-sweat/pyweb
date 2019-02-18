from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from helloflask.init_db import Base


class Album(Base):
    __tablename__ = 'Album'
    albumid = Column(String, primary_key=True)
    createdt = Column(String)
    title = Column(String)
    company = Column(String)
    genre = Column(String)
    likecnt = Column(Integer)
    rate = Column(Float)
    crawldt = Column(String)

class Song(Base):
    __tablename__ = 'Song'
    songno = Column(String, primary_key=True)
    title = Column(String)
    genre = Column(String)
    likecnt = Column(Integer)
    albumid = Column(String, ForeignKey('Album.albumid'), nullable=False)
    album = relationship('Album', backref=backref('Album'))


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    passwd = Column(String)
    nickname = Column(String)

    def __init__(self, email=None, nickname='손님'):
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return 'User %s, %r, %r' % (self.id, self.email, self.nickname)
