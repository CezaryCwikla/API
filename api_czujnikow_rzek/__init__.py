from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='prod'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from api_czujnikow_rzek.errors import errors_bp
    from api_czujnikow_rzek.czujniki import czujniki_bp
    from api_czujnikow_rzek.dane import dane_bp
    from api_czujnikow_rzek.powietrza import powietrza_bp
    from api_czujnikow_rzek.auth import auth_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(czujniki_bp, url_prefix='/api/v1')
    app.register_blueprint(dane_bp, url_prefix='/api/v1')
    app.register_blueprint(powietrza_bp, url_prefix='/api/v1/powietrza')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    return app
