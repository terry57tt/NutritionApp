import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.orm import joinedload

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from models import *

''' Mise à jour de la base de données
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
flask shell
from app import db
db.create_all()'''

# ----------------- Accueil ----------------- #

# page d'accueil
@app.route('/')
def accueil():
    # TODO: Récupérer l'utilisateur courrant
    utilisateur_courrant = utilisateur.query.filter_by(id=1).first()
    diet = diete.query.get(utilisateur_courrant.diete)
    return render_template('accueil.html', utilisateur=utilisateur_courrant, diete=diet)

# ----------------- Diètes ----------------- #

# page des diètes
@app.route('/dietes')
def dietes():
    dietes = diete.query.all()
    current_date = date.today().isoformat()
    return render_template('dietes.html', dietes=dietes, date=current_date)

@app.route('/ajouter_diete', methods=['GET', 'POST'])
def ajouter_diete():
    createur_id = 1
    titre = request.form['titre']
    date_today = datetime.now()
    diet = diete(titre_diete=titre, createur=createur_id, date=date_today)
    db.session.add(diet)
    db.session.commit()

    # TODO : id = diet.id
    return redirect(url_for('creer_diete', id=1))

@app.route('/modifier_diete/<int:id>', methods=['GET', 'POST'])
def modifier_diete(id):
    return redirect('/dietes')

@app.route('/supprimer_diete/<int:id>', methods=['GET', 'POST'])
def supprimer_diete(id):
    diete.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/dietes')

@app.route('/voir_diete/<int:id>', methods=['GET', 'POST'])
def voir_diete(id):
    diet = diete.query.get(id)
    return render_template('display_diete.html', diete=diet, meals=meals, aliments=aliments)

@app.route('/print_diete/<int:id>', methods=['GET', 'POST'])
def print_diete(id):
    return redirect('/dietes')

#changer_diete
@app.route('/changer_diete/<int:id_utilisateur>', methods=['GET', 'POST'])
def changer_diete(id_utilisateur):
    utilisateur_courrant = utilisateur.query.filter_by(id=id_utilisateur).first()
    dietes = diete.query.all()
    return render_template('changer_diete.html', utilisateur=utilisateur_courrant, dietes=dietes)

@app.route('/choisir_diete/<int:id>/<int:id_utilisateur>', methods=['GET', 'POST'])
def choisir_diete(id, id_utilisateur):
    utilisateur_courrant = utilisateur.query.filter_by(id=id_utilisateur).first()
    utilisateur_courrant.diete = id
    db.session.commit()
    return redirect(url_for('accueil'))

# ----------------- Aliments ----------------- #

@app.route('/aliments')
def aliments():
    aliments = aliment.query.all()
    return render_template('aliments.html', aliments=aliments)

@app.route('/ajouter_aliment', methods=['GET', 'POST'])
def ajouter_aliment():
    if request.method == 'POST':
        titre = request.form['titre']
        kcal = int(request.form['kcal']) if request.form['kcal'] else None
        proteines = int(request.form['proteines']) if request.form['proteines'] else None
        glucides = int(request.form['glucides']) if request.form['glucides'] else None
        lipides = int(request.form['lipides']) if request.form['lipides'] else None
        categorie = request.form['categorie']
        photo = request.form['photo']
        description = request.form['description']
        unite = 'unite' in request.form

        food = aliment(
            titre=titre,
            kcal=kcal,
            proteines=proteines,
            glucides=glucides,
            lipides=lipides,
            categorie=categorie,
            photo=photo,
            description=description,
            unite=unite
        )

        db.session.add(food)
        db.session.commit()

        # Redirection vers une autre page après l'ajout de l'aliment
        return redirect('/aliments')

    return render_template('ajouter_aliment.html')

@app.route('/modifier_aliment/<int:id>', methods=['GET', 'POST'])
def modifier_aliment(id):
    return redirect('/aliments')

@app.route('/supprimer_aliment/<int:id>', methods=['GET', 'POST'])
def supprimer_aliment(id):
    aliment.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/aliments')

# ----------------- Reglages ----------------- #

@app.route('/reglages')
def reglages():
    return render_template('reglages.html')

# ----------------- Repas ----------------- #

'''
@app.route('/meals/<int:id>', methods=['GET', 'POST'])
def meals(id):
    if request.method == 'POST':
        titre = request.form['titre']
        type = request.form['type']
        label = request.form['label']
        
        meal = repas(titre=titre, type=type, label=label)
        db.session.add(meal)
        db.session.commit()
        
        return redirect(url_for('repas'))
    else:
        repas_list = repas.query.all()

        repas_lies = (
                repas.query
                .join(estCompose)
                .filter(estCompose.diete == id)
                .options(joinedload(repas.est_composes))
                .all()
            )
        
        return render_template('repas.html', repas=repas_list, repas_lies=repas_lies, diete_id=id)


#add_to_diet
@app.route('/add_to_diet/<int:id>/<int:diete_id>', methods=['GET', 'POST'])
def add_to_diet(id, diete_id):
    relation = estCompose(diete=diete_id, repas=id)
    # TODO : flash message si déjà dans la diète
    if estCompose.query.filter(estCompose.diete == diete_id, estCompose.repas == id).first():
        return redirect(url_for('meals', id=diete_id))
    db.session.add(relation)
    db.session.commit()
    
    return redirect(url_for('meals', id=diete_id))

# enlever repas de la diète
@app.route('/enlever_repas/<int:id>/<int:diete_id>', methods=['GET', 'POST'])
def enlever_repas(id, diete_id):
    relation = estCompose.query.filter(estCompose.diete == diete_id, estCompose.repas == id).first()
    db.session.delete(relation)    
    db.session.commit()
    
    return redirect(url_for('meals', id=diete_id))

#ajouter_repas
@app.route('/ajouter_repas', methods=['GET', 'POST'])
def ajouter_repas():
    if request.method == 'POST':
        titre = request.form['titre']
        type = request.form['type']
        label = request.form['label']
        
        meal = repas(titre=titre, type=type, label=label)
        db.session.add(meal)
        db.session.commit()
        
        return redirect(url_for('repas'))
    else:
        return render_template('ajouter_repas.html')
    
# creer_diete
@app.route('/creer_diete', methods=['GET', 'POST'])
def creer_diete():
    if request.method == 'POST':
        titre = request.form['titre']
        type = request.form['type']
        label = request.form['label']
        
        meal = repas(titre=titre, type=type, label=label)
        db.session.add(meal)
        db.session.commit()
        
        return redirect(url_for('custom_meal', id=meal.id))
    else:
        return render_template('creer_diete.html')
'''

