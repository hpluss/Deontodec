from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        Définit le mot de passe de l'utilisateur en le hachant.
        
        :param password: Le mot de passe en clair.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Vérifie si le mot de passe fourni correspond au hash stocké.
        
        :param password: Le mot de passe à vérifier.
        :return: True si le mot de passe est correct, False sinon.
        """
        return check_password_hash(self.password_hash, password)