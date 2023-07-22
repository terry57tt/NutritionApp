function search_aliment(){
    let input = document.getElementById('searchbar_aliment').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('element_aliment_liste');
        
      for (i = 0; i < x.length; i++) { 
          if (!x[i].innerHTML.toLowerCase().includes(input)) {
              x[i].style.display="none";
          }
          else {
              x[i].style.display="table-row";                 
          }
      }
}

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