import os
from flask import Flask, render_template, request, url_for, redirect, flash, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.orm import joinedload
import pdfkit
from urllib.parse import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.add_extension('jinja2.ext.do')
db = SQLAlchemy(app)
from models import *



# ----------------- Accueil ----------------- #

# page d'accueil
@app.route('/')
def accueil():
    # TODO: Récupérer l'utilisateur courrant
    utilisateur_courrant = utilisateur.query.filter_by(id=1).first()
    diet = diete.query.get(utilisateur_courrant.diete)
    return render_template('accueil.html', utilisateur=utilisateur_courrant, diete=diet)

# ----------------- Login ----------------- #
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login_utilisateur', methods=['GET', 'POST'])
def login_utilisateur():
    mail = request.form['mail']
    mdp = request.form['mdp']
    utilisateur_courrant = utilisateur.query.filter_by(mail=mail).first()
    if utilisateur_courrant is None:
        return redirect(url_for('login'))
    elif utilisateur_courrant.mdp != mdp:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('accueil'))
    
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
    utilisateur_courrant = utilisateur(nom=nom, prenom=prenom, mail=mail, mdp=mdp, age=age, taille=taille, poids=poids, sexe=sexe, diete=diete)
    db.session.add(utilisateur_courrant)
    db.session.commit()
    return redirect(url_for('accueil'))

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
    return redirect(url_for('creer_diete', id = diet.id))

@app.route('/modifier_diete/<int:id>', methods=['GET', 'POST'])
def modifier_diete(id):
    return redirect(url_for('creer_diete', id = id))

@app.route('/supprimer_diete/<int:id>', methods=['GET', 'POST'])
def supprimer_diete(id):
    diete.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/dietes')

@app.route('/voir_diete/<int:id>', methods=['GET', 'POST'])
def voir_diete(id):
    diet = diete.query.get(id)
    return render_template('display_diete.html', root = default_root(), diete=diet)

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

def default_root():
    parsed_url = urlparse(request.url)
    return parsed_url.scheme + "://" + parsed_url.netloc

@app.route('/print_diete_pdf/<int:id_diete>', methods=['GET', 'POST'])
def print_diete_pdf(id_diete):
    utilisateur_courrant = utilisateur.query.filter_by(id=1).first()
    diet = diete.query.get(utilisateur_courrant.diete)
    out = render_template("diete_pdf.html", root = default_root(), diete=diet, navbar=False, utilisateur=utilisateur_courrant)
    return html_to_pdf(out)

def html_to_pdf(html,filename='diete.pdf',download=False):
    pdf = pdfkit.from_string(html, False)
    response = Response(pdf, mimetype='application/pdf')
    if download :
        response.headers.set('Content-Disposition', f'attachment; filename={filename}')
    return response


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


# créer une diète
@app.route('/creer_diete/<int:id>', methods=['GET', 'POST'])
def creer_diete(id):
    diete_courante = diete.query.get(id)
    portions_repas = diete_courante.portions_associees()

    aliments = aliment.query.all()
    return render_template('creer_diete.html', aliments=aliments, diete=diete_courante, portions_repas=portions_repas)
 
