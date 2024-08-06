
// static.js

/////////////////////////////////////////////////////// DONUT_CHART ////////////////////////////////////////////////////////////


var total_amountss = parseFloat(document.getElementById("total-purchases").value);
var payment_amountss = parseFloat(document.getElementById("total-paid-amount").value);
var balance_amountss = parseFloat(document.getElementById("remaining-pay").value);

if (total_amountss === 0 && payment_amountss === 0 && balance_amountss === 0) {
    // If all values are zero, create a chart with zero values
    var ctx = document.getElementById('myDonutChart').getContext('2d');
    var myDonutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Total Purchases', 'Total Paid Amount', 'Remaining Pay'],
            datasets: [{
                data: [1, 1, 1],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1,
                offset: 30 // Explode effect value
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',
            borderRadius: 7,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 30,
                        generateLabels: function (chart) {
                            const data = chart.data;
                            return data.labels.map((label, i) => ({
                                text: label,
                                fillStyle: data.datasets[0].backgroundColor[i],
                                strokeStyle: data.datasets[0].borderColor[i],
                                lineWidth: data.datasets[0].borderWidth,
                                hidden: false,
                                index: i
                            }));
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Zero Chart Example'
                },
                tooltip: {
                    xAlign: 'left' // Set the x-alignment of tooltips to 'center'
                }
            },
            // hoverOffset: 70 // Adjust this value as needed
        }
    });

} else {
    // Otherwise, create the chart with actual values
    var ctx = document.getElementById('myDonutChart').getContext('2d');
    var myDonutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Total Purchases', 'Total Paid Amount', 'Remaining Pay'],
            datasets: [{
                data: [total_amountss, payment_amountss, balance_amountss],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1,
                offset: 30 // Explode effect value
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',
            borderRadius: 7,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 30,
                        generateLabels: function (chart) {
                            const data = chart.data;
                            return data.labels.map((label, i) => ({
                                text: label,
                                fillStyle: data.datasets[0].backgroundColor[i],
                                strokeStyle: data.datasets[0].borderColor[i],
                                lineWidth: data.datasets[0].borderWidth,
                                hidden: false,
                                index: i
                            }));
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Donut Chart Example'
                },
                tooltip: {
                    xAlign: 'left' // Set the x-alignment of tooltips to 'center'
                }
            },
            // hoverOffset: 70 // Adjust this value as needed
        }
    });
}

/////////////////////////////////////////////////////// DONUT_CHART END ////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////// FROM AND TO DATE //////////////////////////////////////////////////


// Function to update area chart values
function updateAreaChartValues(total_amount, payment_amount, balance_amount) {
    var total_amountss = parseFloat(total_amount) || 0;
    var payment_amountss = parseFloat(payment_amount) || 0;
    var balance_amountss = parseFloat(balance_amount) || 0;

    // Update area chart values only if data is available
    if (total_amountss !== 0 || payment_amountss !== 0 || balance_amountss !== 0) {
        var fromDate = document.getElementById('from-date').value;
        var toDate = document.getElementById('to-date').value;

        // Extract month from the fromDate and toDate
        var fromMonth = new Date(fromDate).getMonth() + 1; // Adding 1 to get 1-indexed months
        var toMonth = new Date(toDate).getMonth() + 1; // Adding 1 to get 1-indexed months

        // Check if the current month falls within the selected range
        if (fromMonth > toMonth) {
            // Display data for the selected month only
            document.getElementById('total-purchase-value').textContent = total_amountss;
            document.getElementById('total-paid-value').textContent = payment_amountss;
            document.getElementById('balance-value').textContent = balance_amountss;

            var max = Math.max(total_amountss);
            var offset = max * 1;

            var maxs = Math.max(payment_amountss);
            var offsets = maxs * 1;

            var maxss = Math.max(balance_amountss);
            var offsetss = maxss * 1;

            var datasets = myAreaChart.data.datasets;

            datasets[0].data = [total_amountss, offset, offset];
            datasets[1].data = [offsets, payment_amountss, offsets];
            datasets[2].data = [offsetss, offsetss, balance_amountss];

            myAreaChart.update();
        } else {
            // If the selected range spans multiple months, display an error message
            console.error('Selected date range should be within the same month.');
            // You may also display an error message to the user on the UI
        }
    }
}

