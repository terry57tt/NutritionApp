from setup_sql import db, MAX_RESULTS

class Suivi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=True, server_default='')
    poids = db.Column(db.Integer, nullable=True, server_default='0')
    taux_masse_grasse = db.Column(db.Integer, nullable=True, server_default='0')
    bras = db.Column(db.Integer, nullable=True, server_default='0')
    epaules = db.Column(db.Integer, nullable=True, server_default='0')
    poitrine = db.Column(db.Integer, nullable=True, server_default='0')
    tour_taille = db.Column(db.Integer, nullable=True, server_default='0')
    cuisses = db.Column(db.Integer, nullable=True, server_default='0')
    mollets = db.Column(db.Integer, nullable=True, server_default='0')

    personne = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    personne_obj = db.relationship('Utilisateur', backref=db.backref('suivis'), foreign_keys=[personne])

    def __init__(self, date="", poids="", taux_masse_grasse="", bras="", epaules="", poitrine="", tour_taille="", cuisses="", mollets="", personne=""):
        self.date = date
        self.poids = poids
        self.taux_masse_grasse = taux_masse_grasse
        self.bras = bras
        self.epaules = epaules
        self.poitrine = poitrine
        self.tour_taille = tour_taille
        self.cuisses = cuisses
        self.mollets = mollets
        self.personne = personne

    def get_by_id(id):
        return Suivi.query.get(id)
    
    def delete(self):
        db.session.delete(self)

    def filter_by_personne(personne_id):
        return Suivi.query.filter(Suivi.personne == personne_id).order_by(Suivi.date.asc()).limit(MAX_RESULTS).all()
    
    def filter_by_date(date):
        return Suivi.query.filter(Suivi.date == date).order_by(Suivi.date.desc()).limit(MAX_RESULTS).all()

    def filter_by_date_and_personne(date, personne_id):
        return Suivi.query.filter(
            Suivi.date == date,
            Suivi.personne == personne_id
        ).order_by(Suivi.date.desc()).limit(MAX_RESULTS).all()     

    def jsonformat(self):
        personne = self.personne_obj.jsonformat() if self.personne_obj else None
        return {
            'id': self.id,
            'date': self.date,
            'poids': self.poids,
            'taux_masse_grasse': self.taux_masse_grasse,
            'bras': self.bras,
            'epaules': self.epaules,
            'poitrine': self.poitrine,
            'tour_taille': self.tour_taille,
            'cuisses': self.cuisses,
            'mollets': self.mollets,
            'personne': personne,
        }