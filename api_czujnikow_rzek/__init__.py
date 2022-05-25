from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from api_czujnikow_rzek.errors import errors_bp
    from api_czujnikow_rzek.czujniki import czujniki_bp
    from api_czujnikow_rzek.dane import dane_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(czujniki_bp, url_prefix='/api/v1')
    app.register_blueprint(dane_bp, url_prefix='/api/v1')
    return app
