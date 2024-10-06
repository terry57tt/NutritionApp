// ------------------ BEGIN Update on the fly ------------------------------
function updateQuantity(portionId, newQuantity) {
    // Vérifier si la nouvelle quantité est un nombre valide
    if (isNaN(newQuantity) || newQuantity < 0) {
        console.log("Invalid quantity");
        return;
    }

    // Convertir la nouvelle quantité en entier et l'arrondir
    const newQuantityInt = Math.round(parseInt(newQuantity));

    // Utiliser une URL relative ou absolue dynamique
    const url = window.location.origin + "/update_quantity/" + portionId + "/" + newQuantityInt;

    // Utiliser la méthode HTTP PUT pour mettre à jour la ressource
    $.ajax({
        url: url,
        type: "POST",
        success: function (response) {
            // Mettre à jour l'interface utilisateur avec la nouvelle quantité
            // au lieu de recharger toute la page
            window.location.reload();
            $('#portion_' + portionId + '_quantity').text(newQuantityInt);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // Afficher un message d'erreur convivial à l'utilisateur
            alert("An error occurred: " + textStatus);
            console.log(jqXHR, textStatus, errorThrown);
        }
    });
}

// ------------------ END Update on the fly ------------------------------


// ------------------ BEGIN Histogram chart ------------------------------
function update_chart_intake() {

    const fat_needed = Math.round(user_weight * FAT_PER_KG);
    const carbs_needed = Math.round(user_weight * CARBS_PER_KG);
    const protein_needed = Math.round(user_weight * PROTEIN_PER_KG);

    const data_histo_intake = {
        labels: ['Protéines', 'Glucides', 'Lipides'],
        datasets: [{
            label: 'Grammes',
            data: [total_proteines, total_glucides, total_lipides],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
            ],
            borderWidth: 1
        }]
    };

    // chart configuration : define the y_max value and the step_size
    let y_max = Math.max(total_proteines, total_glucides, total_lipides);
    y_max = Math.ceil(y_max / 10) * 10;
    let step_size = Math.ceil((y_max / 10) / 10) * 10;
    y_max = step_size * 11;

    const config_histo_intake = {
        type: 'bar',
        data: data_histo_intake,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: y_max,
                    ticks: {
                        stepSize: step_size,
                    },
                },
                x: {
                    display: true,
                },
            },
            plugins: {
                legend: {
                    display: false,
                },
                datalabels: {
                    anchor: 'end',
                    align: 'end',
                    formatter: function (value, context) {
                        return value;
                    },
                    font: {
                        weight: 'bold'
                    },
                    color: 'black'
                },
                annotation: {
                    annotations: {
                        proteinesLimit: {
                            type: 'box',
                            yMin: protein_needed,
                            yMax: protein_needed,
                            xMin: -1,
                            xMax: 0.5,
                            backgroundColor: 'rgba(255, 0, 0, 0.5)',
                            borderColor: 'red',
                            borderWidth: 2,
                            label: {
                                enabled: true,
                                content: 'Limite Protéines',
                                position: 'end',
                                backgroundColor: 'red',
                                color: 'white',
                            }
                        },
                        glucidesLimit: {
                            type: 'box',
                            yMin: carbs_needed,
                            yMax: carbs_needed,
                            xMin: 0.5,
                            xMax: 1.5,
                            backgroundColor: 'rgba(255, 0, 0, 0.5)',
                            borderColor: 'red',
                            borderWidth: 2,
                            label: {
                                enabled: true,
                                content: 'Limite Glucides',
                                position: 'end',
                                backgroundColor: 'red',
                                color: 'white',
                            }
                        },
                        lipidesLimit: {
                            type: 'box',
                            yMin: fat_needed,
                            yMax: fat_needed,
                            xMin: 1.5,
                            xMax: 2.5,
                            backgroundColor: 'rgba(255, 0, 0, 0.5)',
                            borderColor: 'red',
                            borderWidth: 2,
                            label: {
                                enabled: true,
                                content: 'Limite Lipides',
                                position: 'end',
                                backgroundColor: 'red',
                                color: 'white',
                            }
                        },
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    };

    // Création du graphique Histogramme
    const histo_chart_intake = new Chart(document.getElementById('chart_intake'), config_histo_intake);
}

// ------------------ END Histogram chart ------------------------------


// -------------------- BEGIN import diet section ----------------------------------

src = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"

let filename = "";

const repasLabels = {
    1: 'Matin',
    3: 'Midi',
    5: 'Soir',
    2: 'Collation Matin',
    4: 'Collation Après-midi',
    6: 'Collation Soir',
};

function submitForm(event) {
    event.preventDefault();

    // Create a new FormData object
    const formData = new FormData();

    // Get the CSV file
    const fichierCSV = document.getElementById("fichier_csv").files[0];
    formData.append("fichier_csv", fichierCSV);
    filename = fichierCSV.name;

    // Send a POST request to /importer_csv
    fetch("/importer_csv", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            // Process the response
            if (data.success) {
                // Get the list of unfound foods from the response
                const liste_aliments_brute = data.liste_aliments;

                // Get the container for the tables
                const repasTablesContainer = document.getElementById('aliments-non-trouves');

                repasTablesContainer.innerHTML = ''; // Clear the container

                let currentTables = {};

                // Loop through each food item
                liste_aliments_brute.forEach(aliment => {
                    const repasType = aliment.repas;

                    // If the table for this meal doesn't exist yet, create it
                    if (!currentTables[repasType]) {
                        // Create the table
                        const table = document.createElement('table');
                        table.className = 'table table-bordered table-striped';

                        // Add the table headers
                        const thead = document.createElement('thead');
                        const headerRow = document.createElement('tr');

                        // Add the meal header
                        const th = document.createElement('th');
                        th.colSpan = 3;
                        th.textContent = repasLabels[repasType];
                        headerRow.appendChild(th);

                        thead.appendChild(headerRow);
                        table.appendChild(thead);

                        // Add the tbody to the table
                        const tbody = document.createElement('tbody');
                        table.appendChild(tbody);

                        repasTablesContainer.appendChild(table);

                        // Store the tbody to add rows later
                        currentTables[repasType] = tbody;
                    }

                    // Add the row to the corresponding table
                    const tbody = currentTables[repasType];
                    const row = document.createElement('tr');
                    const cellAliment = document.createElement('td');
                    cellAliment.style.width = '50%';
                    const cellQuantite = document.createElement('td');
                    cellQuantite.style.width = '25%';
                    const cellOptions = document.createElement('td');
                    cellOptions.style.width = '25%';

                    cellAliment.textContent = aliment.aliment;
                    cellQuantite.textContent = aliment.quantite;

                    // Create a select element
                    const select = document.createElement('select');
                    select.className = 'form-control';
                    select.id = 'select' + aliment.id;
                    select.name = 'select' + aliment.id;
                    select.required = true;

                    // Add the options
                    aliment.suggestions.forEach(suggestion => {
                        const option = document.createElement('option');
                        option.value = suggestion[0];
                        option.textContent = suggestion[0];
                        select.appendChild(option);
                    });

                    // Add the options
                    cellOptions.appendChild(select);

                    row.appendChild(cellAliment);
                    row.appendChild(cellQuantite);
                    row.appendChild(cellOptions);
                    tbody.appendChild(row);
                });

                // Open the modal window
                const modalImport = new bootstrap.Modal(document.getElementById('modalImport'));
                modalImport.show();
            } else {
                alert('Erreur lors de l\'importation du fichier CSV');
                console.log('Error importing the diet while converting the CSV file');
                window.location.reload();
            }
        })
        .catch(error => {
            alert('Erreur lors de l\'importation du fichier CSV' + error);
            window.location.reload();
        });
}

