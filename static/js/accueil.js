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