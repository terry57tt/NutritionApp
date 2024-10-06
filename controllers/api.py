from flask import render_template, request
from flask.blueprints import Blueprint
from openfoodfacts import API, APIVersion, Country, Environment, Flavor

from controllers import app

""" api_connection = API(
    country=Country.fr,
    flavor=Flavor.off,
    version=APIVersion.v3,
    environment=Environment.org,
) """
""" 
@app.route('/api_recherche')
def api_recherche():
    return render_template('api/api_recherche.html')

@app.route('/api_request', methods=['GET', 'POST'])
def api_request():
    if request.method == 'POST':
        recherche = request.form['recherche']
        results = api_connection.product.text_search(recherche)
        return render_template('api/api_affiche.html', results=results)
    return render_template('api/api_recherche.html') """
