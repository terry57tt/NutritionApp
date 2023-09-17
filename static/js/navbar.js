const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;
const dark = document.getElementById('theme_sheet_dark');

// Fonction pour activer le mode sombre
function enableDarkMode() {
    body.classList.add('dark-mode');
    dark.disabled = false;
    darkModeToggle.classList.remove('fa-moon-o');
    darkModeToggle.classList.add('fa-sun-o');
}

// Fonction pour désactiver le mode sombre
function disableDarkMode() {
    body.classList.remove('dark-mode');
    dark.disabled = true;
    darkModeToggle.classList.remove('fa-sun-o');
    darkModeToggle.classList.add('fa-moon-o');
}

// Fonction pour basculer le mode sombre
function toggleDarkMode() {
    if (body.classList.contains('dark-mode')) {
        disableDarkMode();
        localStorage.setItem('darkMode', 'false');
    } else {
        enableDarkMode();
        localStorage.setItem('darkMode', 'true');
    }
}

// Écouteur d'événements pour le bouton de bascule du mode sombre
darkModeToggle.addEventListener('click', toggleDarkMode);

// Vérifie l'état du mode sombre dans le stockage local lors du chargement de la page
window.addEventListener('load', () => {
    const isDarkModeEnabled = localStorage.getItem('darkMode');
    if (isDarkModeEnabled === 'true') {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
});
