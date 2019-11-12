"""This is my database models"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    user_id = DB.Column(DB.Integer, primary_key=True)
    screen_name = DB.Column(DB.String(16), nullable=False)
    display_name = DB.Column(DB.String(16), nullable=False)

class Tweet(DB.Model):
    tweet_id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280), nullable=False)
    author_id = DB.Column(DB.Integer, nullable=False)