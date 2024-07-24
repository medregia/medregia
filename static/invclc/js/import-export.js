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
    function fetchData(completed, category, others,all,pharmacy_name) {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const spanErrors = document.querySelector('span.sidePanelErrors')
        fetch('/import-export/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: 'completed=' + completed + '&category=' + category + '&others=' + others + '&csrfmiddlewaretoken=' + csrfToken + '&all=' + all + '&pharmacyName=' + pharmacy_name
        })
        .then(response => response.json()) // Parse response as JSON
        .then(data => {
            if (data.completed_data){
                updateTableWithData(data.completed_data); // Call updateTableWithData with JSON data
                // console.log(data.completed_data)
            }
            else if (data.not_paid_data){   
                updateTableWithData(data.not_paid_data)
            }
            else if (data.category_list){
                updateTableWithCategoryData(data.category_list);
                // console.log(data.category_list)
            }
            else if (data.storeTypeList){
                updateTableWithOthersData(data.storeTypeList);
            }
            else if (data.otherStores){
                updateTableWithOthersData(data.otherStores);
            }
            else if (data.invoices){
                updateTableWithData(data.invoices)
            }
            else{
                updateTableWithData(data.previous_data);
                // console.log(data.previous_data)
            }
            spanErrors.innerHTML = "";
        })
        .catch(error => {
            if (error){
                spanErrors.innerHTML = "No Such Data Found ..";
                // console.warn('Error:', error);
            }
        });
    }

    // Listen for changes in checkboxes
    document.querySelectorAll('.export2 input[type="checkbox"]:not(#checkboxTable .checkbox)').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            var completed = document.querySelector('.export2-box1 input[name="completed"]').checked;
            var all = document.querySelector('.export2-box1 input[name="all"]').checked;
            var pharmacy = document.querySelector('.export2-box2 input[name="pharmacy"]').checked;
            var medical = document.querySelector('.export2-box2 input[name="medical"]').checked;
            var retailer = document.querySelector('.export2-box2 input[name="retailer"]').checked;

            // Construct category based on selected checkboxes
            var category = [];
            if (pharmacy) category.push('Pharmacy');
            if (medical) category.push('medical');
            if (retailer) category.push('retailer');

            // If Others checkbox is checked, add its value to category


            // Join category array into a comma-separated string
            var categoryString = category.join(',');

            // Fetch filtered data
            fetchData(completed, categoryString,'',all,'');
        });
    });

    var otherDetails = document.querySelector('.export2-box2 input[name="others"]');
    if (otherDetails) {
        otherDetails.addEventListener("input", function() {
            var otherDetail = otherDetails.value.trim();
            if (otherDetail !== '') {
                fetchData(false, '', otherDetail, false,''); // Assuming "completed", "category", and "all" should not be sent when changing the "others" input
            }
        });
    }

    const resetExport = document.querySelector(".export-reset")
    resetExport.addEventListener("click",()=>{
        location.reload()
    })

    document.querySelectorAll('#checkboxTable .checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                const pharmacyName = this.dataset.pharmacy;
                fetchData(false, '', '', false, pharmacyName);
            }
            else{
                fetchData(false, '', '', false, '');
            }
        });
    });
});




// Function to update table with JSON data
function formatDate(dateString) {
    // Parse the date string into a Date object
    var date = new Date(dateString);

    // Extract day, month, and year components
    var day = date.getDate();
    var month = date.getMonth() + 1; // Months are zero-based
    var year = date.getFullYear();

    // Ensure day and month are two digits
    if (day < 10) {
        day = '0' + day;
    }
    if (month < 10) {
        month = '0' + month;
    }

    // Return the formatted date string
    return day + '/' + month + '/' + year;
}

