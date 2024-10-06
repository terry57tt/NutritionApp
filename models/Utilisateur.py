from setup_sql import db
from models.Diete import Diete
from flask_login import login_manager
from werkzeug.security import generate_password_hash
import datetime
import secrets
import hashlib

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=True)
    prenom = db.Column(db.String(255), nullable=True)
    mail = db.Column(db.String(255), nullable=True)
    mdp = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    taille = db.Column(db.Integer, nullable=True)
    poids = db.Column(db.Integer, nullable=True)
    sexe = db.Column(db.String(255), nullable=True)
    objectif = db.Column(db.Integer, nullable=True) # 0 = sèche, 1 = maintien, 2 = prise de masse
    activite = db.Column(db.Integer, nullable=True) # 0 = sédentaire, 1 = légère, 2 = modérée, 3 = intense...
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    diete_obj = db.relationship('Diete', backref=db.backref('utilisateurs'), foreign_keys=[diete])

    def __init__(self, nom="", mail=None, mdp=None, prenom="", age="", taille="", poids="", sexe="homme", objectif=1, activite=2, diete=None, reset_token=None, reset_token_expiration=None):
        self.nom = nom
        self.mail = mail
        self.mdp = generate_password_hash(mdp)
        self.prenom = prenom
        self.age = age
        self.taille = taille
        self.poids = poids
        self.sexe = sexe
        self.objectif = objectif
        self.activite = activite
        self.diete = diete
        self.reset_token = reset_token
        self.reset_token_expiration = reset_token_expiration

    def get_reset_token(self, expiration_minutes=30):
        token = secrets.token_urlsafe(32)
        self.reset_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
        self.reset_token_expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
        return token
    
    def filter_by_token(token):
        test_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
        return Utilisateur.query.filter_by(reset_token=test_token).first()
    
    def get_token(self):
        return self.reset_token
    
    def is_reset_token_valid(self):
        return self.reset_token_expiration is not None and datetime.datetime.utcnow() < self.reset_token_expiration

    def reset_password(self, new_password):
        self.mdp = generate_password_hash(new_password)
        self.reset_token = None
        self.reset_token_expiration = None
        
    def get_id(self):
        return self.id
    
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    @staticmethod
    def get_by_id(id):
        return Utilisateur.query.get(id)
    
    @staticmethod
    def get_all():
        return Utilisateur.query.order_by(Utilisateur.nom).all()

    def mail_partie1(self):
        return self.mail.split('@')[0]
    
    def mail_partie2(self):
        return self.mail.split('@')[1]
    
    def jsonformat(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'mail': self.mail,
            'age': self.age,
            'taille': self.taille,
            'poids': self.poids,
            'sexe': self.sexe,
        }
