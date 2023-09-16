const tableau = document.getElementById('suivi_table');
  const labels = [];
  const poids = [];

  for (let i = 0; i < tableau.rows.length; i++) {
    const row = tableau.rows[i];
    date_value = row.cells[0].textContent;
    labels.push(date_value);
    poids.push(parseFloat(row.cells[1].textContent));
  }

  const ctx = document.getElementById('line_chart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Poids (kg)',
        data: poids,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        pointRadius: 5,
        pointHoverRadius: 10,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          stepSize: 1,
          suggestedMin: Math.min(...poids) - 5,
          suggestedMax: Math.max(...poids) + 5,
        }
      }
    }
  });
  