function updateTableWithData(data) {
    var tableBody = document.querySelector('#export-data tbody');
    var tableHeader = document.querySelector('#export-data thead tr');

    if (tableBody && tableHeader) {
        tableBody.innerHTML = ''; // Clear existing rows

        if (data !== null && data !== undefined && Array.isArray(data) && data.length > 0) {
            // Clear existing header
            tableHeader.innerHTML = '';

            // Add a checkbox field to the header
            var checkboxTh = document.createElement('th');
            var headerCheckbox = document.createElement('input');
            headerCheckbox.type = 'checkbox';
            headerCheckbox.addEventListener('click', function() {
                var checkboxes = document.querySelectorAll('#export-data tbody input[type="checkbox"]');
                checkboxes.forEach(function(checkbox) {
                    checkbox.checked = headerCheckbox.checked;
                });
            });
            checkboxTh.appendChild(headerCheckbox);
            tableHeader.appendChild(checkboxTh);

            // Get keys from the first item in the data
            var keys = Object.keys(data[0]);

            // Update table header
            keys.forEach(function(key) {
                var th = document.createElement('th');
                th.textContent = key;
                tableHeader.appendChild(th);
            });

            // Add "Remark" column to the header
            var remarkTh = document.createElement('th');
            remarkTh.textContent = 'Remark';
            tableHeader.appendChild(remarkTh);

            // Populate table rows
            data.forEach(function(item) {
                var row = document.createElement('tr');

                // Add a checkbox to each row
                var checkboxCell = document.createElement('td');
                var checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkboxCell.appendChild(checkbox);
                row.appendChild(checkboxCell);

                // Create table cells based on keys
                keys.forEach(function(key) {
                    var cell = document.createElement('td');
                    // Check if the key is 'invoice_date' and format the date
                    if (key === 'today_date'){
                        cell.textContent = formatDate(item[key]);
                    } 
                    else if (key === 'Invoice date'){
                        cell.textContent = formatDate(item[key]);
                    }
                    else if (key === 'Today date'){
                        cell.textContent = formatDate(item[key]);
                    }
                    else {
                        cell.textContent = item[key];
                    }
                    row.appendChild(cell);
                });

                // Add empty "Remark" cell
                var remarkCell = document.createElement('td');
                remarkCell.textContent = ''; // or any default value for remark
                row.appendChild(remarkCell);

                tableBody.appendChild(row);
            });
        } else {
            spanErrors.innerHTML = "No Such Data Found ..";
            console.error('Data is not an array or is null/undefined, or the array is empty.');
        }
    } else {
        console.error('#export-data tbody or thead tr not found');
    }
}



function updateTableWithCategoryData(data) {
    var tableHeader = document.querySelector('#export-data thead tr');
    var tableBody = document.querySelector('#export-data tbody');

    if (tableHeader && tableBody) {
        tableHeader.innerHTML = ''; // Clear existing header
        tableBody.innerHTML = ''; // Clear existing body

        // Construct new header
        var headers = Object.keys(data[0]);
        headers.forEach(function(header) {
            var th = document.createElement('th');
            th.textContent = header;
            tableHeader.appendChild(th);
        });

        // Construct body with category data
        data.forEach(function(item) {
            var row = document.createElement('tr');
            headers.forEach(function(header) {
                var td = document.createElement('td');
                td.textContent = item[header];
                row.appendChild(td);
            });
            tableBody.appendChild(row);
        });
    } else {
        console.error('#export-data thead tr or tbody not found');
    }
}

