function printDiv(divName) {
    var printContents = document.querySelector('#' + divName).innerHTML;
    var printWindow = window.open('', '_blank');
    
    printWindow.document.write('<html><head><title>Print</title></head><body>');
    printWindow.document.write(printContents);
    printWindow.document.write('</body></html>');

    printWindow.document.close();
    printWindow.print();
    printWindow.close();
    // Restore the original content after printing
    document.body.innerHTML = originalContents;
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.export-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = link.getAttribute('href');
        });
    });

    // Open the default tab on window load
    document.querySelector(".tablinks.active").click();
});

function openTab(evt, TabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(TabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function changeTable() {
    var selectedTable = document.getElementById("tableSelector").value;

    var tables = document.querySelectorAll('.box table');
    tables.forEach(function(table) {
        table.style.display = 'none';
    });

    if (selectedTable === 'table1') {
        document.querySelector('.box').style.display = 'block';
        document.getElementById('table1').style.display = 'block';
        document.getElementById('table2').style.display = 'none';
        document.querySelector('.boxes').style.display = 'none';
    } else if (selectedTable === 'table2') {
        document.querySelector('.boxes').style.display = 'block';
        document.querySelector('.box').style.display ='none';
        document.getElementById('table1').style.display = 'none';
        document.getElementById('table2').style.display = 'block';
    }

    const agen = document.querySelector(".format2");
    const agency = document.querySelector(".agency");

    if (selectedTable === "table2") {
        agency.style.display = "none";
    } else {
        agency.style.display = "block";
    }

    document.getElementById(selectedTable).style.display = "block";
}

// Save the original body content on window load
var originalContents = document.body.innerHTML;

// Open the default tab on window load
window.onload = function() {
    document.querySelector(".tablinks.active").click();
};