const categories = [
    { value: 'autre', label: 'Autre' },
    { value: 'boisson', label: 'Boisson' },
    { value: 'féculent', label: 'Féculent' },
    { value: 'fruit', label: 'Fruit' },
    { value: 'légume', label: 'Légume' },
    { value: 'légumineuse', label: 'Légumineuse' },
    { value: 'matière grasse', label: 'Matière grasse' },
    { value: 'produit laitier', label: 'Produit laitier' },
    { value: 'poisson', label: 'Poisson' },
    { value: 'viande', label: 'Viande' },
    { value: 'sucrerie', label: 'Sucrerie' },
    { value: '', label: 'Tous les aliments' },
  ];
  
window.addEventListener('DOMContentLoaded', function(){
    var f = document.getElementById('search-form');
  
    var filtre_select = document.getElementById('filterSelect');
  
    while(categories.length)
    {
        var categorie = categories.pop();
        var opt = new Option(categorie.label, categorie.value);
        filtre_select.options[filtre_select.options.length] = opt;
    }
    f.appendChild(filtre_select);
});