$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

selected_activity = 1.55;
selected_diet_type = 1;

// métabolisme de base en fonction des infos de l'utilisateur
const totalMB_HB = document.getElementById("totalMB_HB");
const totalMB_BA = document.getElementById("totalMB_BA");
const totalMB_OX = document.getElementById("totalMB_OX");
const totalMB_SC = document.getElementById("totalMB_SC");

const caloriesMB_HB = totalMB_HB.textContent;
const caloriesMB_BA = totalMB_BA.textContent;
const caloriesMB_OX = totalMB_OX.textContent;
const caloriesMB_SC = totalMB_SC.textContent;

// affichage MB x activité
const caloriesLabel_HB = document.getElementById("caloriesLabel_HB");
const caloriesLabel_BA = document.getElementById("caloriesLabel_BA");
const caloriesLabel_OX = document.getElementById("caloriesLabel_OX");
const caloriesLabel_SC = document.getElementById("caloriesLabel_SC");

// activité physique
const rangeInput = document.getElementById("customRange");
const activityLabel = document.getElementById("activityLabel");

// type de diète Sèche/Maintien/Prise de masse
const rangeInputType = document.getElementById("customRangeType");
const activityLabelType = document.getElementById("activityLabelType");
var info_activity = document.getElementById('info_activity')


rangeInput.addEventListener("input", function() {
    const activityLevel = parseInt(rangeInput.value);

    switch (activityLevel) {
        case 0:
            activityLabel.textContent = "Sédentaire · 1,2";
            selected_activity = 1.2;
            break;
        case 1:
            activityLabel.textContent = "Légèrement actif · 1,375";
            selected_activity = 1.375;
            break;
        case 2:
            activityLabel.textContent = "Actif · 1,55";
            selected_activity = 1.55;
            break;
        case 3:
            activityLabel.textContent = "Très actif · 1,725";
            selected_activity = 1.725;
            break;
        case 4:
            activityLabel.textContent = "Extrêmement actif · 1,9";
            selected_activity = 1.9;
            break;
        default:
            activityLabel.textContent = "";
    }

    changeTooltip(activityLevel);
    changeCalories();
});

function changeTooltip(activityLevel) {
  switch (activityLevel) {
    case 0:
      var tooltip = new bootstrap.Tooltip(info_activity, {
        placement: 'right',
        title: "Aucun exercice quotidien ou presque"
      })
      break;
    case 1:
      var tooltip = new bootstrap.Tooltip(info_activity, {
        placement: 'right',
        title: "Vous faites parfois des exercices physiques (1 à 3 fois par semaine)"
      })
      break;
    case 2:
      var tooltip = new bootstrap.Tooltip(info_activity, {
        placement: 'right',
        title: "Vous faites régulièrement des exercices physiques (3 à 5 fois par semaine)"
      })
      break;
    case 3:
      var tooltip = new bootstrap.Tooltip(info_activity, {
        placement: 'right',
        title: "Vous faites quotidiennement du sport ou des exercices physiques soutenus"
      })
      break;
    case 4:
      var tooltip = new bootstrap.Tooltip(info_activity, {
        placement: 'right',
        title: "Votre travail est extrêmement physique ou grand sportif"
      })
      break;
    default:
      var tooltip = new bootstrap.Tooltip(info_activity, {
        placement: 'right',
        title: ""
      })
    }
}

rangeInputType.addEventListener("input", function() {
    const dietType = parseInt(rangeInputType.value);

    switch (dietType) {
        case 0:
          activityLabelType.textContent = "Sèche · 0,8";
          selected_diet_type = 0.8;
            break;
        case 1:
          activityLabelType.textContent = "Maintien · 1";
          selected_diet_type = 1;
            break;
        case 2:
          activityLabelType.textContent = "Prise de masse · 1,2";
          selected_diet_type = 1.2;
            break;
        default:
          activityLabelType.textContent = "";
    }

    changeCalories();
});

function changeCalories() {
    caloriesLabel_HB.textContent = Math.round(caloriesMB_HB * selected_activity * selected_diet_type);
    caloriesLabel_BA.textContent = Math.round(caloriesMB_BA * selected_activity * selected_diet_type);
    caloriesLabel_OX.textContent = Math.round(caloriesMB_OX * selected_activity * selected_diet_type);
    caloriesLabel_SC.textContent = Math.round(caloriesMB_SC * selected_activity * selected_diet_type);
}

const data = {
    labels: ['Protéines', 'Lipides', 'Glucides'],
    datasets: [{
      label: 'Macronutriments',
      data: [pourcentage_proteines,pourcentage_lipides,pourcentage_glucides],
      backgroundColor: [
          '#fff4de',
          '#e8f4ff',
          '#ffe8e8',
        ],
      hoverOffset: 20,
      borderWidth: 5,
      borderRadius: 10,
      bordereAlign: 'inner',
      
    }]
  };

  // Configuration du graphique
  const config = {
    type: 'doughnut',
    data: data,
      options: {
          plugins: {
          legend: {
              position: 'bottom',
          },
          }
      },
  };

  const circle_chart = new Chart(document.getElementById('macro_chart'), config);

  const data_radar = {
      labels: [
          'Matin',
          'Collation matin',
          'Midi',
          'Collation après-midi',
          'Soir',
          'Collation soir'
      ],
      datasets: [{
        label: 'Expected',
        data: [65, 59, 90, 81, 56, 55],
        fill: true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        pointBackgroundColor: 'rgb(255, 99, 132)',
      }, {
        label: 'Realised',
        data: [28, 48, 40, 19, 96, 100],
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        pointBackgroundColor: 'rgb(54, 162, 235)',
      }]
    };

    const config_radar = {
      type: 'radar',
      data: data_radar,
      options: {
        elements: {
          line: {
            borderWidth: 3
          }
        },
        plugins: {
          legend: {
            position: 'bottom',
          },
        }
      },
    };

    // Création du graphique Radar
    const radar_chart = new Chart(document.getElementById('objectifs_chart'), config_radar);      
          
    const data_histo = {
      labels: ['Sèche', 'Maintien', 'Prise de masse'],
      datasets: [{
          label: 'Objectifs',
          data: [calories-500, calories, calories+500],
          backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(255, 205, 86, 0.2)',
          ],
          borderColor: [
          'rgb(255, 99, 132)',
          'rgb(255, 159, 64)',
          'rgb(255, 205, 86)',
          ],
          borderWidth: 1
          
      }]
  };

  const config_histo = {
      type: 'bar',
      data: data_histo,
      options: {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 500,
                },
            },
            x: {
                display: true,
            },
          },
        plugins: {
            legend: {
                display: false,
                beginAtZero: true,
            }
        }
    },
  };

  // Création du graphique Histogramme
  const histo_chart = new Chart(document.getElementById('evolution_chart'), config_histo);