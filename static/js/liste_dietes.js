var delayTimer; // Timer pour retarder l'envoi de la requête AJAX
  
var currentPage = 1;
var pageSize = 5; // Nombre d'éléments par page

const tableElement = document.getElementById('table_dietes');
const mode = tableElement.dataset.mode;
const user = tableElement.dataset.user;
  
  function updateData() {
    var filterValue = $('#filterInput').val();

    function fetchData() {
      filterValue = document.getElementById('filterInput').value;

      $.ajax({
        url: '/get_filtered_data_dietes',
        type: 'POST',
        data: {
          filter: filterValue,
          page: currentPage,
          page_size: pageSize
        },
        success: function(response) {            
          var dataContainer = $('#dietesContainer');
          dataContainer.empty();
  
          if(response.data.length === 0) {
            dataContainer.append('<tr><td colspan="4" class="text-center">Aucune diète trouvée.</td></tr>');
            updatePagination(1);
            return;
          }

          dataContainer.append(`
            <tr class="text-center">
                <th class="colonne_table_30 primary">Titre</th>
                <th class="colonne_table_20 third">Créateur</th>
                <th class="colonne_table_20 third">Date</th>
                <th class="colonne_table_30 primary">Actions</th>
            </tr>
            `);

          // Afficher les éléments de la page actuelle
          response.data.forEach(function(item) {
            dataContainer.append(`
                <tr class="text-center">
                    <td class="colonne_table_30 primary">${item.titre_diete}</td>
                    <td class="colonne_table_20 third">${affichage_createur(item.createur)}</td>
                    <td class="colonne_table_20 third">${changeFormat(item.date)}</td>
                    <td class="colonne_table_30 primary">${affichage_buttons(item.id,item.titre_diete)}</td>
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

function changeFormat(date){
    var d = new Date(date);
    var month = d.getMonth()+1;
    var day = d.getDate();
    var year = d.getFullYear();
    var string_month = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novebre', 'Décembre'
    ]
    var date = day + " " + string_month[month] + " " + year;
    return date;
}

function affichage_createur(createur){
    return createur.prenom + " " + createur.nom;
}

function affichage_buttons(id,titre){
    if(mode == "voir"){
        return `<button onclick="voir_diete(${id})" class="btn btn-primary" data-toggle="tooltip" title="Voir"><i class="fa fa-eye"></i></button>
        <button onclick="modifier_diete(${id})" class="btn btn-primary" data-toggle="tooltip" title="Modifier"><i class="fa fa-pencil"></i></button>
        <button class="btn btn-danger" data-toggle="tooltip" title="Supprimer" data-bs-toggle="modal" data-bs-target="#modal${id}"><i class="fa fa-trash"></i></button>${modal_confirmtion_suppression_diete(id,titre)}`;
    } else if(mode == "changer"){
        return `<button onclick="voir_diete(${id})" class="btn btn-primary" data-toggle="tooltip" title="Voir" data-toggle="tooltip" title="Voir"><i class="fa fa-eye"></i></button>
        <button onclick="changer_diete(${id})" class="btn btn-primary" data-toggle="tooltip" title="Choisir" data-toggle="tooltip" title="Choisir"><i class="fa fa-hand-o-up"></i></button>`;
    }
}

function voir_diete(id){
    window.location.href = "/voir_diete/" + id;
}

function modifier_diete(id){
    window.location.href = "/modifier_diete/" + id;
}

function supprimer_diete(id){
    window.location.href = "/supprimer_diete/" + id;
}

function changer_diete(id){
    window.location.href = "/choisir_diete/" + id + "/" + user;
}

function modal_confirmtion_suppression_diete(id,titre){
  return `<div class="modal fade" id="modal${id}" tabindex="-1" aria-labelledby="modal${id}Label" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="modal${id}Label">Supprimer la diète « ${titre} » ?</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
            <div class="modal-body">
              <p>La diète sera suprrimée pour tous les utilisateurs.</p>
            </div>
            <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                  <button type="button" class="btn btn-warning" data-bs-dismiss="modal" onclick="supprimer_diete(${id})">Supprimer</button>
                </div>
              </div>
            </div>
          </div>`;
}