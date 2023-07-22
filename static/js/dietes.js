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