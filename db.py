from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import SQLALCHEMY_DATABASE_URI
from app import app

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    settings = db.Column(db.String(32500))
    tracking = db.Column(db.String(32500))
    rank = db.Column(db.Integer)


if __name__ == '__main__':
    manager.run()
