$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function ajouterQuantite(alimentId,idDiete) {
  var str_repas = "";

  var quantiteInput = document.getElementById("quantite" + alimentId);
  var quantite = quantiteInput.value;

  if(quantite == ""){
    alert("Veuillez entrer une quantité.");
    return;
  }

  const matin = document.getElementById('matinCheckbox' + alimentId);
  const col_matin = document.getElementById('col_matinCheckbox'+ alimentId);
  const midi = document.getElementById('midiCheckbox'+ alimentId);
  const col_aprem = document.getElementById('col_apremCheckbox'+ alimentId);
  const soir = document.getElementById('soirCheckbox'+ alimentId);
  const col_soir = document.getElementById('col_soirCheckbox'+ alimentId);

  if(matin.checked){
    str_repas += matin.value;
  }
  if(col_matin.checked){
    str_repas += col_matin.value;
  }
  if(midi.checked){
    str_repas += midi.value;
  }
  if(col_aprem.checked){
    str_repas += col_aprem.value;
  }
  if(soir.checked){
    str_repas += soir.value;
  }
  if(col_soir.checked){
    str_repas += col_soir.value;
  }

  if(!matin.checked && !col_matin.checked && !midi.checked && !col_aprem.checked && !soir.checked && !col_soir.checked){
    alert("Veuillez sélectionner au moins un repas.");
    return;
  }

  ajouterQuantiteDiete(alimentId,idDiete,quantite,str_repas);
}

function ajouterQuantiteDiete(alimentId,idDiete,quantite,str_repas) {
  var url = "http://127.0.0.1:5000/ajouter_aliment_diete/" + alimentId + "/" + idDiete + "/" + quantite + "/" + str_repas;
    
    $.ajax({
      url: url,
      type: "GET",
      success: function(response) {
        window.location.reload();
      },
      error: function(error) {
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
    success: function(response) {
      window.location.reload();
    },
    error: function(error) {
      console.log(error);
    }
  });
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
          dataContainer.append('<tr><td colspan="4" class="text-center">Aucun aliment trouvé.</td></tr>');
          updatePagination(1);
          return;
        }

        response.data.forEach(function(item) {
          dataContainer.append('<tr class="element_aliment"><td style="width: 40%;">' 
          + item.titre + '</td><td style="width: 30%;">'
          + item.kcal + ' kcal</td><td style="width: 30%;">'
          + item.proteines + ' g/p</td><td><button class="btn btn-sm btn-primary" data-toggle="tooltip" title="Ajouter" data-bs-toggle="modal" data-bs-target="#modal'
          + item.id + '"><i class="fa fa-plus"></i></button>'
          + fenetre_modale(item) + '</td></tr>');
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
function unite_to_string(unite){
  if(unite == 0){
    return "g ";
  }
  else if(unite == 1){
    return "";
  }
  else{
    return "mL ";
  }
}