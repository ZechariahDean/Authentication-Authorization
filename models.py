"""Models for Authentication_Authorization"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  """Model for Users"""

  __tablename__ = "users"

  username = db.Column(db.String(20), primary_key = True, nullable = False)
  password = db.Column(db.Text, nullable = False)
  email = db.Column(db.String(50), nullable = False)
  first_name = db.Column(db.String(30), nullable = False)
  last_name = db.Column(db.String(30), nullable = False)

  feedbacks = db.relationship("Feedback", backref="users", cascade="all, delete-orphan")

class Feedback(db.Model):
  """model for feedback"""

  __tablename__ = "feedbacks"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  title = db.Column(db.String(100), nullable = False)
  content = db.Column(db.Text, nullable = False)
  username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable = False)



def connect_db(app):
  """Connect the database to application"""
  db.app = app
  db.init_app(app)