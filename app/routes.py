
from flask import render_template
from flask import current_app as app

from app.auth import register, login, logout, profile


@app.route('/')
def index():
    return render_template('index.html')

# Enregistrement des routes d'authentification
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/profile', 'profile', profile, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)