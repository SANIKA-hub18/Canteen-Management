document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('monthlyChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Aug 1', 'Aug 2', 'Aug 3', 'Aug 4', 'Aug 5'],
      datasets: [
        {
          label: 'Tea',
          data: [15, 20, 25, 18, 25],
          borderColor: 'blue',
          fill: false,
        },
        {
          label: 'Snacks',
          data: [20, 25, 35, 30, 42],
          borderColor: 'green',
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Monthly Consumption Pattern' }
      }
    }
  });
});
