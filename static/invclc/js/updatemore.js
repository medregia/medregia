document.addEventListener('DOMContentLoaded', function () {
  const editButtons = document.querySelectorAll('.editBtn');
  const saveButtons = document.querySelectorAll('.saveBtn');
  const cancelButtons = document.querySelectorAll('.cancelBtn');
  const deleteButtons = document.querySelectorAll('.deleteBtn');

  editButtons.forEach((editBtn, index) => {
    editBtn.addEventListener('click', function () {
      const row = this.closest('tr');
      const inputFields = row.querySelectorAll('input');

      inputFields.forEach(input => {
        input.removeAttribute('disabled');
        input.classList.add('border-active');
      });

      editBtn.style.display = 'none';
      saveButtons[index].style.display = 'inline-block';
      cancelButtons[index].style.display = 'inline-block';
      if (deleteButtons[index]) {
        deleteButtons[index].style.display = 'none';
      }
    });

    //TODO: POSTING a Data For Update using Featch  Save
    saveButtons[index].addEventListener('click', function () {
      const row = this.closest('tr');
      const inputFields = row.querySelectorAll('input');
      const invoiceId = row.dataset.invoiceId;
      const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

      const dataToUpdate = {};
      inputFields.forEach(input => {
        input.setAttribute('disabled', 'true');
        input.classList.remove('border-active');
        dataToUpdate[input.name] = input.value;
      });

      fetch(`/update_invoice/${invoiceId}/`, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
           'X-CSRFToken': csrfToken,
         },
         body: JSON.stringify(dataToUpdate),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Row updated successfully:', data);
      })
      .catch(error => {
      console.error('Error updating row:', error);
      });


      editBtn.style.display = 'inline-block';
      saveButtons[index].style.display = 'none';
      cancelButtons[index].style.display = 'none';
      if (deleteButtons[index]) {
        deleteButtons[index].style.display = 'inline-block';
      }
    });

    cancelButtons[index].addEventListener('click', function (event) {
      event.preventDefault();

      const row = this.closest('tr');
      const inputFields = row.querySelectorAll('input');

      inputFields.forEach(input => {
        input.setAttribute('disabled', 'true');
        input.classList.remove('border-active');
      });

      editBtn.style.display = 'inline-block';
      saveButtons[index].style.display = 'none';
      cancelButtons[index].style.display = 'none';
      if (deleteButtons[index]) {
        deleteButtons[index].style.display = 'inline-block';
      }
    });

    //TODO: Fetch for Deleting 

    if (deleteButtons[index]) {
      deleteButtons[index].addEventListener('click', function () {
        const row = this.closest('tr');
        const invoiceId = row.dataset.invoiceId;
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        fetch(`/delete_invoice/${invoiceId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': csrfToken,
          },
        })
          .then(response => response.json())
          .then(data => {
            row.remove();
            console.log('Row deleted successfully:', data);
          })
          .catch(error => {
            console.error('Error deleting row:', error);
          });
      });
    }
  });
});

// checkbox script//
document.addEventListener("DOMContentLoaded", function () {
  // Get the table header checkbox
  const headerCheckbox = document.querySelector('thead input[type="checkbox"]');

  // Get all the table body checkboxes
  const bodyCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]');

  // Add an event listener to the header checkbox
  headerCheckbox.addEventListener("change", function () {
    // Loop through each body checkbox and set its checked property
    bodyCheckboxes.forEach(function (checkbox) {
      checkbox.checked = headerCheckbox.checked;
    });
  });
});


//  csv button script//
document.addEventListener('DOMContentLoaded', function () {
  const csvBtn = document.querySelector('.csvBtn');
  csvBtn.addEventListener('click', function () {
    printSelectedRows();
  });

  function printSelectedRows() {
    const checkboxes = document.querySelectorAll('.checkmoreTable tbody input[type="checkbox"]');
    const selectedRows = [];

    checkboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        const row = checkbox.closest('tr');
        const rowData = {
          pharmacyName: row.querySelector('[name="pharmacy_name"]').value,
          invoiceAmount: row.querySelector('[name="invoice_amount"]').value,
          invoiceDate: row.querySelector('[name="invoice_date"]').value,
          balanceAmount: row.querySelector('[name="balance_amount"]').value,
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
    const headers = ['Pharmacy Name', 'Invoice Amount', 'Invoice Date', 'Balance Amount'];
    const csvContent = [
      headers.join(','),
      ...data.map((row) => Object.values(row).map(value => `"${value}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'Updated-Record.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
});
