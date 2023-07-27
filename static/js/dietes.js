function search_food(){
  let input = document.getElementById('searchbar').value
  input=input.toLowerCase();
  let x = document.getElementsByClassName('element_aliment');
      
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="table-row";                 
        }
    }
}

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

  $.ajax({
      url: '/get_filtered_data',
      type: 'POST',
      data: { filter: filterValue, page: currentPage, page_size: pageSize },
      success: function(response) {
          var dataContainer = $('#dataContainer');
          dataContainer.empty();

          // Afficher les éléments de la page actuelle
          response.data.forEach(function(item) {
              dataContainer.append('<p>' + item.titre + '</p>');
          });

          // Mise à jour de la pagination
          updatePagination(response.total_pages);
      },
      error: function() {
          alert('Erreur lors du chargement des données filtrées.');
      }
  });
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