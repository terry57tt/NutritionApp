$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function ajouterQuantite(alimentId,idDiete) {
  var quantiteInput = document.getElementById("quantite" + alimentId);
  var quantite = quantiteInput.value;
  var repasInput = document.getElementById("repas" + alimentId);
  var repas = repasInput.value;
  
    var url = "http://127.0.0.1:5000/ajouter_aliment_diete/" + alimentId + "/" + idDiete + "/" + quantite + "/" + repas;
    
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
                  <label for="repas${item.id}"></label>
                  <select id="repas${item.id}" class="form-control" required>
                    <option value="1">Matin</option>
                    <option value="2">Collation Matin</option>
                    <option value="3">Midi</option>
                    <option value="4">Collation Après-midi</option>
                    <option value="5">Soir</option>
                    <option value="6">Collation Soir</option>
                  </select>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                  <button type="button" class="btn btn-primary" onclick="ajouterQuantite(${item.id}, ${dieteId})">Ajouter</button>
                </div>
              </div>
            </div>
          </div>`;
}

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