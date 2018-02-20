#encoding: utf-8

from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    #'now()' gets the first time of server when we login; 也就是一直显示的是第一次登陆的时间；
    #'now' gets the current time when the server gets started everytime;显示的是每次登陆的时间，变动的。
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('questions'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    question = db.relationship('Question', backref=db.backref('comments'))
    author = db.relationship('User', backref=db.backref('comments'))