@app.route('/ajouter_aliment_diete/<int:id_aliment>/<int:id_diete>/<int:quantite>/<int:label>', methods=['GET', 'POST'])
def ajouter_aliment_diete(id_aliment, id_diete, quantite, label):
    nouvelle_portion = portion(diete=id_diete, aliment=id_aliment, nombre=quantite, label_portion=label)
    
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
    
    a1 = aliment(titre='Blanc d\'œuf', kcal=52, proteines=11, glucides=0, lipides=0, categorie='protéine', photo='', description='', unite=0)
    a2 = aliment(titre='Farine de patate douce', kcal=363, proteines=0, glucides=0, lipides=0, categorie='féculent', photo='', description='', unite=0)
    a3 = aliment(titre='WHEY ISOLAT', kcal=346, proteines=90, glucides=0, lipides=0, categorie='protéine', photo='', description='', unite=0)
    a4 = aliment(titre='Yaourt 0% 125g', kcal=50, proteines=0, glucides=0, lipides=0, categorie='lactose', photo='', description='', unite=1)
    a5 = aliment(titre='Poulet', kcal=150, proteines=30, glucides=0, lipides=0, categorie='viande', photo='', description='', unite=0)
    a6 = aliment(titre='Patate douce', kcal=86, proteines=0, glucides=0, lipides=0, categorie='féculent', photo='', description='', unite=0)
    a7 = aliment(titre='Brocolis', kcal=50, proteines=0, glucides=0, lipides=0, categorie='légume', photo='', description='', unite=0)
    a8 = aliment(titre='Huile d\'olive', kcal=884, proteines=0, glucides=0, lipides=100, categorie='matière grasse', photo='', description='', unite=0)
    a9 = aliment(titre='Caséine', kcal=343, proteines=80, glucides=0, lipides=0, categorie='protéine', photo='', description='', unite=0)
    a10 = aliment(titre='Glutamine', kcal=420, proteines=0, glucides=0, lipides=0, categorie='complément alimentaire', photo='', description='', unite=0)
    a11 = aliment(titre='Flocons d\'avoine', kcal=350, proteines=8, glucides=0, lipides=0, categorie='féculent', photo='', description='', unite=0)
    a12 = aliment(titre='Haricots verts', kcal=31, proteines=0, glucides=0, lipides=0, categorie='légume', photo='', description='', unite=0)
    a13 = aliment(titre='Jaune d\'œuf', kcal=55, proteines=0, glucides=0, lipides=0, categorie='protéine', photo='', description='', unite=1)
    a14 = aliment(titre='Pomme', kcal=52, proteines=0, glucides=13.8, lipides=0.2, categorie='fruit', photo='', description='', unite=1)
    a15 = aliment(titre='Banane', kcal=105, proteines=0, glucides=22.4, lipides=0.3, categorie='fruit', photo='', description='', unite=1)
    a16 = aliment(titre='Riz', kcal=355, proteines=0, glucides=0, lipides=0, categorie='féculent', photo='', description='', unite=0)
    a17 = aliment(titre='Noix', kcal=654, proteines=0, glucides=0, lipides=0, categorie='fruit à coque', photo='', description='', unite=0)
    a18 = aliment(titre='Concombre', kcal=13, proteines=0, glucides=0, lipides=0, categorie='légume', photo='', description='', unite=0)
    a19 = aliment(titre='Poisson blanc', kcal=172, proteines=0, glucides=0, lipides=0, categorie='poisson', photo='', description='', unite=0)
    
    # création de la diète
    date = datetime.now()

    d1 = diete(titre_diete='Diète Pat Sèche 2500', createur=1, date=date)
    d2 = diete(titre_diete='Diète Pat Pdm 4000', createur=1, date=date)

    # création des portions
    # 1 = matin, 2 = collation matin, 3 = midi, 4 = collation midi, 5 = soir, 6 = collation soir
    p1 = portion(diete=1, aliment=1, nombre=200, label_portion=1)
    p2 = portion(diete=1, aliment=2, nombre=20, label_portion=1)
    p3 = portion(diete=1, aliment=3, nombre=40, label_portion=2)
    p4 = portion(diete=1, aliment=4, nombre=1, label_portion=2)
    p5 = portion(diete=1, aliment=5, nombre=160, label_portion=3)
    p6 = portion(diete=1, aliment=6, nombre=130, label_portion=3)
    p7 = portion(diete=1, aliment=7, nombre=150, label_portion=3)
    p8 = portion(diete=1, aliment=8, nombre=10, label_portion=3)
    p9 = portion(diete=1, aliment=3, nombre=40, label_portion=4)
    p10 = portion(diete=1, aliment=12, nombre=150, label_portion=4)
    p11 = portion(diete=1, aliment=5, nombre=160, label_portion=5)
    p12 = portion(diete=1, aliment=6, nombre=130, label_portion=5)
    p13 = portion(diete=1, aliment=7, nombre=150, label_portion=5)
    p14 = portion(diete=1, aliment=8, nombre=10, label_portion=5)
    p15 = portion(diete=1, aliment=9, nombre=30, label_portion=6)
    p16 = portion(diete=1, aliment=17, nombre=30, label_portion=6)

    p18 = portion(diete=2, aliment=1, nombre=200, label_portion=1)
    p19 = portion(diete=2, aliment=2, nombre=1, label_portion=1)
    p20 = portion(diete=2, aliment=3, nombre=40, label_portion=2)
    p21 = portion(diete=2, aliment=6, nombre=1, label_portion=2)
    p22 = portion(diete=2, aliment=5, nombre=250, label_portion=3)
    p23 = portion(diete=2, aliment=9, nombre=80, label_portion=3)
    p24 = portion(diete=2, aliment=10, nombre=100, label_portion=3)
    p25 = portion(diete=2, aliment=11, nombre=10, label_portion=3)
    p26 = portion(diete=2, aliment=5, nombre=40, label_portion=4)
    p27 = portion(diete=2, aliment=12, nombre=30, label_portion=4)
    p28 = portion(diete=2, aliment=5, nombre=200, label_portion=5)
    p29 = portion(diete=2, aliment=9, nombre=80, label_portion=5)
    p30 = portion(diete=2, aliment=10, nombre=100, label_portion=5)
    p31 = portion(diete=2, aliment=11, nombre=10, label_portion=5)
    p32 = portion(diete=2, aliment=13, nombre=30, label_portion=6)
    p33 = portion(diete=2, aliment=14, nombre=10, label_portion=6)
    p34 = portion(diete=2, aliment=15, nombre=30, label_portion=6)

    # création de l'utilisateur terry tempestini terry57tt@gmail.com
    u1 = utilisateur(nom='Tempestini', prenom='Terry', mail='terry57tt@gmail.com', mdp='terry57tt', age=21, taille=180, poids=80, sexe='homme', diete=1)

    # ajout des données dans la base de données
    db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19])
    db.session.add_all([d1, d2])
    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13 ,p14, p15, p16, p18, p19, p20, p21, p22, p23 ,p24, p25, p26, p27, p28, p29 ,p30, p31, p32, p33, p34])
    db.session.add(u1)

    db.session.commit()

    return redirect(url_for('accueil'))