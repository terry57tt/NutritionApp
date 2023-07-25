from setup_sql import db
from models.Portion import Portion
from models.Aliment import Aliment

class Diete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_diete = db.Column(db.String(255), nullable=True) # nom de la diete
    createur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)

    createur_obj = db.relationship('Utilisateur', backref=db.backref('dietes'), foreign_keys=[createur])
    
    def get_by_id(id):
        return Diete.query.get(id)
    
    def get_all():
        return Diete.query.order_by(Diete.date.desc()).all()
    
    def portions_associees(self):
        return Portion.query.join(Aliment).filter(Portion.diete == self.id).order_by(Portion.label_portion, Aliment.titre).all()
    
    def total_kcal(self):
        return sum([portion.kcal_portion() for portion in self.portions_associees()])
    
    def total_proteines(self):
        return sum([portion.proteines_portion() for portion in self.portions_associees()])
    
    def total_glucides(self):
        return sum([portion.glucides_portion() for portion in self.portions_associees()])
    
    def total_lipides(self):
        return sum([portion.lipides_portion() for portion in self.portions_associees()])