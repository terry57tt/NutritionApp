from setup_sql import db
from models.Diete import Diete

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
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))

    diete_obj = db.relationship('Diete', backref=db.backref('utilisateurs'), foreign_keys=[diete])

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
