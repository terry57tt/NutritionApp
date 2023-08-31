$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function checkFileSelectedAliment() {
    var fileInput = document.getElementById('fichier_aliment');
    var button = document.getElementById('bouton_importer_aliment');
    if (fileInput.files.length > 0) {
        button.disabled = false;
    }
    else {
        button.disabled = true;
    }
}

var delayTimer; // Timer pour retarder l'envoi de la requête AJAX

var currentPage = 1;
var pageSize = 5; // Nombre d'éléments par page

function updateData() {
  var filterValue = $('#filterInput').val();
  var selected_category = "";

  const categoryFilterSelect = document.getElementById('filterSelect');
  categoryFilterSelect.addEventListener('change', function() {
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
      success: function(response) {
        var dataContainer = $('#dataContainer');
        dataContainer.empty();
        
        if(response.data.length === 0) {
          dataContainer.append('<tr><td colspan="9" class="text-center">Aucun aliment trouvé.</td></tr>');
          updatePagination(1);
          return;
        }

        dataContainer.append(`<tr class="text-center">
                <th class="colonne_table_20 primary">Titre</th>
                <th class="colonne_table_10 secondary">Kcal</th>
                <th class="colonne_table_10 third">Protéines</th>
                <th class="colonne_table_10 third">Glucides</th>
                <th class="colonne_table_10 third">Lipides</th>
                <th class="colonne_table_10 secondary">Catégorie</th>
                <th class="colonne_table_10 third">Unité</th>
                <th class="colonne_table_10 secondary">Valide</th>
                <th class="colonne_table_10 primary">Action</th>
            </tr>`);

        response.data.forEach(function(item) {
          dataContainer.append(`
            <tr>
                <td class="colonne_table_20 primary">${item.titre}</td>
                <td class="colonne_table_10 secondary">${item.kcal}</td>
                <td class="colonne_table_10 third">${item.proteines} g</td>
                <td class="colonne_table_10 third">${item.glucides} g</td>
                <td class="colonne_table_10 third">${item.lipides} g</td>
                <td class="colonne_table_10 secondary">${item.categorie}</td>
                <td class="colonne_table_10 third">${mesure_aliment(item.unite)}</td>
                <td class="colonne_table_10 secondary">${aliment_valide(item)}</td>
                <td class="colonne_table_10 primary">
                  <div class="container">
                    <div class="row text-center">
                      <div class="col-md-6 mb-1">
                        <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#modal_modifier${item.id}"><i class="fa fa-pencil"></i></button>${modal_modifier_aliment(item)}
                      </div>
                      <div class="col-md-6">
                        <button class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#modal${item.id}"><i class="fa fa-trash"></i></button>${modal_confirmtion_suppression_aliment(item)}
                      </div>
                    </div>
                  </div>      
                </td>
            </tr>
          `);
        });

        // Mise à jour de la pagination
        updatePagination(response.total_pages);
      },
      error: function() {
        alert('Erreur lors du chargement des données filtrées.');
      }
    });
  }

  // Initial fetch of data on page load
  fetchData();
}


function updatePagination(totalPages) {
  var pagination = $('#pagination');
  pagination.empty();

  // Créer le lien pour la page précédente
  pagination.append('<li class="page-item"><a class="page-link" href="#" onclick="goToPage(' + (currentPage - 1) + ')" id="prevPageLink">&laquo;</a></li>');

  // Créer les liens pour chaque page
  for (var i = 1; i <= totalPages; i++) {
      pagination.append('<li class="page-item"><a class="page-link" href="#" onclick="goToPage(' + i + ')">' + i + '</a></li>');
  }

  // Créer le lien pour la page suivante
  pagination.append('<li class="page-item"><a class="page-link" href="#" onclick="goToPage(' + (currentPage + 1) + ')" id="nextPageLink">&raquo;</a></li>');

  // Désactiver le lien de la page précédente si on est à la première page
  if (currentPage === 1) {
      $('#prevPageLink').addClass('disabled');
  } else {
      $('#prevPageLink').removeClass('disabled');
  }

  // Désactiver le lien de la page suivante si on est à la dernière page
  if (currentPage === totalPages) {
      $('#nextPageLink').addClass('disabled');
  } else {
      $('#nextPageLink').removeClass('disabled');
  }
}