// Function to update area chart values
function updateAreaChart(data) {
    if (data && data.monthlyData && Array.isArray(data.monthlyData) && data.monthlyData.length > 0) {
        console.log('Monthly data received:', data.monthlyData);

        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

        const months = [];
        const totalAmounts = [];
        data.monthlyData.forEach(item => {
            months.push(monthNames[item.month - 1]);
            totalAmounts.push(parseFloat(item.totalAmount) || 0); // Ensure totalAmount is parsed as a float or set to 0 if undefined
        });

        // Check if months and totalAmounts arrays are not empty
        if (months.length > 0 && totalAmounts.length > 0) {
            myAreaChart.data.labels = months;
            myAreaChart.data.datasets[0].data = totalAmounts;
            myAreaChart.update();
        } else {
            console.error('Monthly data is missing or invalid.', data);
        }
    } else {
        console.error('Monthly data is missing or invalid.', data);
    }
}

// Function to update values based on date range
function updateValues() {
    var fromDate = document.getElementById('from-date').value;
    var toDate = document.getElementById('to-date').value;

    if (fromDate.trim() !== '' && toDate.trim() !== '') {
        fetch(`/api/data?fromDate=${fromDate}&toDate=${toDate}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update area chart with monthly data
                updateAreaChart(data);
                
                // Update other elements with total amounts
                document.getElementById('total-purchases').value = parseFloat(data.total_amount) || 0;
                document.getElementById('total-paid-amount').value = parseFloat(data.payment_amount) || 0;
                document.getElementById('remaining-pay').value = parseFloat(data.balance_amount) || 0;

                // Update the donut chart
                myDonutChart.data.datasets[0].data = [
                    parseFloat(data.total_amount) || 0,
                    parseFloat(data.payment_amount) || 0,
                    parseFloat(data.balance_amount) || 0
                ];
                myDonutChart.update();

                // Update area chart values
                updateAreaChartValues(data.total_amount, data.payment_amount, data.balance_amount);

            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

// Add event listeners to the date inputs
document.getElementById('from-date').addEventListener('change', updateValues);
document.getElementById('to-date').addEventListener('change', updateValues);

// Initial chart rendering when the page loads
updateValues();


////////////////////////////////////////////////////////// FROM AND TO DATE END //////////////////////////////////////////////////////



/////////////////////////////////////////////////////// YEAR ////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function () {
    const yearCheckbox = document.getElementById('yearCheckbox');
    const yearSelect = document.getElementById('yearSelect');

    // Function to toggle the visibility of the year dropdown and populate years
    function toggleYearDropdown() {
        if (yearCheckbox.checked) {
            yearSelect.classList.remove('hidden');
            clearYears(); // Ensure any existing years or placeholder are cleared before populating
            populateYears();
        } else {
            yearSelect.classList.add('hidden');
            clearYears();
            showPlaceholder();
        }
    }

    // Function to populate years in the dropdown
    function populateYears() {
        const currentYear = new Date().getFullYear();
        for (let year = currentYear; year >= 1900; year--) {
            const option = document.createElement('option');
            option.textContent = year;
            yearSelect.appendChild(option);
        }
    }

    // Function to clear years from the dropdown
    function clearYears() {
        yearSelect.innerHTML = '';
    }

    // Function to show placeholder option
    function showPlaceholder() {
        const placeholderOption = document.createElement('option');
        placeholderOption.textContent = 'year';
        yearSelect.appendChild(placeholderOption);
    }

    // Event listener for checkbox change
    yearCheckbox.addEventListener('change', toggleYearDropdown);

    // Initial setup based on the current state of the checkbox
    toggleYearDropdown();
});

/////////////////////////////////////////////////////// YEAR END ////////////////////////////////////////////////////////////

/////////////////////////////////////////////// MONTH ///////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
    var checkbox = document.getElementById("showMonthsCheckbox");
    var dropdown = document.getElementById("monthDropdown");

    // Array of month names
    var months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ];

    // Function to populate dropdown with months
    function populateDropdown() {
        dropdown.innerHTML = ""; // Clear existing options

        months.forEach(function (month) {
            var option = document.createElement("option");
            option.text = month;
            dropdown.add(option);
        });
    }

    // Event listener for checkbox change
    checkbox.addEventListener("change", function () {
        if (checkbox.checked) {
            populateDropdown();
        } else {
            dropdown.innerHTML = ""; // Clear dropdown if checkbox is unchecked
            // Add placeholder option
            var placeholderOption = document.createElement("option");
            placeholderOption.text = "_month_";
            dropdown.add(placeholderOption);
        }
    });
});

/////////////////////////////////////////////// MONTH END ///////////////////////////////////////////////////////////


/////////////////////////////////////// WEEK ////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
    var weekCheckbox = document.getElementById("showWeeksCheckbox");
    var weekDropdown = document.getElementById("weeksDropdown");

    var weeks = [
        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'
    ];

    function populateWeeksDropdown() {
        weekDropdown.innerHTML = "";

        weeks.forEach(function (week) {
            var option = document.createElement('option');
            option.text = week;
            weekDropdown.add(option);
        });
    }

    weekCheckbox.addEventListener("change", function () {
        if (weekCheckbox.checked) {
            populateWeeksDropdown();
        } else {
            weekDropdown.innerHTML = ""; // Clear dropdown if checkbox is unchecked
            // Add placeholder option
            var placeholderOption = document.createElement("option");
            placeholderOption.text = "_weeks_";
            placeholderOption.disabled = true;
            placeholderOption.selected = true;
            weekDropdown.add(placeholderOption);
        }
    });

    // Initial placeholder option setup
    var initialPlaceholderOption = document.createElement("option");
    initialPlaceholderOption.text = "_weeks_";
    initialPlaceholderOption.disabled = true;
    initialPlaceholderOption.selected = true;
    weekDropdown.add(initialPlaceholderOption);
});

/////////////////////////////////////// WEEK END ////////////////////////////////////////////////////

/////////////////////////////////////// SELECTEDYEAR START ////////////////////////////////////////////////////

$(document).ready(function () {
    $('#yearCheckbox').change(function () {
        if (this.checked) {
            var selectedYear = $('#yearSelect').val();
            fetchYearlyData(selectedYear);
        } else {
            displayTotalSum();
        }
    });

    $('#yearSelect').change(function () {
        var selectedYear = $(this).val();
        fetchYearlyData(selectedYear);
    });
});

function fetchYearlyData(selectedYear) {
    $.ajax({
        type: 'GET',
        url: '/get_yearly_data/',
        data: {
            year: selectedYear
        },
        success: function (response) {
            updateFields(response);
            updateDonutChart(response);
            updateAreaChart(response);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}

function updateFields(data) {
    $('#total-purchases').val(data.total_amount);
    $('#total-paid-amount').val(data.payment_amount);
    $('#remaining-pay').val(data.balance_amount);
}

function updateDonutChart(data) {
    myDonutChart.data.datasets[0].data = [data.total_amount, data.payment_amount, data.balance_amount];
    myDonutChart.update();
}

function updateAreaChart(data) {
    if (data && data.monthlyData && Array.isArray(data.monthlyData) && data.monthlyData.length > 0) {
        console.log('Monthly data received:', data.monthlyData);

        var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

        var months = data.monthlyData.map(function (item) {
            return monthNames[item.month - 1];
        });

        myAreaChart.data.labels = months;
        myAreaChart.data.datasets[0].data = data.monthlyData.map(function (item) {
            return item.total_amount;
        });
        myAreaChart.data.datasets[1].data = data.monthlyData.map(function (item) {
            return item.total_payment;
        });
        myAreaChart.data.datasets[2].data = data.monthlyData.map(function (item) {
            return item.total_balance;
        });

        // Ensure that the line is always displayed by setting fill to 'origin' and adjust fill color and opacity
        myAreaChart.data.datasets.forEach(function(dataset) {
            dataset.fill = 'origin';
            dataset.backgroundColor = 'rgba(0, 123, 255, 0.05)'; // Adjust the color and opacity as needed
        });

        console.log('Updated chart data:', myAreaChart.data);

        myAreaChart.update();
    } else {
        console.error('Monthly data is missing or invalid.', data);
    }
}



function displayTotalSum() {
    $.ajax({
        type: 'GET',
        url: '/get_total_sum/',
        success: function (response) {
            updateFields(response);
            updateDonutChart(response);
            updateAreaChart(response); // Corrected function call

        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}



/////////////////////////////////////// YEAR END ////////////////////////////////////////////////////

/////////////////////////////////////// SELECTEDMONTHS START ////////////////////////////////////////////////////

$(document).ready(function () {
    // Function to handle changes in the checkbox and dropdown
    function updateData() {
        if ($('#showMonthsCheckbox').prop('checked')) {
            var selectedMonth = $('#monthDropdown').val();
            $.ajax({
                type: 'GET',
                url: '/get_monthly_data/',
                data: {
                    month: selectedMonth
                },
                success: function (response) {
                    $('#total-purchases').val(response.total_amount);
                    $('#total-paid-amount').val(response.payment_amount);
                    $('#remaining-pay').val(response.balance_amount);

                    updateDonutChart(response);
                    updateAreaCharts(response);
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        } else {
            displayTotalSum();
        }
    }

    // Event listeners for checkbox and dropdown change events
    $('#showMonthsCheckbox').change(updateData);
    $('#monthDropdown').change(updateData);
});

// Function to update the donut chart
function updateDonutChart(data) {
    myDonutChart.data.datasets[0].data = [data.total_amount, data.payment_amount, data.balance_amount];
    myDonutChart.update();
}

// Function to update the area chart with monthly data
function updateAreaCharts(data) {
    if (data && data.invoice_data) {
        var labels = [];
        var totalAmounts = [];
        var paymentAmounts = [];
        var balanceAmounts = [];

        data.invoice_data.forEach(function(invoice) {
            labels.push(new Date(invoice.invoice_date).toLocaleDateString());
            totalAmounts.push(invoice.invoice_amount);  // Use invoice_amount for total_amount
            paymentAmounts.push(invoice.payment_amount);
            balanceAmounts.push(invoice.balance_amount);
        });

        myAreaChart.data.labels = labels;
        myAreaChart.data.datasets[0].data = totalAmounts;  // Assign totalAmounts for total_amount
        myAreaChart.data.datasets[1].data = paymentAmounts;
        myAreaChart.data.datasets[2].data = balanceAmounts;
        myAreaChart.update();
    } else {
        console.error('Monthly data is missing or invalid.');
    }
}

function displayTotalSum() {
    // Make an AJAX request to get the sum of all data
    $.ajax({
        type: 'GET',
        url: '/get_total_sum/',
        success: function (response) {
            // Update fields and donut chart with sum data
            updateFields(response);
            updateDonutChart(response);
            updateAreaCharts(response);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}

/////////////////////////////////////// SELECTEDMONTHS END ////////////////////////////////////////////////////


///////////////////////////////////////////////// SELECTED YEAR MONTH START ////////////////////////////////////////////////

$(document).ready(function () {
    // Event listener for year checkbox change
    $('#yearCheckbox').change(function () {
        if (this.checked) {
            var selectedYear = $('#yearSelect').val();
            getData(selectedYear);
        }
    });

    // Event listener for year dropdown change
    $('#yearSelect').change(function () {
        var selectedYear = $(this).val();
        getData(selectedYear);
    });

    // Event listener for month checkbox and dropdown change
    $('#showMonthsCheckbox, #monthDropdown').change(function () {
        if ($('#showMonthsCheckbox').prop('checked')) {
            var selectedYear = $('#yearSelect').val();
            var selectedMonth = $('#monthDropdown').val();
            getMonthlyData(selectedYear, selectedMonth);
        }
    });
});

// Function to fetch yearly data
function getData(selectedYear) {
    $.ajax({
        type: 'GET',
        url: '/get_yearly_data/',
        data: {
            year: selectedYear
        },
        success: function (response) {
            updateFields(response);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}
// Function to update the area chart with monthly data
function updateAreaCharts(data) {
    if (data && data.invoice_data) {
        var labels = [];
        var totalAmounts = [];
        var paymentAmounts = [];
        var balanceAmounts = [];

        data.invoice_data.forEach(function(invoice) {
            labels.push(new Date(invoice.invoice_date).toLocaleDateString());
            totalAmounts.push(invoice.invoice_amount);  // Use invoice_amount for total_amount
            paymentAmounts.push(invoice.payment_amount);
            balanceAmounts.push(invoice.balance_amount);
        });

        myAreaChart.data.labels = labels;
        myAreaChart.data.datasets[0].data = totalAmounts;  // Assign totalAmounts for total_amount
        myAreaChart.data.datasets[1].data = paymentAmounts;
        myAreaChart.data.datasets[2].data = balanceAmounts;
        myAreaChart.update();
    } else {
        console.error('Monthly data is missing or invalid.');
    }
}

// Function to fetch monthly data
function getMonthlyData(selectedYear, selectedMonth) {
    var requestData = { month: selectedMonth };

    // Add year to request data if selected
    if (selectedYear) {
        requestData.year = selectedYear;
    }

    $.ajax({
        type: 'GET',
        url: '/get_monthly_data/',
        data: requestData,
        success: function (response) {
            updateFields(response);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}

// Function to update fields with received data
function updateFields(data) {
    $('#total-purchases').val(data.total_amount);
    $('#total-paid-amount').val(data.payment_amount);
    $('#remaining-pay').val(data.balance_amount);

     // Call updateAreaCharts to update the chart
     updateAreaCharts(data);
}

///////////////////////////////////////////////// SELECTED YEAR MONTH END ////////////////////////////////////////////////

//////////////////////////////////////////////// AREA CHARTJS ////////////////////////////////////////////////

var total_amountss = parseFloat(document.getElementById("total-purchases").value) || 0;
var payment_amountss = parseFloat(document.getElementById("total-paid-amount").value) || 0;
var balance_amountss = parseFloat(document.getElementById("remaining-pay").value) || 0;

document.getElementById('total-purchase-value').textContent = total_amountss;
document.getElementById('total-paid-value').textContent = payment_amountss;
document.getElementById('balance-value').textContent = balance_amountss;

var max = Math.max(total_amountss);
var offset = max*1 

var maxs = Math.max(payment_amountss);
var offsets = maxs*1

var maxss = Math.max(balance_amountss);
var offsetss = maxss*1


var ctxArea = document.getElementById('myAreaChart').getContext('2d');
var myAreaChart = new Chart(ctxArea, {
    type: 'line',
    data: {
        labels: ['Total Amount','Payment Amount','Balance Amount'],
        datasets: [
            {
                label: 'Total Amount',
                data: [total_amountss, offset, offset],
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false,
                pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                pointRadius: 4
            },
            {
                label: 'Payment Amount',
                data: [offsets, payment_amountss, offsets],
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                fill: false,
                pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                pointRadius: 4
            },
            {
                label: 'Balance Amount',
                data: [offsetss, offsetss, balance_amountss],
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                fill: false,
                pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                pointRadius: 4
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    fontColor: "#000",
                    fontSize: 14
                },
                border: {
                    display: false
                },
                grid: {
                    display: false
                },
                stacked: true,
                title: {
                    display: true,
                }
            },
            x: {
                border: {
                    display: false
                },
                grid: {
                    display: false
                },
                display: true,
                stacked: true,
            }
        },
        layout: {
            padding: {
                left: 20,
                right: 120,
                top: 20,
                bottom: 20
            }
        },
        plugins: {
            legend: {
                display: false // Hide the built-in legend
            }
        }
    }
});



