from .extensions import db

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    species = db.Column(db.String(100))
    habitat = db.Column(db.String(100))
    legs = db.Column(db.Integer)
    image = db.Column(db.String(200)) 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))