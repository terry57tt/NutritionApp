from flask import render_template, request, redirect, url_for, flash, Response, jsonify
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from setup_sql import db
from controllers import app
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/t', methods=['GET', 'POST'])
def t():
    diete = Diete.get_by_id(1)
    all_users = Utilisateur.get_all()
    return render_template('aliment/test.html', diete=diete, all_users=all_users)

@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user = Utilisateur.get_by_id(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('controllers.t'))

@app.route('/use/<int:id>', methods=['GET', 'POST'])
def use(id):
    user = Utilisateur.get_by_id(id)
    login_user(user)
    return redirect(url_for('controllers.reglages'))

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if Utilisateur.query.filter_by(mail="terry57tt@gmail.com").first() is None:
        user = Utilisateur(nom="Terry", mail="terry57tt@gmail.com", mdp="terrypassword", prenom="Terry", age="21", taille="170", poids="68", sexe="homme")
        db.session.add(user)
        db.session.commit()
    else :
        user = Utilisateur.query.filter_by(mail="terry57tt@gmail.com").first()
    login_user(user)
    return redirect(url_for('controllers.reglages'))
    