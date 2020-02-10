$(function () {
  var $populationChart = $("#price-chart");
  $.ajax({
    url: $populationChart.data("url"),
    success: function (data) {

      var ctx = $populationChart[0].getContext("2d");

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Price',
            backgroundColor: '#cadb2a',
            data: data.data
          }]          
        },
        options: {
          responsive: true,
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Price Bar Chart'
          }
        }
      });
    }
  });
});



$(function () {
  var $populationChart = $("#review-chart");
  $.ajax({
    url: $populationChart.data("url"),
    success: function (data) {

      var ctx = $populationChart[0].getContext("2d");

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Review Todal',
            backgroundColor: '#cadb2a',
            data: data.data
          }]          
        },
        options: {
          responsive: true,
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Price Bar Chart'
          }
        }
      });
    }
  });
});