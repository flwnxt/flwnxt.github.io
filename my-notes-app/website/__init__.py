from flask import Flask
from os import path
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager
# from website.database import *
# from website import models


# Define the DB connection
db = SQLAlchemy()
DB_NAME = "database.db"


# Create DB tables
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


# Create App & db connection
def create_app():
    app = Flask(__name__)
    # store the secret key
    app.config['SECRET_KEY'] = 'random string'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # solve an error in which this function couldn't have been parsed
    with app.app_context():
        db.create_all()

    # import the blueprints
    from .views import views
    from .auth import auth

    # register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # deprecated import:
    # import this file to ensure that the .models file is initialized before it launches
    # from website.models import User, Note

    create_database(app)

    # telling flask how we find and log in an user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # using for logging out an user
    @login_manager.user_loader
    def load_user(usr_id):
        return User.query.get(int(usr_id))

    return app


def create_database(app):
    print('Before If not')
    if not path.exists('website/' + DB_NAME):
        app.app_context().push()
        db.create_all()
        print('Created Database!')
