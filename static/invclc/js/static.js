google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
google.charts.setOnLoadCallback(drawChart2);



function drawChart() {

    var data = google.visualization.arrayToDataTable([
      ['Task', 'Hours per Day'],
      ['python',     11],
      ['html/css',      20],
      ['boostrap',  17],
      ['javascript', 15],
      ['django',    7]
    ]);

    var options = {
      title: 'SKILLS'
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
  }



  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart2() {
    var data = google.visualization.arrayToDataTable([
      ['Year', 'Sales', 'Expenses'],
      ['2013',  1000,      400],
      ['2014',  1170,      460],
      ['2015',  660,       1120],
      ['2016',  1030,      540]
    ]);

    var options = {
      title: 'Company Performance',
      hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}},
      vAxis: {minValue: 0}
    };

    var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }