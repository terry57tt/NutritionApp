from setup_sql import db, MAX_RESULTS
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
        if(self.portions_associees()):
            return sum([portion.kcal_portion() for portion in self.portions_associees()])
        else:
            return 0
    
    def total_proteines(self):
        if(self.portions_associees()):
            return sum([portion.proteines_portion() for portion in self.portions_associees()])
        else:
            return 0
    
    def total_glucides(self):
        if(self.portions_associees()):
            return sum([portion.glucides_portion() for portion in self.portions_associees()])
        else:
            return 0
            
    def total_lipides(self):
        if(self.portions_associees()):
            return sum([portion.lipides_portion() for portion in self.portions_associees()])
        else:
            return 0
        
    def total_kcal_portion(self,int):
        if(self.portions_associees()):
            return sum([portion.kcal_portion() for portion in self.portions_associees() if portion.label_portion == int])
        else:
            return 0
        
    def total_proteines_portion(self,int):
        if(self.portions_associees()):
            return sum([portion.proteines_portion() for portion in self.portions_associees() if portion.label_portion == int])
        else:
            return 0
        
    def total_glucides_portion(self,int):
        if(self.portions_associees()):
            return sum([portion.glucides_portion() for portion in self.portions_associees() if portion.label_portion == int])
        else:
            return 0
        
    def total_lipides_portion(self,int):
        if(self.portions_associees()):
            return sum([portion.lipides_portion() for portion in self.portions_associees() if portion.label_portion == int])
        else:
            return 0
        
    def search_by_titre(filter_value):
        return Diete.query.filter(Diete.titre_diete.like('%' + filter_value + '%')).limit(MAX_RESULTS).all()
    
    def jsonformat(self):
        createur = self.createur_obj.jsonformat() if self.createur_obj else None
        return {
            'id': self.id,
            'titre_diete': self.titre_diete,
            'createur': createur,
            'date': self.date,
        }