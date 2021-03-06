var config = {
  type: 'pie',
  data: {
    datasets: [{
      data: {{ review |review_date }},
      backgroundColor: [
        '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
      ],
      label: 'labels'
    }],
    labels: {{ review_date | review_rating }}
  },
  options: {
    responsive: true
  }
};

window.onload = function() {
  var ctx = document.getElementById('pie-chart').getContext('2d');
  window.myPie = new Chart(ctx, config);
};
