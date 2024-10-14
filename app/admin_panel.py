from flask_admin.contrib.sqla import ModelView
from .models import User
from flask_admin import Admin
from . import db

admin = Admin()

admin.add_view(ModelView(User,db.session))