function goToPage(pageNumber) {
  currentPage = pageNumber;
  updateData();
}

$(document).ready(function() {
  $('#filterInput').on('keyup', function() {
      clearTimeout(delayTimer);
      delayTimer = setTimeout(updateData, 500);
  });

  // Charger les données initiales (page 1)
  updateData();
});

function aliment_valide(item){
    if(item.valide){
        return `<button onclick="invalider_aliment(${item.id})" data-toggle="tooltip" title="Aliment invalide" class="btn btn-sm btn-danger"><i class="fa fa-close"></i></button>`
    }
    else{
        return `<button onclick="valider_aliment(${item.id})" data-toggle="tooltip" title="Aliment valide" class="btn btn-sm btn-success"><i class="fa fa-check"></i></button>`
    }
};

function invalider_aliment(id){
    $.ajax({
        url: '/invalider_aliment/'+id,
        type: 'POST',
        success: function(response) {
            updateData();
        },
        error: function() {
            alert('Erreur lors de la validation de l\'aliment.');
        }
    });
}

function valider_aliment(id){
    $.ajax({
        url: '/valider_aliment/'+id,
        type: 'POST',
        success: function(response) {
            updateData();
        },
        error: function() {
            alert('Erreur lors de la validation de l\'aliment.');
        }
    });
}

function supprimer_aliment(id){
    $.ajax({
        url: '/supprimer_aliment/'+id,
        type: 'POST',
        success: function(response) {
          updateData();
        },
        error: function() {
            alert('Erreur lors de la suppression de l\'aliment.');
        }
    });
}

function modal_confirmtion_suppression_aliment(item){
  return `<div class="modal fade" id="modal${item.id}" tabindex="-1" aria-labelledby="modal${item.id}Label" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="modal${item.id}Label">Supprimer l'aliment « ${item.titre} » ?</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
            <div class="modal-body">
              <p>L'aliment sera supprimé définitivement de toutes les diètes.</p>
            </div>
            <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                  <button type="button" class="btn btn-warning" data-bs-dismiss="modal" onclick="supprimer_aliment(${item.id})">Supprimer</button>
                </div>
              </div>
            </div>
          </div>`;
}

