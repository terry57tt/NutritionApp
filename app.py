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
flask shell
from app import db
db.create_all()'''

@app.route('/')
def index():
    # TODO: Récupérer l'utilisateur courrant
    utilisateur_courrant = utilisateur.query.filter_by(id=1).first()
    diet = diete.query.get(utilisateur_courrant.diete)
    return render_template('index.html', utilisateur=utilisateur_courrant, diete=diet)

@app.route('/add')
def hello():
    a = aliment(titre='nothing')
    db.session.add(a)
    db.session.commit()
    return 'Add'

@app.route('/dietes')
def dietes():
    dietes = diete.query.all()
    current_date = date.today().isoformat()
    return render_template('dietes.html', dietes=dietes, date=current_date)

@app.route('/aliments')
def aliments():
    aliments = aliment.query.all()
    return render_template('aliments.html', aliments=aliments)

@app.route('/reglages')
def reglages():
    return render_template('reglages.html')

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

#modifier_aliment
@app.route('/modifier_aliment/<int:id>', methods=['GET', 'POST'])
def modifier_aliment(id):
    return redirect('/aliments')

#supprimer_aliment
@app.route('/supprimer_aliment/<int:id>', methods=['GET', 'POST'])
def supprimer_aliment(id):
    aliment.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/aliments')

@app.route('/ajouter_diete', methods=['GET', 'POST'])
def ajouter_diete():
    createur_id = 1
    titre = request.form['titre']
    date_today = datetime.now()
    diet = diete(titre_diete=titre, createur=createur_id, date=date_today)
    db.session.add(diet)
    db.session.commit()

    # TODO : id = diet.id
    return redirect(url_for('meals', id=1))

    
#modifier_diete
@app.route('/modifier_diete/<int:id>', methods=['GET', 'POST'])
def modifier_diete(id):
    return redirect('/dietes')

#supprimer_diete
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
    
# creation_repas
@app.route('/creation_repas', methods=['GET', 'POST'])
def creation_repas():
    if request.method == 'POST':
        titre = request.form['titre']
        type = request.form['type']
        label = request.form['label']
        
        meal = repas(titre=titre, type=type, label=label)
        db.session.add(meal)
        db.session.commit()
        
        return redirect(url_for('custom_meal', id=meal.id))
    else:
        return render_template('creation_repas.html')

# custom_meal
@app.route('/custom_meal/<int:id>', methods=['GET', 'POST'])
def custom_meal(id):
    portions_from_meal = db.session.query(portion).filter(portion.repas == id).all()

    aliments = aliment.query.all()
    return render_template('creation_repas.html', aliments=aliments, repas_id=id, portions_from_meal=portions_from_meal)
 
# add aliment to meal
@app.route('/add_to_meal/<int:id>/<int:diete_id>', methods=['GET', 'POST'])
def add_to_meal(id, diete_id):
    quantite = request.args.get('quantite')
    part = portion(repas=diete_id, aliment=id, nombre=quantite)
    if portion.query.filter(portion.repas == diete_id, portion.aliment == id).first():
        return redirect(url_for('custom_meal', id=diete_id))    
    db.session.add(part)
    db.session.commit()
    return redirect(url_for('custom_meal', id=diete_id))

@app.route('/remove_from_meal/<int:id>/<int:diete_id>', methods=['GET', 'POST'])
def remove_from_meal(id, diete_id):
    part = portion.query.filter(portion.repas == diete_id, portion.aliment == id).first()
    db.session.delete(part)    
    db.session.commit()
    
    return redirect(url_for('custom_meal', id=diete_id))

#init bdd
@app.route('/init')
def init():
    db.drop_all()
    db.create_all()
    a1 = aliment(titre='Pomme', kcal=52, proteines=0.3, glucides=13.8, lipides=0.2, categorie='fruit', photo='pomme.jpg', description='La pomme est le fruit du pommier, arbre fruitier largement cultivé. L espèce la plus cultivée est Malus domestica.', unite=True)
    a2 = aliment(titre='Banane', kcal=89, proteines=1.1, glucides=22.4, lipides=0.3, categorie='fruit', photo='banane.jpg', description='La banane est un fruit comestible, produit par diverses espèces de plantes herbacées de la famille des Musaceae.', unite=True)
    a3 = aliment(titre='Orange', kcal=47, proteines=0.9, glucides=11.8, lipides=0.2, categorie='fruit', photo='orange.jpg', description='L orange est un agrume, fruit des orangers, des arbres de la famille des Rutaceae.', unite=True)
    a4 = aliment(titre='Pain', kcal=266, proteines=8.5, glucides=50.9, lipides=1.1, categorie='feculent', photo='pain.jpg', description='Le pain est un aliment de base traditionnel de nombreuses cultures. Il se présente sous forme de miche, de miettes ou de baguette.', unite=True)

    # crétaion des repas
    r1 = repas(titre='Galette de riz', type='Matin', label='Prise de masse')
    r2 = repas(titre='Poulet et brocolis', type='Midi', label='Maintien')
    r3 = repas(titre='Patate douce poisson', type='Soir', label='Sèche')

    # le repas 1 est composé de 100g de pomme, 250g de banane et 40g d'orange
    p1 = portion(repas=1, aliment=1, nombre=100)
    p2 = portion(repas=1, aliment=2, nombre=250)
    p3 = portion(repas=1, aliment=3, nombre=40)

    # le repas 2 est composé de 100g de pain, 200g de poulet et 100g de brocolis
    p4 = portion(repas=2, aliment=4, nombre=100)
    p5 = portion(repas=2, aliment=1, nombre=200)
    p6 = portion(repas=2, aliment=2, nombre=100)

    # le repas 3 est composé de 100g de patate douce, 200g de poisson et 100g de brocolis
    p7 = portion(repas=3, aliment=4, nombre=100)
    p8 = portion(repas=3, aliment=1, nombre=200)
    p9 = portion(repas=3, aliment=2, nombre=100)

    # création de la diète
    d1 = diete(titre_diete='Diète Pat Sèche 2500', createur=1)
    d2 = diete(titre_diete='Diète Pat Pdm 4000', createur=1)

    # la diète 1 est composée du repas 1, 2 et 3
    e1 = estCompose(diete=1, repas=1)
    e2 = estCompose(diete=1, repas=2)
    e3 = estCompose(diete=1, repas=3)

    # création de l'utilisateur terry tempestini terry57tt@gmail.com
    u1 = utilisateur(nom='Tempestini', prenom='Terry', mail='terry57tt@gmail.com', mdp='terry57tt', age=21, taille=180, poids=80, sexe='homme', diete=1)

    # ajout des données dans la base de données
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.add(a4)
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)
    db.session.add(p6)
    db.session.add(p7)
    db.session.add(p8)
    db.session.add(p9)
    db.session.add(d1)
    db.session.add(d2)
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)
    db.session.add(u1)

    db.session.commit()

    students = aliment.query.all()
    return render_template('index.html', students=students)