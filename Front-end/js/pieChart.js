google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['EQ', 'Condition'],
          ['OK',     80],
          ['Broken',      20],
          ['Unknown',      10]
        ]);

        var options = {
          title: '',
          backgroundColor: 'transparent',
          colors: ['#bada55', '#f73d28', '#c0c0c0']
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }