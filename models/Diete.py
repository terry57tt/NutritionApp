from setup_sql import db, MAX_RESULTS
from models.Portion import Portion
from models.Aliment import Aliment


class Diete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_diete = db.Column(db.String(255), nullable=True)  # nom de la diete
    createur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)

    createur_obj = db.relationship('Utilisateur', backref=db.backref('dietes'), foreign_keys=[createur])

    def get_by_id(id):
        return Diete.query.get(id)

    def get_all():
        return Diete.query.order_by(Diete.date.desc()).all()

    def portions_associees(self):
        return Portion.query.join(Aliment).filter(Portion.diete == self.id).order_by(Portion.label_portion,
                                                                                     Aliment.titre).all()

    def total_kcal(self):
        if (self.portions_associees()):
            return sum([portion.kcal_portion() for portion in self.portions_associees()])
        else:
            return 0

    def total_proteines(self):
        if (self.portions_associees()):
            return sum([portion.proteines_portion() for portion in self.portions_associees()])
        else:
            return 0

    def total_glucides(self):
        if (self.portions_associees()):
            return sum([portion.glucides_portion() for portion in self.portions_associees()])
        else:
            return 0

    def total_lipides(self):
        if (self.portions_associees()):
            return sum([portion.lipides_portion() for portion in self.portions_associees()])
        else:
            return 0

    def total_kcal_meal(self, meal_number):
        if self.portions_associees():
            return sum(
                [portion.kcal_portion() for portion in self.portions_associees() if
                 portion.label_portion == meal_number])
        else:
            return 0

    # return the total of a specific nutriment in gram for a specific meal number
    def total_nutriment_portion(self, meal_number, nutriment):
        if self.portions_associees():
            return sum(
                [getattr(portion, f'{nutriment}_portion')() for portion in self.portions_associees() if
                 portion.label_portion == meal_number]
            )
        else:
            return 0

    # return the total of grams of proteins for a specific meal number
    def total_proteines_portion(self, meal_number):
        return self.total_nutriment_portion(meal_number, 'proteines')

    # return the total of grams of glucides for a specific meal number
    def total_glucides_portion(self, meal_number):
        return self.total_nutriment_portion(meal_number, 'glucides')

    # return the total of grams of lipides for a specific meal number
    def total_lipides_portion(self, meal_number):
        return self.total_nutriment_portion(meal_number, 'lipides')

    def search_by_titre(self):
        return Diete.query.filter(Diete.titre_diete.like('%' + self + '%')).limit(MAX_RESULTS).all()

    def jsonformat(self):
        createur = self.createur_obj.jsonformat() if self.createur_obj else None
        return {
            'id': self.id,
            'titre_diete': self.titre_diete,
            'createur': createur,
            'date': self.date,
        }

    def sets_of_portions(self):
        portions_diet = self.portions_associees()

        portions_par_type = {}

        for portion in portions_diet:
            type_portion = portion.label_portion
            if type_portion not in portions_par_type:
                portions_par_type[type_portion] = []
            portions_par_type[type_portion].append(portion)

        sets_of_portions = list(portions_par_type.values())
        return sets_of_portions

    # give percentage of g per macro for a specific meal number
    def percentage_of_g_per_macro(self, meal_number, macro):
        total_g = self.total_proteines_portion(meal_number) + self.total_glucides_portion(
            meal_number) + self.total_lipides_portion(meal_number)
        if total_g == 0:
            return 0
        if macro == "proteines":
            return self.total_proteines_portion(meal_number) / total_g * 100
        elif macro == "glucides":
            return self.total_glucides_portion(meal_number) / total_g * 100
        elif macro == "lipides":
            return self.total_lipides_portion(meal_number) / total_g * 100
        else:
            return 0

    def total_kcal_portion(self):
        return sum([self.total_kcal_meal(i) for i in range(1, 5)])