# créer une diète
@app.route('/creer_diete/<int:id>', methods=['GET', 'POST'])
def creer_diete(id):
    diete_courante = diete.query.get(id)
    portions_repas = diete_courante.portions_associees()

    aliments = aliment.query.all()
    return render_template('creer_diete.html', aliments=aliments, id_diete=id, portions_repas=portions_repas)
 
@app.route('/ajouter_aliment_diete/<int:id_aliment>/<int:id_diete>/<int:quantite>', methods=['GET', 'POST'])
def ajouter_aliment_diete(id_aliment, id_diete, quantite):
    nouvelle_portion = portion(diete=id_diete, aliment=id_aliment, nombre=quantite, label_portion='matin')
        
    db.session.add(nouvelle_portion)
    db.session.commit()

    return redirect(url_for('creer_diete', id=id_diete))

@app.route('/enlever_aliment_diete/<int:id_portion>/<int:id_diete>', methods=['GET', 'POST'])
def enlever_aliment_diete(id_portion, id_diete):
    portion_courante = portion.query.get(id_portion)

    db.session.delete(portion_courante)    
    db.session.commit()
    
    return redirect(url_for('creer_diete', id=id_diete))

#init bdd
@app.route('/init')
def init():
    db.drop_all()
    db.create_all()
    a1 = aliment(titre='Pomme', kcal=52, proteines=0.3, glucides=13.8, lipides=0.2, categorie='fruit', photo='pomme.jpg', description='La pomme est le fruit du pommier, arbre fruitier largement cultivé. L espèce la plus cultivée est Malus domestica.', unite=True)
    a2 = aliment(titre='Banane', kcal=89, proteines=1.1, glucides=22.4, lipides=0.3, categorie='fruit', photo='banane.jpg', description='La banane est un fruit comestible, produit par diverses espèces de plantes herbacées de la famille des Musaceae.', unite=True)
    a3 = aliment(titre='Orange', kcal=47, proteines=0.9, glucides=11.8, lipides=0.2, categorie='fruit', photo='orange.jpg', description='L orange est un agrume, fruit des orangers, des arbres de la famille des Rutaceae.', unite=True)
    a4 = aliment(titre='Pain', kcal=266, proteines=8.5, glucides=50.9, lipides=1.1, categorie='feculent', photo='pain.jpg', description='Le pain est un aliment de base traditionnel de nombreuses cultures. Il se présente sous forme de miche, de miettes ou de baguette.', unite=True)

    # création de la diète
    date = datetime.now()

    d1 = diete(titre_diete='Diète Pat Sèche 2500', createur=1, date=date)
    d2 = diete(titre_diete='Diète Pat Pdm 4000', createur=1, date=date)

    # création des portions
    p1 = portion(diete=1, aliment=1, nombre=1, label_portion='matin')
    p2 = portion(diete=1, aliment=2, nombre=1, label_portion='matin')
    p3 = portion(diete=1, aliment=3, nombre=1, label_portion='midi')
    p4 = portion(diete=1, aliment=4, nombre=1, label_portion='midi')
    p5 = portion(diete=1, aliment=1, nombre=1, label_portion='soir')
    p6 = portion(diete=1, aliment=2, nombre=1, label_portion='soir')

    p7 = portion(diete=2, aliment=1, nombre=1, label_portion='matin')
    p8 = portion(diete=2, aliment=2, nombre=1, label_portion='matin')
    p9 = portion(diete=2, aliment=3, nombre=1, label_portion='midi')
    p10 = portion(diete=2, aliment=4, nombre=1, label_portion='midi')
    p11 = portion(diete=2, aliment=1, nombre=1, label_portion='soir')
    p12 = portion(diete=2, aliment=2, nombre=1, label_portion='soir')

    # création de l'utilisateur terry tempestini terry57tt@gmail.com
    u1 = utilisateur(nom='Tempestini', prenom='Terry', mail='terry57tt@gmail.com', mdp='terry57tt', age=21, taille=180, poids=80, sexe='homme', diete=1)

    # ajout des données dans la base de données
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.add(a4)
    db.session.add(d1)
    db.session.add(d2)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)
    db.session.add(p6)
    db.session.add(p7)
    db.session.add(p8)
    db.session.add(p9)
    db.session.add(p10)
    db.session.add(p11)
    db.session.add(p12)
    db.session.add(u1)

    db.session.commit()

    return redirect(url_for('accueil'))