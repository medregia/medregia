document.addEventListener("DOMContentLoaded", function () {
    // Get the table header checkbox
    const headerCheckbox = document.querySelector('thead input[type="checkbox"]');

    // Get all the table body checkboxes
    const bodyCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]');

    // Add an event listener to the header checkbox
    if (headerCheckbox){
        headerCheckbox.addEventListener("change", function () {
        // Loop through each body checkbox and set its checked property
        bodyCheckboxes.forEach(function (checkbox) {
            checkbox.checked = headerCheckbox.checked;
        });
    });
    }

    const csvBtn = document.querySelector('.csvBtn');
    csvBtn.addEventListener('click', function () {
        printSelectedRows();
    });

    function printSelectedRows() {
        const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
        const selectedRows = [];

        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                const row = checkbox.closest('tr');
                const rowData = {
                    pharmacyName: row.querySelector('td:nth-child(2)').textContent.trim(),
                    agencyName: row.querySelector('td:nth-child(3)').textContent.trim(),
                    invoiceNumber: row.querySelector('td:nth-child(4)').textContent.trim(),
                    invoiceDate: row.querySelector('td:nth-child(5)').textContent.trim(),
                    invoiceAmount: parseCurrency(row.querySelector('td:nth-child(6)').textContent),
                    duePay: parseCurrency(row.querySelector('td:nth-child(7)').textContent),
                    balance: parseCurrency(row.querySelector('td:nth-child(8)').textContent)
                };
                selectedRows.push(rowData);
            }
        });

        if (selectedRows.length > 0) {
            downloadCSV(selectedRows);
        } else {
            alert('No rows selected. Please select at least one row.');
        }
    }

    function downloadCSV(data) {
        const headers = ['Pharmacy Name', 'Agency Name', 'Invoice Number', 'Invoice Date', 'Invoice Amount', 'Due Pay', 'Balance'];
        const csvContent = [
            headers.join(','),
            ...data.map((row) => Object.values(row).map(value => `"${value}"`).join(',')),
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'Check-Record.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    function parseCurrency(value) {
        // Regular expression to match currency symbols and non-numeric characters
        const regex = /[^\d.]+/g;
        // Remove unwanted characters except dots and convert the string to a floating-point number
        return parseFloat(value.replace(regex, '').trim());
    }
});
