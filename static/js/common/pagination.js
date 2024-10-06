function updatePagination(totalPages) {
    var pagination = $('#pagination');
    pagination.empty();

    var maxDisplayedPages = 3;  // Nombre maximum de boutons de pages affichés
    var startPage, endPage;

    if (totalPages <= maxDisplayedPages) {
        startPage = 1;
        endPage = totalPages;
    } else {
        startPage = Math.max(1, currentPage - Math.floor(maxDisplayedPages / 2));
        endPage = Math.min(totalPages, startPage + maxDisplayedPages - 1);

        if (endPage - startPage < maxDisplayedPages - 1) {
            startPage = Math.max(1, endPage - maxDisplayedPages + 1);
        }
    }

    // Créer le lien pour la page précédente
    pagination.append('<li class="page-item"><a class="page-link" href="#" onclick="goToPage(' + (currentPage - 1) + ')" id="prevPageLink">&laquo;</a></li>');

    if (startPage > 1) {
        pagination.append('<li class="page-item"><a class="page-link" href="#" onclick="goToPage(1)">1</a></li>');
        if (startPage > 2) {
            pagination.append('<li class="page-item disabled"><a class="page-link" href="#">...</a></li>');
        }
    }

    for (var i = startPage; i <= endPage; i++) {
        pagination.append('<li class="page-item' + (i === currentPage ? ' active' : '') + '"><a class="page-link" href="#" onclick="goToPage(' + i + ')">' + i + '</a></li>');
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            pagination.append('<li class="page-item disabled"><a class="page-link" href="#">...</a></li>');
        }
        pagination.append('<li class="page-item"><a class="page-link" href="#" onclick="goToPage(' + totalPages + ')">' + totalPages + '</a></li>');
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