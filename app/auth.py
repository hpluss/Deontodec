from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional



## Formulaires de connexion

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    username = StringField('Pseudo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("S'inscrire")

class ProfileForm(FlaskForm):
    username = StringField('Pseudo', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Mot de passe actuel')
    new_password = PasswordField('Nouveau mot de passe', validators=[Optional(),Length(min=6)])
    confirm_password = PasswordField('Confirmer le nouveau mot de passe', 
                                     validators=[EqualTo('new_password')])
    submit = SubmitField('Mettre à jour le profil')

### Routes de connexion classique

def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Ce pseudo est déjà utilisé.', 'danger')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Cet email est déjà utilisé.', 'danger')
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
            login_user(user)
            return redirect(url_for('index'))
    
    return render_template('auth/login.html',form=form, action="register")

def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou mot de passe invalide.', 'danger')

    return render_template('auth/login.html', form=form, action="login")


@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))


############## Route associée à la page de profile

@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.new_password.data:
                current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Votre profil a été mis à jour avec succès.', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Mot de passe incorrect.', 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/profile.html', title='Profil', form=form)