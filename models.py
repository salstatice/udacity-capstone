import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


'''
Actor
Have name, age and gender
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  roles = db.relationship('Role', backref='actor', lazy=True)

  def __init__(self, name, age, gender=""):
    self.name = name
    self.age = age
    self.gender = gender

  '''
  format()
    json repsentation of the Actor model
  '''
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
    }

  '''
  insert()
    inserts a new model into a database
    the model must have a unique id or null id
    EXAMPLE
      actor = Actor(name=req_name, age=req_age, gender=req_gender)
      actor.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  

'''
Movie
Have title and release date
'''
class Movie(db.Model):
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  date = Column(db.DateTime, nullable=False)
  roles = db.relationship('Role', backref='movie', lazy=True)

  def __init__(self, title, date):
    self.title = title
    self.date = date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_year': self.data.strftime("%Y"),
    }

'''
Role
Have role name, actor name and related movie
'''
class Role(db.Model):
  __tablename__ = 'Role'

  id = Column(Integer, primary_key=True)
  role_name = Column(String)
  actor_id = Column(Integer, db.ForeignKey('Actor.id'))
  movie_id = Column(Integer, db.ForeignKey('Movie.id'))

  def __init__(self, role_name, actor_id, movie_id):
    self.role_name = role_name
    self.actor_id = actor_id
    self.movie_id = movie_id

  def format(self):
    return {
      'id': self.id,
      'role_name': self.role_name,
      'actor_id': self.actor_id,
      'actor_name': self.actor.name,
      'movie_id': self.movie_id,
      'movie_name': self.movie.title,
    }
  
