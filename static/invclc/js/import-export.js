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

const tablechange =  document.querySelector("#tableSelector");
  tablechange.addEventListener("change",changeTable)
  function changeTable() {
    var selectedOption = document.getElementById("tableSelector").value;
    if (selectedOption === "table1") {
      document.getElementById("table1").style.display = "block";
      document.getElementById("table2").style.display = "none";
      document.querySelector(".lastbox-content-agency").style.display = "none";
      document.querySelector(".panel-container").style.display = "block";
      document.querySelector(".panel-container").style.display = "flex";
      document.querySelector(".box2").style.justifyContent = "center"; 

    } else if (selectedOption === "table2") {
      document.getElementById("table1").style.display = "none";
      document.getElementById("table2").style.display = "block";
      document.querySelector(".lastbox-content-agency").style.display = "block";
      document.querySelector(".panel-container").style.display = "none";
      document.querySelector("#table2").style.display = "flex";
      document.querySelector("#table2").style.flexDirection = "column";
      document.querySelector("#table2").style.justifyContent = "center";
      document.querySelector("#table2").style.alignItems = "center";  
    }
    console.log(selectedOption)
  }

// Save the original body content on window load
var originalContents = document.body.innerHTML;

// Open the default tab on window load
window.onload = function() {
    document.querySelector(".tablinks.active").click();
};

// for import a table
function handleFileSelect(inputId) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (file) {
        if (file.type === 'application/pdf') {
            const reader = new FileReader();
            reader.onload = function(event) {
                const pdfContent = event.target.result;
                // Create container div
                const container = document.createElement('div');
                container.style.display = 'flex';
                container.style.alignItems = 'center';
                container.style.justifyContent = 'center';
                container.style.width = '100vw'; // Full viewport width
                container.style.height = '100vh'; // Full viewport height
                
                
                // Create iframe element
                const iframe = document.createElement('iframe');
                iframe.setAttribute('src', pdfContent);
                // Set style for iframe to cover most of the screen
                iframe.style.width = '90vw'; // 90% of viewport width
                iframe.style.height = '90vh'; // 90% of viewport height
                iframe.style.border = 'none'; // Remove iframe border
                
                // Append iframe to container
                container.appendChild(iframe);
                // Append container to body
                document.body.appendChild(container);
            };
            reader.readAsDataURL(file);
        } else {
            // Handle other file types
            console.log('Unsupported file type');
        }
    }
}

//  function handleFileSelect(inputId) {
//             var file = document.getElementById(inputId).files[0];
//             var reader = new FileReader();

//             reader.onload = function(event) {
//                 var csvData = event.target.result;
//                 displayCSV(csvData);
//             };

//             reader.readAsText(file);
//         }

//         function displayCSV(csvData) {
//             // Split CSV data into rows
//             var rows = csvData.split("\n");
            
//             // Create a table element
//             var table = document.createElement("table");

//             // Iterate through rows and create table rows and cells
//             rows.forEach(function(rowData) {
//                 var row = document.createElement("tr");
//                 var cells = rowData.split(",");
//                 cells.forEach(function(cellData) {
//                     var cell = document.createElement("td");
//                     cell.appendChild(document.createTextNode(cellData));
//                     row.appendChild(cell);
//                 });
//                 table.appendChild(row);
//             });

//             // Append the table to the body of the document
//             document.body.appendChild(table);
//         }


function handleFileSelect(inputId) {
    var file = document.getElementById(inputId).files[0];
    var reader = new FileReader();

    reader.onload = function(event) {
        var csvData = event.target.result;
        displayCSV(csvData);
    };

    reader.readAsText(file);
}
function displayCSV(csvData) {
    // Split CSV data into rows
    var rows = csvData.split("\n");
    
    // Create a table element
    var table = document.createElement("table");
    var tbody = document.createElement("tbody");

    // Iterate through rows and create table rows and cells
    rows.forEach(function(rowData) {
        var row = document.createElement("tr");
        var cells = rowData.split(",");
        cells.forEach(function(cellData) {
            var cell = document.createElement("td");
            cell.appendChild(document.createTextNode(cellData));
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });

    // Append the tbody to the table
    table.appendChild(tbody);

    // Create a div to center the table
    var centerDiv = document.createElement("div");
    centerDiv.style.display = "flex";
    centerDiv.style.justifyContent = "center";
    centerDiv.appendChild(table);

    // Append the centered table to the main-box div inside tabcontent
    var mainBox = document.querySelector('.tabcontent .main-box');
    mainBox.appendChild(centerDiv);
}

