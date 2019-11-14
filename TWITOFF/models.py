"""This is my database models"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    user_id = DB.Column(DB.BigInteger, primary_key=True)
    screen_name = DB.Column(DB.String(16), nullable=False)
    display_name = DB.Column(DB.String(16), nullable=False)
    pfp_url = DB.Column(DB.String(100), nullable=False)
    color = DB.Column(DB.String(6), nullable=False)

class Tweet(DB.Model):
    tweet_id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300), nullable=False)
    author_id = DB.Column(DB.BigInteger, nullable=False)
    embedding = DB.Column(DB.PickleType, nullable=False)