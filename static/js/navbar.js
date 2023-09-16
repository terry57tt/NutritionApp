const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;

darkModeToggle.addEventListener('click', () => {
    const dark = document.getElementById('theme_sheet_dark');
    dark.disabled = !dark.disabled;
});