function updateTableWithOthersData(data){
    var otherHeader = document.querySelector('#export-data thead tr');
    var otherBody = document.querySelector('#export-data tbody');

    if (otherHeader && otherBody) {
        otherHeader.innerHTML = ''; // Clear existing header
        otherBody.innerHTML = ''; // Clear existing body

        // Construct new header
        var headers = Object.keys(data[0]);
        headers.forEach(function(header) {
            var th = document.createElement('th');
            th.textContent = header;
            otherHeader.appendChild(th);
        });

        // Construct body with category data
        data.forEach(function(item) {
            var row = document.createElement('tr');
            headers.forEach(function(header) {
                var td = document.createElement('td');
                td.textContent = item[header];
                row.appendChild(td);
            });
            otherBody.appendChild(row);
        });
    } else {
        console.error('#export-data thead tr or tbody not found');
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

var allCheckbox = document.querySelector('input[name="all"]');
var completedCheckbox = document.querySelector('input[name="completed"]');
var pharmacyCheckbox = document.querySelector('input[name="pharmacy"]');
var medicalCheckbox = document.querySelector('input[name="medical"]');
var retailerCheckbox = document.querySelector('input[name="retailer"]');

allCheckbox.addEventListener("click", function() {
    if (completedCheckbox.checked) {
        completedCheckbox.checked = false;
    }
    if (pharmacyCheckbox.checked) {
        pharmacyCheckbox.checked = false;
    }
    if (medicalCheckbox.checked) {
        medicalCheckbox.checked = false;
    }
    if (retailerCheckbox.checked) {
        retailerCheckbox.checked = false;
    }
});

completedCheckbox.addEventListener("click", function() {
    if (allCheckbox.checked) {
        allCheckbox.checked = false;
    }
    if (pharmacyCheckbox.checked) {
        pharmacyCheckbox.checked = false;
    }
    if (medicalCheckbox.checked) {
        medicalCheckbox.checked = false;
    }
    if (retailerCheckbox.checked) {
        retailerCheckbox.checked = false;
    }
});

pharmacyCheckbox.addEventListener("click", function() {
    if (allCheckbox.checked) {
        allCheckbox.checked = false;
    }
    if (completedCheckbox.checked) {
        completedCheckbox.checked = false;
    }
    if (medicalCheckbox.checked) {
        medicalCheckbox.checked = false;
    }
    if (retailerCheckbox.checked) {
        retailerCheckbox.checked = false;
    }
});

medicalCheckbox.addEventListener("click", function() {
    if (allCheckbox.checked) {
        allCheckbox.checked = false;
    }
    if (completedCheckbox.checked) {
        completedCheckbox.checked = false;
    }
    if (pharmacyCheckbox.checked) {
        pharmacyCheckbox.checked = false;
    }
    if (retailerCheckbox.checked) {
        retailerCheckbox.checked = false;
    }
});

retailerCheckbox.addEventListener("click", function() {
    if (allCheckbox.checked) {
        allCheckbox.checked = false;
    }
    if (completedCheckbox.checked) {
        completedCheckbox.checked = false;
    }
    if (pharmacyCheckbox.checked) {
        pharmacyCheckbox.checked = false;
    }
    if (medicalCheckbox.checked) {
        medicalCheckbox.checked = false;
    }
});


// Get all checkboxes
const checkboxes = document.querySelectorAll('.checkbox');

// Add event listener to each checkbox
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function() {
        if (this.checked) {
            checkboxes.forEach(otherCheckbox => {
                if (otherCheckbox !== this) {
                    otherCheckbox.checked = false;
                }
            });
        }
    });
});


// const pharmacyCheckbox = document.getElementById('pharmacyCheckbox');


const otherCheckboxes = document.querySelectorAll('.checkbox:not(#pharmacyCheckbox)');


pharmacyCheckbox.addEventListener('click', function() {
    if (this.checked) {
        otherCheckboxes.forEach(otherCheckbox => {
            otherCheckbox.checked = false;
        });
    }
});

otherCheckboxes.forEach(otherCheckbox => {
    otherCheckbox.addEventListener('click', function() {
        if (this.checked) {
            pharmacyCheckbox.checked = false;
        }
    });
});

// authentication/js/notification.js
document.addEventListener('DOMContentLoaded', function() {
    const notificationIcon = document.getElementById('notification-icon');
    const notificationPopup = document.getElementById('notification-popup');
    const closePopupBtn = document.getElementById('close-popup');
    const popupBackdrop = document.getElementById('popup-backdrop');
    const mainContent = document.getElementById('main-content'); // Ensure this ID exists in your HTML
    const viewAllBtn = document.getElementById('view-all-btn');

    function showPopup() {
        popupBackdrop.style.display = 'block'; // Ensure popupBackdrop is displayed
        setTimeout(() => {
            notificationPopup.classList.add('show');
            popupBackdrop.classList.add('show');
            mainContent.classList.add('blurred-background');
        }, 10); // Small delay to ensure the display property is set
    }

    function hidePopup() {
        notificationPopup.classList.remove('show');
        popupBackdrop.classList.remove('show');
        mainContent.classList.remove('blurred-background');
        setTimeout(() => {
            popupBackdrop.style.display = 'none';
        }, 300); // Match the transition duration
    }

    if (notificationIcon) {
        notificationIcon.addEventListener('click', showPopup);
    }

    if (closePopupBtn) {
        closePopupBtn.addEventListener('click', hidePopup);
    }

    if (popupBackdrop) {
        popupBackdrop.addEventListener('transitionend', function(event) {
            if (!popupBackdrop.classList.contains('show')) {
                popupBackdrop.style.display = 'none';
            }
        });

        window.addEventListener('click', function(event) {
            if (event.target === popupBackdrop) {
                hidePopup();
            }
        });
    }

    if (viewAllBtn) {
        viewAllBtn.addEventListener('click', function() {
            window.location.href = "/all_notification/";
        });
    }
});
