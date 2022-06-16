"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://i.stack.imgur.com/l60Hf.png"

def connect_db(app):
    '''connect to database'''
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User'''
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                           nullable=False)
    last_name = db.Column(db.String(20),
                          nullable=False)
    image_url = db.Column(db.String,
                        nullable=False,
                        default=DEFAULT_IMAGE_URL)

    def __repr__(self):
        rep = f'<User: {self.first_name} {self.last_name}, id={self.id} >'
        return rep


class Post(db.Model):
    '''post'''
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(20),
                           nullable=False)
    content = db.Column(db.String,
                          nullable=False)
    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.now())
    user_id=db.Column(db.Integer.
                        db.ForeignKey('Users.id'))

    user = db.relationship('User')

    def __repr__(self):
        rep = f'<User: {self.first_name} {self.last_name}, id={self.id} >'
        return rep