function modal_modifier_aliment(aliment, test="autre"){
    return `
      <div class="modal fade" id="modal_modifier${aliment.id}" tabindex="-1" aria-labelledby="modal_modifier${aliment.id}Label" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="modal_modifier${aliment.id}Label">Modifier l'aliment</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
        <form method="POST" action="/modifier_aliment_post/${aliment.id}"  enctype="multipart/form-data">
            <div class="modal-body">
                    <div class="container">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <div class="input-group">
                          <span class="input-group-text">Titre</span>
                          <input id="titre" name="titre" class="form-control" type="text" value="${aliment.titre}" required/>
                        </div>
                      </div>
                      <div class="col-md-6 mb-3">
                        <div class="input-group">
                          <input id="kcal" name="kcal" class="form-control" type="number" value="${aliment.kcal}" required/>
                          <span class="input-group-text">Kcal</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="container">
                    <div class="row">
                      <div class="col-md-4">
                        <div class="input-group mb-3">
                          <span class="input-group-text">Protéines</span>
                          <input id="proteines" name="proteines" class="form-control" type="number" value="${aliment.proteines}" required/>
                        </div>
                      </div>
                      <div class="col-md-4">
                        <div class="input-group mb-3">
                          <span class="input-group-text">Glucides</span>
                          <input id="glucides" name="glucides" class="form-control" type="number" value="${aliment.glucides}" required/>
                        </div>
                      </div>
                      <div class="col-md-4 mb-3">
                        <div class="input-group">
                          <span class="input-group-text">Lipides</span>
                          <input id="lipides" name="lipides" class="form-control" type="number" value="${aliment.lipides}" required/>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="container">
                    <div class="row">
                      <div class="col-md-4 mb-3">
                          <select id="categorie" name="categorie" class="form-control" required>
                            <option value="autre" ${selected_category(aliment.categorie,"autre")}>Autre</option>
                            <option value="boisson" ${selected_category(aliment.categorie,"boisson")}>Boisson</option>
                            <option value="féculent" ${selected_category(aliment.categorie,"féculent")}>Féculent</option>
                            <option value="fruit" ${selected_category(aliment.categorie,"fruit")}>Fruit</option>
                            <option value="légume" ${selected_category(aliment.categorie,"légume")}>Légume</option>
                            <option value="légumineuse" ${selected_category(aliment.categorie,"légumineuse")}>Légumineuse</option>
                            <option value="matière grasse" ${selected_category(aliment.categorie,"matière grasse")}>Matière grasse</option>
                            <option value="produit laitier" ${selected_category(aliment.categorie,"produit laitier")}>Produit laitier</option>
                            <option value="poisson" ${selected_category(aliment.categorie,"poisson")}>Poisson</option>
                            <option value="viande" ${selected_category(aliment.categorie,"viande")}>Viande</option>
                            <option value="sucrerie" ${selected_category(aliment.categorie,"sucrerie")}>Sucrerie</option>
                          </select>
                      </div>
                      <div class="col-md-8 mb-3">
                          <div class="input-group">
                              <input class="form-control" type="file" id="fichier_photo" name="fichier_photo">
                          </div>
                      </div>
                    </div>
                  </div>
                  <div class="container">
                    <div class="row">
                      <div class="col-md-5 mb-3">
                        <div class="input-group description">
                          <span class="input-group-text">Description</span>
                          <textarea id="description" name="description" class="form-control">${aliment.description}</textarea>
                        </div>
                      </div>
                      <div class="col-md-4 mb-3">
                        <img src="/static/upload/${aliment.photo}" height="80" width="80" onerror="this.src='/static/images/empty_photo.png';">
                      </div>
                      <div class="col-md-3 mb-3">
                          <div class="form-check">
                              <input class="form-check-input" value="0" type="radio" name="unite" id="flexRadioDefault1" value="100 g" ${checked_unity(aliment.unite,0)} required>
                              <label class="form-check-label" for="flexRadioDefault1">
                              100 g
                              </label>
                          </div>
                          <div class="form-check">
                              <input class="form-check-input" value="1" type="radio" name="unite" id="flexRadioDefault2" value="1 portion" ${checked_unity(aliment.unite,1)} required>
                              <label class="form-check-label" for="flexRadioDefault2">
                              1 portion
                              </label>
                          </div>
                          <div class="form-check">
                              <input class="form-check-input" value="2" type="radio" name="unite" id="flexRadioDefault3" value="100 mL" ${checked_unity(aliment.unite,2)} required>
                              <label class="form-check-label" for="flexRadioDefault3">
                              100 mL
                              </label>
                          </div>
                      </div>
                    </div>
                  </div>
            </div>
            <div class="modal-footer">
              <div class="container">
                    <div class="row">
                      <div class="container">
                        <div class="row">
                          <div class="text-center">
                            <button class="btn btn-secondary" data-bs-dismiss="modal" type="button">Annuler</button>
                            <button class="btn btn-primary" type="submit">Modifier</button>
                          </div>
                        </div>
                      </div>
                    </div>
                </div>
            </div>
            </form>
          </div>
        </div>
      </div>
    `;
  }

function selected_category(current, categorie){
  if(current == categorie){
    return "selected";
  }
  else{
    return "";
  }
}

function checked_unity(current, unity){
  if(current == unity){
    return "checked";
  }
  else{
    return "";
  }
}

function mesure_aliment(unite){
  if(unite == 0){
    return "100 g";
  }
  else if(unite == 1){
    return "1 portion";
  }
  else{
    return "100 mL";
  }
}