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
            display: true
          }
        }
      });
    }
  });
});


// 그래프 2
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
            label: '상품별 리뷰수',
            backgroundColor: '#4e73df',
            data: data.data
          }]          
        },
        options: {
          responsive: true,
          legend: {
            position: 'top',
          },
          title: {
            display: true
          }
        }
      });
    }
  });
});


// 그래프 3
$(function () {
  var $populationChart = $("#chart3");
  $.ajax({
    url: $populationChart.data("url"),
    success: function (data) {
      var ctx = $populationChart[0].getContext("2d");

      data_list = []
      for(var i = 0; i < 10; i++) {
        obj = {}
        obj['x'] = data.labels[i]
        obj['y'] = data.data[i]
        data_list.push(obj)
      }
      console.log(data_list)

      new Chart(ctx, {
        type: 'scatter',
        data: {
          datasets: [{
              label: 'Scatter Dataset',
              backgroundColor: 'rgb(255, 99, 132)',
              data: [
                data_list
              ]
              // data: data_list
          }]
        },
        options: {
          scales: {
              xAxes: [{
                  type: 'linear',
                  position: 'bottom'
              }]
          }
      }

      });
    }
  });
});
