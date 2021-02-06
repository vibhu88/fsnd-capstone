from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable = False )
    theatres = db.relationship('Theatre', backref='movie', cascade="all, delete-orphan", lazy=True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    theatres = db.relationship('Theatre', backref='artist', cascade="all, delete-orphan", lazy=True)

class Theatre(db.Model):
    __tablename__ = 'Chart'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable = False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False )