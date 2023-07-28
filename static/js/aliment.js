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

    console.log("fetchData()");
    
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

        dataContainer.append(`<tr class="text-center">
                <th>Titre</th>
                <th>Kcal</th>
                <th>Protéines</th>
                <th>Glucides</th>
                <th>Lipides</th>
                <th>Catégorie</th>
                <th>Unité</th>
                <th>Valide</th>
                <th>Modifier</th>
                <th>Supprimer</th>
            </tr>`);

        response.data.forEach(function(item) {
          dataContainer.append(`
            <tr class="element_aliment_liste">
                <td style="width: 20%">${item.titre}</td>
                <td style="width: 10%">${item.kcal}</td>
                <td style="width: 10%">${item.proteines} g</td>
                <td style="width: 10%">${item.glucides} g</td>
                <td style="width: 10%">${item.lipides} g</td>
                <td style="width: 10%">${item.categorie}</td>
                <td style="width: 10%">pour 100g</td>
                <td style="width: 10%">${aliment_valide(item)}</td>
                <td style="width: 10%">
                    <a href="/modifier_aliment/${item.id}" class="btn btn-sm btn-primary">➜</a>
                </td>
                <td style="width: 10%">
                    <a href="/supprimer_aliment/${item.id}" class="btn btn-sm btn-outline-danger">X</a>
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
        return `<button onclick="invalider_aliment(${item.id})" class="btn btn-sm btn-outline-danger red_dot"></button>`
    }
    else{
        return `<button onclick="valider_aliment(${item.id})" class="btn btn-sm btn-outline-success green_dot"></button>`
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