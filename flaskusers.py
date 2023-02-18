# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)
#####
# need: pip install email_validator, Flask-User and others from cyborgchaman


from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin
from flask_babelex import Babel
#from flask.ext.babelex import Babel

# import os
# import openai
from flask import redirect, render_template, request, url_for
# import pickle
# from datetime import datetime, date
# from dotenv import load_dotenv, find_dotenv

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickstart_app.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Flask-User QuickStart App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form


def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    babel = Babel(app)
    babel.BABEL_DEFAULT_LOCALE='es'
    
    #app.config.from_pyfile('mysettings.cfg')
    # Initialize Flask-SQLAlchemy
    db = SQLAlchemy(app)

    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
        
        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        email_confirmed_at = db.Column(db.DateTime())
        
        # User information
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        #sesiones = db.relationship('Sesion', secondary=user_sessions, lazy='subquery',
        #    backref=db.backref('usuarios', lazy=True))
        
    def __repr__(self):
        return '<User %r>' % self.username


    # Create all database tables
    db.create_all()

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # The Home page is accessible to anyone
    # @app.route('/')
    # def home():
    #     return render_template('home.html')

    @app.route('/oldhome')
    def home_page():
        # String-based templates
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Home page</h3>
                <a href={{ url_for('user.register') }}>Register</a>
                <a href={{ url_for('user.login') }}>Sign in</a><br>
                <a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)
                <a href={{ url_for('member_page') }}>Member page</a> (login required)
                <a href={{ url_for('user.logout') }}>Sign out</a>
            {% endblock %}
            """)
    ### end create_app
    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=4000, debug=True)
