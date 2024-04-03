function opentab(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }


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

const tableSelector = document.getElementById("tableSelector");
const csvFileInput = document.getElementById("csv_file_input");
const csvContainer = document.getElementById("csvContainer");
const tableContainer = document.getElementById("table2");
const table = document.getElementById("tableContainer");
const csvTable = document.getElementById("csvTable");
const upload = document.getElementById("upload");


const lastboxAgency = document.querySelector(".lastbox-content-agency");

tableSelector.addEventListener("change", function() {
  if (tableSelector.value === "format1") {
    csvContainer.style.display = "block";
    tableContainer.style.display = "none";
    lastboxAgency.style.display = "none";
    table.style.display = "none";
    csvContainer.style.textAlign = "center";
    csvTable.style.width = "100%";
    csvTable.style.margin = "0 auto";
    upload.style.display = "block";

//   } else {
//     csvContainer.style.display = "none";
//     tableContainer.style.display = "block";
//     lastboxAgency.style.display = "block";
//     loadTable();
//   }
  }else if (tableSelector.value === "format2"){
    csvContainer.style.display = "none";
    tableContainer.style.display = "block";
    lastboxAgency.style.display = "block";
    table.style.display = "block";
    upload.style.display = "none";
}

const trElements = csvTable.getElementsByTagName("tr");
for (let i = 0; i < trElements.length; i++) {
  trElements[i].style.border = "1px solid #ccc";
}

// Add border to td elements
const tdElements = csvTable.getElementsByTagName("td");
for (let i = 0; i < tdElements.length; i++) {
  tdElements[i].style.border = "1px solid #ccc";
}

// Add border to th elements
const thElements = csvTable.getElementsByTagName("th");
for (let i = 0; i < thElements.length; i++) {
  thElements[i].style.border = "1px solid #ccc";
}

});

csvFileInput.addEventListener("change", function() {
  loadCSV();
});

function loadCSV() {
  const file = csvFileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const lines = e.target.result.split('\n');
      csvTable.innerHTML = ""; // Clear previous table data
      lines.forEach(line => {
        const cells = line.split(',');
        const row = csvTable.insertRow();
        cells.forEach(cell => {
          const cellElement = row.insertCell();
          cellElement.textContent = cell;
        });
      });
    };
    reader.readAsText(file);
  }
}

function loadTable() {
  // You need to implement the logic to load the table data for format 2 here
}

function clearTable() {
  csvTable.innerHTML = ""; // Clear CSV table
  // You may want to clear data in the table for format 2 here as well
}