from flask import render_template, request, redirect, url_for, flash, Response
from models.Utilisateur import Utilisateur
from setup_sql import db

from controllers import app

@app.route('/reglages')
def reglages():
    utilisateur_courrant = Utilisateur.get_by_id(1)
    return render_template('reglages/reglages.html', utilisateur=utilisateur_courrant)

@app.route('/modifier_utilisateur/<int:id>', methods=['GET', 'POST'])
def modifier_utilisateur(id):
    utilisateur_courrant = Utilisateur.get_by_id(id)
    if request.method == 'POST':
        utilisateur_courrant.nom = request.form['nom']
        utilisateur_courrant.prenom = request.form['prenom']
        partie1 = request.form['mail']
        partie2 = request.form['boite_mail']
        utilisateur_courrant.mail = partie1 + '@' + partie2
        utilisateur_courrant.age = request.form['age']
        utilisateur_courrant.taille = request.form['taille']
        utilisateur_courrant.poids = request.form['poids']
        utilisateur_courrant.sexe = request.form['sexe']

        db.session.commit()

        flash('Les informations ont été modifiées avec succès', 'success')
        return redirect(url_for('controllers.reglages'))