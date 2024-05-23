document.addEventListener('DOMContentLoaded', function () {
  const paymentTableBody = document.getElementById('payTableBody');
//   const headerMessages = document.querySelector('.header-messages');

  paymentTableBody.addEventListener('click', function (event) {
    const target = event.target;

    // Check if the clicked element is a pay button
    if (target.classList.contains('payBtn')) {
      const row = target.closest('tr');
      const paymentField = row.querySelector('input[name="pmnt_amount"]');
      const cancelBtn = row.querySelector('.cancelBtn');

      // Enable the payment field for editing
      paymentField.removeAttribute('disabled');
      paymentField.classList.add('border-active');

      // Show the cancel button
      cancelBtn.style.display = 'inline-block';

      // Change the text content of the pay button to 'Save'
      target.textContent = 'Save';

      // Add an event listener to the cancel button
      cancelBtn.addEventListener('click', function () {
        // Reset changes on cancel
        paymentField.setAttribute('disabled', 'true');
        paymentField.classList.remove('border-active');
        cancelBtn.style.display = 'none';

        // Change the text content of the pay button back to 'Pay'
        target.textContent = 'Pay';

        // Reload the page on cancel
        location.reload();
      });

      // Add an event listener to the save/pay button
      target.addEventListener('click', function () {
        if (target.textContent === 'Save') {
          const invoiceId = target.getAttribute('data-pay-id');
          const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

          // Extract only the payment data for updating
          const paymentData = {
            payment_amount: paymentField.value,
          };

          fetch(`/payment_invoice/${invoiceId}/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(paymentData),
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            console.log('Payment updated successfully:', data);
            
            // Update the payment field with the returned data
            paymentField.value = data.payment_amount;

            // Reset the button text to 'Pay'
            target.textContent = 'Pay';

            // Reset the cancel button and payment field
            cancelBtn.style.display = 'none';
            paymentField.setAttribute('disabled', 'true');
            paymentField.classList.remove('border-active');

            // Reload the page on successful save
            location.reload();
          })
          .catch(error => {
            console.error('Error updating payment:', error);
            location.reload();
          });
        }
      });
    }
  });
});


document.addEventListener("DOMContentLoaded", function () {
  // Get the table header checkbox
  const headerCheckbox = document.querySelector('.unpaidmoretable thead input[type="checkbox"]');

  // Get all the table body checkboxes
  const bodyCheckboxes = document.querySelectorAll('.unpaidmoretable tbody input[type="checkbox"]');

  // Add an event listener to the header checkbox
  headerCheckbox.addEventListener("change", function () {
    // Loop through each body checkbox and set its checked property
    bodyCheckboxes.forEach(function (checkbox) {
      checkbox.checked = headerCheckbox.checked;
    });
  });
});



document.addEventListener('DOMContentLoaded', function () {
  const csvBtn = document.querySelector('.csvBtn');
  csvBtn.addEventListener('click', function () {
    printSelectedRows();
  });

  function printSelectedRows() {
    const checkboxes = document.querySelectorAll('.unpaidmoretable tbody input[type="checkbox"]');
    const selectedRows = [];

    checkboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        const row = checkbox.closest('tr');
        const rowData = {
          pharmacyName: row.querySelector('[name="phmy_name"]').value,
          invoiceAmount: row.querySelector('[name="iv_amount"]').value,
          balanceAmount: row.querySelector('[name="bal_amount"]').value,
          paidAmount: row.querySelector('[name="pmnt_amount"]').value,
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
    const headers = ['Pharmacy Name', 'Invoice Amount', 'Balance Amount', 'Paid Amount'];
    const csvContent = [
      headers.join(','),
      ...data.map((row) => Object.values(row).map(value => `"${value}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'Payment-Dept.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
});
