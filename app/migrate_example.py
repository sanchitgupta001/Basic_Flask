from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class Users():
    id = db.Column(db.Integer(10),primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    settings = db.Column(db.String(32500))
    tracking = db.Column(db.String(32500))
    rank = db.Column(db.Integer(3))


if __name__ == '__main__':
    manager.run()
