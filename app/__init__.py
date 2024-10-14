from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager





db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    

    with app.app_context(): 
        from . import routes
        from . import auth
        from . import admin_panel

        admin_panel.admin.init_app(app)
        db.create_all()

    return app