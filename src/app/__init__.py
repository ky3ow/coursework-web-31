import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config=None):
    from app.routes import main

    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(main)

    DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=DATABASE,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{DATABASE}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        migrate = Migrate(app, db)
        db.create_all()

    return app
