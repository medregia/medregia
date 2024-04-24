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
  document.getElementById(cityName).style.display = "inline-flex";
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
  var activeTab = document.querySelector(".tablinks.active");
  if (activeTab) {
    activeTab.click();
  }
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
const csvFileInput = document.querySelector('input[type="file"]');
const csvContainer = document.getElementById("csvContainer");
const tableContainer = document.getElementById("table2");
const table = document.getElementById("tableContainer");
const csvTable = document.getElementById("csvTable");
const uploadButton = document.getElementById("Upload-btn");
const lastboxAgency = document.querySelector(".lastbox-content-agency");

// Initially hide the upload button
// uploadButton.style.display = "none";

// Event listener for CSV file input change
// csvFileInput.addEventListener("change", function() {
// // If a file is selected, show the upload button
// if (csvFileInput.files.length > 0) {
//   uploadButton.style.display = "block";
// } else {
//   // Otherwise, hide the upload button
//   uploadButton.style.display = "none";
// }
// });


// Event listener for table selector change
// Assuming csvFileInput is the input element for CSV files

// Assuming uploadButton is the submit button

tableSelector.addEventListener("change", function() {
  if (tableSelector.value === "format1") {
      // Show the panel-container for format 1
      const panelContainer = document.querySelector(".panel-container");
      panelContainer.style.display = "flex";
      panelContainer.style.justifyContent = "center";
      panelContainer.style.alignItems = "center";

      csvContainer.style.display = "block";
      tableContainer.style.display = "none";
      lastboxAgency.style.display = "none";
      table.style.display = "none";
      csvContainer.style.textAlign = "center";
      csvTable.style.width = "100%";
      csvTable.style.margin = "0 auto";

      // Show the upload button when format1 is selected and a file is chosen
      if (csvFileInput && csvFileInput.files.length > 0) {
          uploadButton.style.display = "block";
      } 
      // else {
      //     uploadButton.style.display = "none";
      // }

      // Show the buttons to choose CSV, PDF, and Excel files for format 1
      document.querySelectorAll(".btn.pdf, .btn.xlsx").forEach(function(btn) {
          btn.style.display = "block";
      });
  } else if (tableSelector.value === "format2") {
      // Hide the panel-container for format 2
      document.querySelector(".panel-container").style.display = "none";

      csvContainer.style.display = "none";
      tableContainer.style.display = "block";
      lastboxAgency.style.display = "block";
      table.style.display = "block";

      // Hide the upload button when format2 is selected
      // uploadButton.style.display = "none";

      // Hide the buttons to choose CSV, PDF, and Excel files for format 2
      document.querySelectorAll(".btn.pdf, .btn.xlsx").forEach(function(btn) {
          btn.style.display = "none";
      });
  }
});






// Event listener for CSV file input change
// csvFileInput.addEventListener("change", function() {
//   // If a file is selected and the format is set to format1, show the upload button
//   if (csvFileInput.files.length > 0 && tableSelector.value === "format1") {
//       uploadButton.style.display = "block";
//   } else {
//       // Otherwise, hide the upload button
//       uploadButton.style.display = "none";
//   }
// });


// const trElements = csvTable.getElementsByTagName("tr");
// for (let i = 0; i < trElements.length; i++) {
// trElements[i].style.border = "1px solid #ccc";
// }

// // Add border to td elements
// const tdElements = csvTable.getElementsByTagName("td");
// for (let i = 0; i < tdElements.length; i++) {
// tdElements[i].style.border = "1px solid #ccc";
// }

// // Add border to th elements
// const thElements = csvTable.getElementsByTagName("th");
// for (let i = 0; i < thElements.length; i++) {
// thElements[i].style.border = "1px solid #ccc";
// }


// csvFileInput.addEventListener("change", function() {
// loadCSV();
// });

// function loadCSV() {
// const file = csvFileInput.files[0];
// if (file) {
//   const reader = new FileReader();
//   reader.onload = function(e) {
//     const lines = e.target.result.split('\n');
//     csvTable.innerHTML = ""; // Clear previous table data
//     lines.forEach(line => {
//       const cells = line.split(',');
//       const row = csvTable.insertRow();
//       cells.forEach(cell => {
//         const cellElement = row.insertCell();
//         cellElement.textContent = cell;
//       });
//     });
//   };
//   reader.readAsText(file);
// }
// }

// function loadTable() {
// }

// function clearTable() {
// csvTable.innerHTML = ""; 
// } 


