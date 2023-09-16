from flask import render_template, request, redirect, url_for, flash, current_app
from models.Utilisateur import Utilisateur
from setup_sql import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from threading import Thread
from flask_mail import Message
from flask import Blueprint
from . import app
import os
from flask_mail import Mail

auth = Blueprint('auth', __name__)

@app.route('/')
def login():
    user = Utilisateur.query.filter_by(id=1).first()
    return render_template('compte/login.html')

@app.route('/login_user', methods=['GET', 'POST'])
def login_utilisateur():
    user = Utilisateur.query.filter_by(mail=request.form['mail']).first()
    if user and check_password_hash(user.mdp, request.form['mdp']):
        login_user(user)
        flash('Connecté avec succès!', 'success')
        return redirect(url_for('controllers.accueil'))
    else:
        flash('Échec de la connexion. Veuillez vérifier vos identifiants.', 'danger')
    return redirect(url_for('controllers.login'))

@app.route('/signup')
def signup():
    return render_template('compte/signup.html')

@app.route('/signup_user', methods=['GET', 'POST'])
def signup_utilisateur():
    if request.method == 'POST':
        mail = request.form['mail']
        mdp = request.form['mdp']
        confirmation_mdp = request.form['confirmation']
        
        if is_invalid_mail(mail):
            flash('Adresse mail invalide', 'danger')
            return redirect(url_for('controllers.signup'))
        
        if is_invalid_password(mdp):
            flash('Mot de passe invalide', 'danger')
            return redirect(url_for('controllers.signup'))
        
        if mdp != confirmation_mdp:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return redirect(url_for('controllers.signup'))

        new_user = Utilisateur(mail=mail, mdp=mdp)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        flash('Inscription réussie ! Renseignez vos informations personnelles.', 'success')
        return redirect(url_for('controllers.reglages'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('controllers.login'))

def is_invalid_mail(mail):
    if Utilisateur.query.filter_by(mail=mail).first() or mail == '' or mail is None or '@' not in mail or '.' not in mail:
        return True
    return False

def is_invalid_password(mdp):
    if mdp == '' or mdp is None or len(mdp) < 8:
        return True
    return False

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        mail = request.form['mail']
        user = Utilisateur.query.filter_by(mail=mail).first()
        if user:
            token = user.get_reset_token()
            db.session.commit()

            msg = Message()
            msg.subject = 'Réinitialisation du mot de passe'
            msg.sender = 'terry57tt@gmail.com'
            msg.recipients = ['terry57tt@gmail.com']
            msg.html = render_template('mail/reset_password.html', user=user, token=token)
            email = Mail(current_app)
            email.send(msg)

            flash('Un mail vous a été envoyé pour réinitialiser votre mot de passe.', 'success')
            return redirect(url_for('controllers.login'))
        else:
            flash('Adresse mail inconnue.', 'danger')
    return redirect(url_for('controllers.login'))

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = Utilisateur.filter_by_token(token)
    if user and user.is_reset_token_valid():
        return render_template('compte/new_password.html', token=token)
    else:
        flash('Lien de réinitialisation invalide ou expiré.', 'danger')
        return redirect(url_for('controllers.login'))
    
@app.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    user = Utilisateur.filter_by_token(token)
    if user and user.is_reset_token_valid():
        if request.method == 'POST':
            mdp = request.form['mdp']
            confirmation_mdp = request.form['confirmation']
            
            if is_invalid_password(mdp):
                flash('Mot de passe invalide', 'danger')
                return redirect(url_for('controllers.reset_password', token=token))
            
            if mdp != confirmation_mdp:
                flash('Les mots de passe ne correspondent pas', 'danger')
                return redirect(url_for('controllers.reset_password', token=token))

            user.reset_password(mdp)
            db.session.commit()

            flash('Mot de passe réinitialisé avec succès !', 'success')
            return redirect(url_for('controllers.login'))
        return redirect(url_for('controllers.new_password', token=token))
    else:
        flash('Lien de réinitialisation invalide ou expiré.', 'danger')
        return redirect(url_for('controllers.login'))