function load_import_diet() {
    const dietTitle = filename.split('.').slice(0, -1).join('.'); // Remove the file extension
    const aliments = [];
    document.querySelectorAll('#aliments-non-trouves tr').forEach(row => {
        // si ligne 1 (titre du repas) on passe
        if (row.cells.length === 1) {
            return;
        }

        // Get the quantity
        const quantite = row.cells[1].textContent;
        // Get the selected suggestion
        const select = row.cells[2].querySelector('select');
        const suggestion = select.options[select.selectedIndex].value;
        // Get the meal number
        const repas = row.closest('table').querySelector('th').textContent;
        const repas_number = Object.keys(repasLabels).find(key => repasLabels[key] === repas);

        aliments.push({
            quantite,
            suggestion,
            repas_number,
        });
    });

    fetch('/store_diet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({diet_title: dietTitle, aliments})
    })
        .then(response => response.json())
        .then(() => {
            window.location.reload();
        })
}

// -------------------- END import diet section ----------------------------------

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function ajouterQuantite(alimentId, idDiete) {
    var str_repas = "";

    var quantiteInput = document.getElementById("quantite" + alimentId);
    var quantite = quantiteInput.value;

    if (quantite == "") {
        alert("Veuillez entrer une quantité.");
        return;
    }

    const matin = document.getElementById('matinCheckbox' + alimentId);
    const col_matin = document.getElementById('col_matinCheckbox' + alimentId);
    const midi = document.getElementById('midiCheckbox' + alimentId);
    const col_aprem = document.getElementById('col_apremCheckbox' + alimentId);
    const soir = document.getElementById('soirCheckbox' + alimentId);
    const col_soir = document.getElementById('col_soirCheckbox' + alimentId);

    if (matin.checked) {
        str_repas += matin.value;
    }
    if (col_matin.checked) {
        str_repas += col_matin.value;
    }
    if (midi.checked) {
        str_repas += midi.value;
    }
    if (col_aprem.checked) {
        str_repas += col_aprem.value;
    }
    if (soir.checked) {
        str_repas += soir.value;
    }
    if (col_soir.checked) {
        str_repas += col_soir.value;
    }

    if (!matin.checked && !col_matin.checked && !midi.checked && !col_aprem.checked && !soir.checked && !col_soir.checked) {
        alert("Veuillez sélectionner au moins un repas.");
        return;
    }

    ajouterQuantiteDiete(alimentId, idDiete, quantite, str_repas);
}

