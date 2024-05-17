// google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(drawChart);
// google.charts.setOnLoadCallback(drawChart2);



// function drawChart() {

//     var data = google.visualization.arrayToDataTable([
//       ['Task', 'Hours per Day'],
//       ['python',     11],
//       ['html/css',      20],
//       ['boostrap',  17],
//       ['javascript', 15],
//       ['django',    7]
//     ]);

//     var options = {
//       title: 'SKILLS'
//     };

//     var chart = new google.visualization.PieChart(document.getElementById('piechart'));

//     chart.draw(data, options);
//   }



//   google.charts.load('current', {'packages':['corechart']});
//   google.charts.setOnLoadCallback(drawChart);

//   function drawChart2() {
//     var data = google.visualization.arrayToDataTable([
//       ['Year', 'Sales', 'Expenses'],
//       ['2013',  1000,      400],
//       ['2014',  1170,      460],
//       ['2015',  660,       1120],
//       ['2016',  1030,      540]
//     ]);

//     var options = {
//       title: 'Company Performance',
//       hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}},
//       vAxis: {minValue: 0}
//     };

//     var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
//     chart.draw(data, options);
//   }


document.getElementById('from-date').addEventListener('change', updateValues);
document.getElementById('to-date').addEventListener('change', updateValues);

function updateValues() {
    var fromDate = document.getElementById('from-date').value;
    var toDate = document.getElementById('to-date').value;

    if (fromDate.trim() !== '' && toDate.trim() !== '') {
        fetch(`/statics/?from_date=${fromDate}&to_date=${toDate}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-purchases').value = data.total_amount;
                document.getElementById('total-paid-amount').value = data.payment_amount;
                document.getElementById('remaining-pay').value = data.balance_amount;

                // Update pie chart
                if (data.pie_chart_data) {
                    document.getElementById('pie-chart-container').innerHTML = '<img src="data:image/png;base64,' + data.pie_chart_data + '" alt="Pie Chart">';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}