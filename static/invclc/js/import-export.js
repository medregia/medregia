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
    } else if (selectedOption === "table2") {
      document.getElementById("table1").style.display = "none";
      document.getElementById("table2").style.display = "block";
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