function ajouterQuantiteDiete(alimentId, idDiete, quantite, str_repas) {
    var url = "http://127.0.0.1:5000/ajouter_aliment_diete/" + alimentId + "/" + idDiete + "/" + quantite + "/" + str_repas;

    $.ajax({
        url: url,
        type: "GET",
        success: function (response) {
            window.location.reload();
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function checkFileSelected() {
    var fileInput = document.getElementById('fichier_csv');
    var button = document.getElementById('bouton_importer');
    if (fileInput.files.length > 0) {
        button.disabled = false;
    }
}

function changeTitle(id) {
    var titleInput = document.getElementById("titleInput");
    var title = titleInput.value;
    var url = "http://127.0.0.1:5000/change_title/" + id + "/" + title;

    $.ajax({
        url: url,
        type: "GET",
        success: function (response) {
            window.location.reload();
        },
        error: function (error) {
            console.log(error);
        }
    });
}

var delayTimer; // Timer pour retarder l'envoi de la requête AJAX

var currentPage = 1;
var pageSize = 3; // Nombre d'éléments par page

function updateData() {
    var filterValue = $('#filterInput').val();
    var selected_category = "";

    const categoryFilterSelect = document.getElementById('filterSelect');
    categoryFilterSelect.addEventListener('change', function () {
        fetchData();
    });

    // Function to fetch the data using AJAX
    function fetchData() {

        filterValue = document.getElementById('filterInput').value;
        selected_category = categoryFilterSelect.value;

        $.ajax({
            url: '/get_filtered_data',
            type: 'POST',
            data: {
                filter: filterValue,
                selected_category: selected_category,
                page: currentPage,
                page_size: pageSize
            },
            success: function (response) {
                var dataContainer = $('#dataContainer');
                dataContainer.empty();

                if (response.data.length === 0) {
                    dataContainer.append('<tr><td colspan="4" class="text-center">Aucun aliment trouvé.</td></tr>');
                    updatePagination(1);
                    return;
                }

                response.data.forEach(function (item) {
                    dataContainer.append('<tr class="element_aliment"><td style="width: 70%;">'
                        + item.titre + '</td><td style="width: 30%;">'
                        + item.kcal + ' kcal</td><td><button class="btn btn-sm btn-primary" data-toggle="tooltip" title="Ajouter" data-bs-toggle="modal" data-bs-target="#modal'
                        + item.id + '"><i class="fa fa-plus"></i></button>'
                        + fenetre_modale(item) + '</td></tr>');
                });

                // Mise à jour de la pagination
                updatePagination(response.total_pages);
            },
            error: function () {
                alert('Erreur lors du chargement des données filtrées.');
            }
        });
    }

    // Initial fetch of data on page load
    fetchData();
}

$(document).ready(function () {
    $('#filterInput').on('keyup', function () {
        clearTimeout(delayTimer);
        delayTimer = setTimeout(updateData, 500);
    });

    // Charger les données initiales (page 1)
    updateData();
    // Charger le graphique
    update_chart_intake();
});

function fenetre_modale(item) {
    return `<div class="modal fade" id="modal${item.id}" tabindex="-1" aria-labelledby="modal${item.id}Label" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="modal${item.id}Label">Ajouter la quantité</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="input-group">
                    <input type="number" id="quantite${item.id}" class="form-control" min="1" required placeholder="Quantité">
                    
                    <div class="input-group-prepend">
                      <div class="input-group-text" id="btnGroupAddon2">` + unite_to_string(item.unite) + item.titre + `</div>
                    </div>

                  </div>
                  <div class="row">
                    <div class="col-md-4">
                      <div class="form-check text-left mt-2">
                        <input type="checkbox" class="form-check-input" id="matinCheckbox${item.id}" name="matinCheckbox${item.id}" value="1">
                        <label class="form-check-label" for="matinCheckbox${item.id}">Matin</label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check text-left mt-2">
                        <input type="checkbox" class="form-check-input" id="col_matinCheckbox${item.id}" name="col_matinCheckbox${item.id}" value="2">
                        <label class="form-check-label" for="col_matinCheckbox${item.id}">Col. Matin</label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check text-left mt-2">
                        <input type="checkbox" class="form-check-input" id="midiCheckbox${item.id}" name="midiCheckbox${item.id}" value="3">
                        <label class="form-check-label" for="midiCheckbox${item.id}">Midi</label>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-4">
                      <div class="form-check text-left">
                        <input type="checkbox" class="form-check-input" id="col_apremCheckbox${item.id}" name="col_apremCheckbox${item.id}" value="4">
                        <label class="form-check-label" for="col_apremCheckbox${item.id}">Après-midi</label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check text-left">
                        <input type="checkbox" class="form-check-input" id="soirCheckbox${item.id}" name="soirCheckbox${item.id}" value="5">
                        <label class="form-check-label" for="soirCheckbox${item.id}">Soir</label>
                      </div>
                    </div>
                    <div class="col-md-4 text-left">
                      <div class="form-check text-left">
                        <input type="checkbox" class="form-check-input" id="col_soirCheckbox${item.id}" name="col_soirCheckbox${item.id}" value="6">
                        <label class="form-check-label" for="col_soirCheckbox${item.id}">Col. Soir</label>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                  <button type="button" class="btn btn-primary" onclick="ajouterQuantite(${item.id}, ${dieteId})">Ajouter</button>
                </div>
              </div>
            </div>
          </div>`;
}

/*
function fenetre_modale(item){
  return `<div class="modal fade" id="modal${item.id}" tabindex="-1" aria-labelledby="modal${item.id}Label" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="modal${item.id}Label">Ajouter la quantité</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="input-group">
                    <input type="number" id="quantite${item.id}" class="form-control" min="1" required placeholder="Quantité">
                    
                    <div class="input-group-prepend">
                      <div class="input-group-text" id="btnGroupAddon2">`+ unite_to_string(item.unite) + item.titre +`</div>
                    </div>
                  </div>
                  <div id="list1" class="dropdown-check-list" tabindex="100">
                      <span class="anchor">Repas</span>
                      <ul class="items">
                        <li><input type="checkbox" />Matin</li>
                        <li><input type="checkbox" />Collation Matin</li>
                        <li><input type="checkbox" />Midi</li>
                        <li><input type="checkbox" />Collation Après-midi</li>
                        <li><input type="checkbox" />Soir</li>
                        <li><input type="checkbox" />Collation Soir</li>
                      </ul>
                  </div>
                <script>
                var checkList = document.getElementById('list1');
                checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
                  if (checkList.classList.contains('visible'))
                    checkList.classList.remove('visible');
                  else
                    checkList.classList.add('visible');
                };
                </script>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                  <button type="button" class="btn btn-primary" onclick="ajouterQuantite(${item.id}, ${dieteId})">Ajouter</button>
                </div>
              </div>
            </div>
          </div>`;
}
*/
function unite_to_string(unite) {
    if (unite == 0) {
        return "g ";
    } else if (unite == 1) {
        return "";
    } else {
        return "mL ";
    }
}