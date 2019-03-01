from flask import Flask
from flask_migrate import Migrate
from jobplus.config import configs
from jobplus.models import db,User
from flask_login import LoginManager

def register_extensions(app):
    db.init_app(app)
    Migrate(app,db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view='front.login'

def register_blueprints(app):
    from .handlers import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)



def create_app(config):
    app = Flask(__name__)

    if isinstance(config,dict):
        app.config.update(config)
    else:
        app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    return app