document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch filtered data
    function fetchData(completed, category, others,all) {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch('/import-export/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: 'completed=' + completed + '&category=' + category + '&others=' + others + '&csrfmiddlewaretoken=' + csrfToken + '&all=' + all
        })
        .then(response => response.json()) // Parse response as JSON
        .then(data => {
            console.log("Data : ",data)
            if (data.completed_data){
                updateTableWithData(data.completed_data); // Call updateTableWithData with JSON data
                // console.log(data.completed_data)
            }
            else if (data.not_paid_data){
                console.log("not_paid_data : ",data.not_paid_data);
                updateTableWithData(data.not_paid_data)
            }
            else{
                updateTableWithData(data.previous_data);
                // console.log(data.previous_data)
            }

        })
        .catch(error => {
            console.warn('Error:', error);
        });
    }

    // Listen for changes in checkboxes
    document.querySelectorAll('.export2 input[type="checkbox"]').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            var completed = document.querySelector('.export2-box1 input[name="completed"]').checked;
            var all = document.querySelector('.export2-box1 input[name="all"]').checked;
            var pharmacy = document.querySelector('.export2-box2 input[name="pharmacy"]').checked;
            var medical = document.querySelector('.export2-box2 input[name="medical"]').checked;
            var agency = document.querySelector('.export2-box2 input[name="agency"]').checked;
            var others = document.querySelector('.export2-box2 input[name="others"]');

            // Construct category based on selected checkboxes
            var category = [];
            if (pharmacy) category.push('Pharmacy');
            if (medical) category.push('medical');
            if (agency) category.push('Agency');

            // If Others checkbox is checked, add its value to category
            if (others) {
                var otherValue = document.querySelector('.export2-box2 input[name="other_value"]').value;
                if (otherValue.trim() !== '') {
                    category.push(otherValue.trim());
                }
            }

            // Join category array into a comma-separated string
            var categoryString = category.join(',');

            // Fetch filtered data
            fetchData(completed, categoryString, others,all);
        });
    });
});


// Function to update table with JSON data
function updateTableWithData(data) {
    var tableBody = document.querySelector('#export-data tbody');
    if (tableBody) {
        tableBody.innerHTML = ''; // Clear existing rows
        if (data !== null && data !== undefined && Array.isArray(data)) {
            data.forEach(function(item) {
                var row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="checkbox"></td>
                    <td>${item.invoice_number}</td>
                    <td>${item.invoice_amount}</td>
                    <td>${item.updated_by}</td>
                    <td>${item.today_date}</td>
                    <td>${item.payment_amount}</td>
                    <td>${item.balance_amount == 0 ? 'Paid' : 'Pending'}</td>
                    <td></td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error('Data is not an array or is null/undefined.');
        }
    } else {
        console.error('#export-data tbody not found');
    }
}




function displayCSV(file) {
        // Create a FileReader object
        var reader = new FileReader();

        // Define the onload event handler
        reader.onload = function(event) {
            // Parse CSV content
            var csv = event.target.result;
            var rows = csv.split('\n');

            // Clear existing table content
            var table = document.getElementById('csvTable');
            table.innerHTML = '';

            // Loop through CSV rows and create table rows
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i].split(',');
                var tr = document.createElement('tr');

                // Create table cells
                for (var j = 0; j < row.length; j++) {
                    var td = document.createElement('td');
                    td.textContent = row[j];
                    tr.appendChild(td);
                }

                // Append row to table
                table.appendChild(tr);
            }
        };

        // Read the uploaded file as text
        reader.readAsText(file);
    }

    // Add event listener to file input
    var fileInput = document.querySelector('input[type="file"]');
    const csvButton = document.querySelector('.upload-btn')
    fileInput.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            displayCSV(file);
            csvButton.classList.toggle('vanish')
        }
    });

document.getElementById("uploadBtn").addEventListener("click", function() {
    const uploadMsg = document.querySelector(".upload-msg");
    let form = document.getElementById("uploadForm");
    let formData = new FormData(form);
    fetch('/upload_csv/', {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            uploadMsg.textContent = "File Upload Failed Due to Duplicate Entry of Invoice Number or Incorrect Date Format";
            uploadMsg.style.color = "red";
            throw new Error('File Upload Failed Due to Duplicate Entry of Invoice Number or Incorrect Date Format');
        }
    })
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            if (response.status === 500) {
                uploadMsg.textContent = "! Please check your data. Your data must satisfy the following requirements !";
                uploadMsg.style.color = "orange";
            }
        } else {
            uploadMsg.textContent = data.message;
            uploadMsg.style.color = "green";
        }
    })
    .catch(error => {
        console.error('File Upload Error:', error);
        uploadMsg.textContent = error;
        uploadMsg.style.color = "red";
    });
});
