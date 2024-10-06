from flask import render_template, request, redirect, url_for, flash, Response
from models.Utilisateur import Utilisateur
from setup_sql import db
from flask_login import login_required, current_user

from controllers import app


@app.route('/reglages')
@login_required
def reglages():
    utilisateur_courrant = current_user
    return render_template('reglages/reglages.html', utilisateur=utilisateur_courrant)


@app.route('/modifier_utilisateur/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_utilisateur(id):
    utilisateur_courrant = Utilisateur.get_by_id(id)
    if request.method == 'POST':
        utilisateur_courrant.nom = request.form['nom']
        utilisateur_courrant.prenom = request.form['prenom']
        utilisateur_courrant.age = request.form['age']
        utilisateur_courrant.taille = request.form['taille']
        utilisateur_courrant.poids = request.form['poids']
        utilisateur_courrant.sexe = request.form['sexe']
        utilisateur_courrant.objectif = request.form['objectif']
        utilisateur_courrant.activite = request.form['activite']

        db.session.commit()

        flash('Les informations ont été modifiées avec succès', 'success')
        return redirect(url_for('controllers.reglages'))
