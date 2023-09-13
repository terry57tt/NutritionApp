from flask import render_template, request, redirect, url_for, flash, Response
from models.Utilisateur import Utilisateur
from setup_sql import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from controllers import app
from flask import Blueprint
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