from flask import render_template, request, redirect, url_for, flash, Response
from models.Utilisateur import Utilisateur
from setup_sql import db

from controllers import app

@app.route('/login')
def login():
    return render_template('compte/login.html')

@app.route('/signup')
def signup():
    return render_template('compte/signup.html')

@app.route('/login_utilisateur', methods=['GET', 'POST'])
def login_utilisateur():
    mail = request.form['mail']
    mdp = request.form['mdp']
    utilisateur_courrant = Utilisateur.query.filter_by(mail=mail).first()
    if utilisateur_courrant is None:
        return redirect(url_for('controllers.login'))
    elif utilisateur_courrant.mdp != mdp:
        return redirect(url_for('controllers.login'))
    else:
        return redirect(url_for('controllers.accueil'))
    
@app.route('/signup_utilisateur', methods=['GET', 'POST'])
def signup_utilisateur():
    nom = request.form['nom']
    prenom = request.form['prenom']
    mail = request.form['mail']
    mdp = request.form['mdp']
    age = request.form['age']
    taille = request.form['taille']
    poids = request.form['poids']
    sexe = request.form['sexe']
    diete = 1
    utilisateur_courrant = Utilisateur(nom=nom, prenom=prenom, mail=mail, mdp=mdp, age=age, taille=taille, poids=poids, sexe=sexe, diete=diete)
    db.session.add(utilisateur_courrant)
    db.session.commit()
    return redirect(url_for('controllers.accueil'))