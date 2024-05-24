window.onload = function () {
  var activeTab = document.querySelector(".tablinks.active");
  if (activeTab) {
    activeTab.click();
  }
};

// TODO: Partially Payment Dynamicaly Changing
const paymentRows = document.querySelectorAll("#paymentTableBody tr");
paymentRows.forEach(row => {
  const partiallyBalance = row.querySelector(".partiallyBalance");
  const partiallyPayment = row.querySelector(".partiallyPayment");
  const initialBalance = partiallyBalance.value;

  partiallyPayment.addEventListener("input", function() {
    let balance = Number(initialBalance);
    let payment = Number(this.value);

    let newBalance = balance - payment;

    partiallyBalance.value = newBalance >= 0 ? newBalance : 'Amount Exceeds';
  });

  partiallyPayment.addEventListener("change", function() {
    if (this.value.trim() === "") {
      partiallyBalance.value = initialBalance;
    }
  });
});

// TODO: Payment List Dynamically Change

const payRows = document.querySelectorAll("#payTableBody tr");
payRows.forEach(row => {
  const balanceAmount = row.querySelector(".bal_amount");
  const paymentAmount = row.querySelector(".pmnt_amount");
  const initial_Balance = balanceAmount.value;

  paymentAmount.addEventListener("input", function() {
    let pendingBalance = Number(initial_Balance);
    let payPayment = Number(this.value);

    let createdBalance = pendingBalance - payPayment;

    balanceAmount.value = createdBalance >= 0 ? createdBalance : 'Amount Exceeds';
  });

  paymentAmount.addEventListener("change", function() {
    if (this.value.trim() === "") {
      balanceAmount.value = initial_Balance;
    }
  });
});

// TODO: Uptade Dynamically Change

const updateRows = document.querySelectorAll("#updatePaymentTable tr");
updateRows.forEach(row => {
  const  updateBalance = row.querySelector(".updateBalance");
  const  updatePay = row.querySelector(".updatePay");
  const updatePayment = row.querySelector(".updatePayment");
  const initialUpdate= updatePay.value;

  updatePayment.addEventListener("input", function() {
    let updatingPay = Number(initialUpdate);
    let payingPayment = Number(this.value);

    let changingTotal = payingPayment - updatingPay;

    updateBalance.value = changingTotal >= 0 ? changingTotal : 'Amount Exceeds';
  });

  updatePayment.addEventListener("change", function() {
    if (this.value.trim() === "") {
      updateBalance.value = initialUpdate;
    }
  });
});

function openpanel(evt, panels) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    tabcontent[i].style.backgroundColor="#EEF3F5";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    tablinks[i].style.backgroundColor = "#fff";
  }
  var panel = document.getElementById(panels);
  if (panel) {
    panel.style.display = "inline-flex";
  }
  if (evt.currentTarget.className.indexOf("active") === -1) {
    evt.currentTarget.className += " active";
    evt.currentTarget.style.backgroundColor = "#EEF3F5";
  }
  else {
    evt.currentTarget.style.backgroundColor = "#fff"; 
    // Set background color to white if the element is not active
  }

  const invoice_amount = document.querySelector(".invoice_amount");
  const payment_amount = document.querySelector(".payment_amount");
  const balance_amount = document.querySelector(".balance_amount");

  invoice_amount.addEventListener("input", calculate);
  payment_amount.addEventListener("input", calculate);

  function calculate() {
    let invoice = Number(invoice_amount.value);
    let payment = Number(payment_amount.value);
    let balance = invoice - payment;

    if (balance < 0) {
      balance_amount.value = "Amount Not Valid";
      balance_amount.style.backgroundColor = "red";
      balance_amount.style.color = "#FFFF";
    } else if (
      Number(invoice_amount.value) !== 0 &&
      Number(payment_amount.value) !== 0 &&
      Number(invoice_amount.value) == Number(payment_amount.value)
    ) {
      balance_amount.value = "Paying Full Amount ";
      balance_amount.style.backgroundColor = "green";
      balance_amount.style.color = "#FFFF";
    } else {
      balance_amount.value =` ₹ ${balance}`;
      balance_amount.style.backgroundColor = "#d3d3d3";
      balance_amount.style.color = "black";
    }
  }
}

//TODO: Pannel For Update 

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
      let headerMessage = document.querySelector('.header-messages');

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
        headerMessage.textContent = "Successfully Updated"
        location.reload()
      })
      .catch(error => {
      console.error('Error updating row:', error);
      headerMessage.textContent = `Updation Failed`
      headerMessage.style.color = "red"
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
        let headerMessage = document.querySelector('.header-messages');
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        fetch(`/delete_invoice/${invoiceId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': csrfToken,
          },
        })
          .then(response => response.json())
          .then(data => {
            location.reload()
            row.remove();
            console.log('Row deleted successfully:', data);
            headerMessage.textContent = "Row Deleted Successfully "
          })
          .catch(error => {
            console.error('Error deleting row:', error);
            headerMessage.textContent = "Row Not Deleted "
            headerMessage.style.color = "red"
          });
      });
    }
  });


});

// TODO:  Partially Paid Pannel

document.addEventListener('DOMContentLoaded', function () {
  const paymentTableBody = document.getElementById('paymentTableBody');
  const payButtons = paymentTableBody.querySelectorAll('.payBtn');
  const cancelButtons = paymentTableBody.querySelectorAll('.cancelBtn');
  const headerMessages = document.querySelector('.header-messages');

  payButtons.forEach((payBtn, index) => {
    const row = payBtn.closest('tr');
    const cancelBtn = row.querySelector('.cancelBtn');
    const inputFields = row.querySelectorAll('input');

    payBtn.addEventListener('click', function () {

      if (payBtn.textContent === 'Save') {
        const invoiceId = row.dataset.invoiceId;
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        // Extract only the payment data for updating
        const paymentField = row.querySelector('input[name="payment_amount"]');
        const paymentData = {
          payment_amount: paymentField.value,
        };

        fetch(`/pay_invoice/${invoiceId}/`, {
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
          headerMessages.textContent = "Payment Processed Successfully .."

          // Update the payment field with the returned data
          paymentField.value = data.payment_amount;

          payBtn.textContent = 'Pay';
          cancelBtn.style.display = 'none'; // Hide cancel button after saving
          inputFields.forEach(input => {
            input.setAttribute('disabled', 'true'); 
            input.classList.remove('border-active');
          });

          // Reload the page after successful payment
          location.reload();
          
        })
        .catch(error => {
          console.error('Error updating row:', error);
          headerMessages.textContent = "Payment Failed .."
          headerMessages.style.color = "red"
          payBtn.textContent = 'Save'; // Handle error scenario, if needed
          location.reload();
        });
      } else {
        cancelBtn.style.display = 'inline-block';

        // Enable only the payment field for editing
        const paymentField = row.querySelector('input[name="payment_amount"]');
        paymentField.removeAttribute('disabled');
        paymentField.classList.add('border-active');

        // Disable other input fields
        inputFields.forEach(input => {
          if (input !== paymentField) {
            input.setAttribute('disabled', 'true');
            input.classList.remove('border-active');
          }
          else
            input.value = '';
            input.focus();
        });

        payBtn.textContent = 'Save';
      }
    });
  });

  cancelButtons.forEach(cancelBtn => {
    cancelBtn.addEventListener('click', function () {
      this.style.display = 'none';

      const row = this.closest('tr');
      const inputFields = row.querySelectorAll('input');

      inputFields.forEach(input => {
        input.setAttribute('disabled', 'true');
        input.classList.remove('border-active');
      });

      const payBtn = row.querySelector('.payBtn');
      payBtn.textContent = 'Pay';
      // Refresh the table by reloading the page
      location.reload();
    });
  });
});



//TODO: Payment List Finall Panel
document.addEventListener('DOMContentLoaded', function () {
  const paymentTableBody = document.getElementById('payTableBody');
  const headerMessages = document.querySelector('.header-messages');

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
            let paymentMessage = paymentData.payment_amount
            headerMessages.textContent = `$ ${paymentMessage} Paied Successfully `

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
            headerMessages.style.color = "red"
            headerMessages.textContent = `Paied Failed : Check Your Payment Amount `
            location.reload();
          });
        }
      });
    }
  });
});
document.addEventListener('DOMContentLoaded', function() {
  var invoiceDateInput = document.getElementById('id_invoice_date');

  if (invoiceDateInput){
    invoiceDateInput.addEventListener('input', function() {
      var formattedValue = this.value.replace(/[^\d\/]/g, ''); // Remove all characters except digits and slashes
      if (formattedValue.length > 10) {
          formattedValue = formattedValue.substr(0, 10); // Limit to 10 characters
      }
      if (formattedValue.length >= 2 && formattedValue.indexOf('/') === -1) {
          formattedValue = formattedValue.substr(0, 2) + '/' + formattedValue.substr(2);
      }
      if (formattedValue.length >= 5 && formattedValue.indexOf('/', 3) === -1) {
          formattedValue = formattedValue.substr(0, 5) + '/' + formattedValue.substr(5);
      }
      this.value = formattedValue;
  });
  }
  
  // Handle backspace and delete key events
  if (invoiceDateInput){
    invoiceDateInput.addEventListener('keydown', function(event) {
      if (event.key === 'Backspace' || event.key === 'Delete') {
          var caretStart = this.selectionStart;
          var caretEnd = this.selectionEnd;
          var value = this.value;
          if (caretStart === caretEnd) {
              if (event.key === 'Backspace' && value.charAt(caretStart - 1) === '/') {
                  this.value = value.slice(0, caretStart - 1) + value.slice(caretStart);
                  event.preventDefault();
              } else if (event.key === 'Delete' && value.charAt(caretStart) === '/') {
                  this.value = value.slice(0, caretStart) + value.slice(caretStart + 1);
                  event.preventDefault();
              }
          }
      }
    });
  }
  
});


document.getElementById('saveButton').addEventListener('click', async function() {
  const form = document.getElementById('invoiceForm');
  const formData = new FormData(form);
  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
  const messages = document.querySelector('#header-message');

  if (messages.classList.contains('error-message')) {
      messages.classList.remove('error-message');
  }

  if (messages.classList.contains('header-message')) {
      messages.classList.remove('header-message');
  }

  const data = {
      pharmacy_name: formData.get('pharmacy_name'),
      invoice_number: formData.get('invoice_number'),
      invoice_date: formData.get('invoice_date'),
      invoice_amount: formData.get('invoice_amount'),
      payment_amount: formData.get('payment_amount'),
  };

  // Check if any field is empty
  for (const [key, value] of Object.entries(data)) {
      if (!value) { // Check for null, undefined, or empty string
          alert(`${key.replace('_', ' ')} cannot be empty.`);
          return; // Stop the function if any field is empty
      }
  }

  try {
      const response = await fetch('/index/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
          console.log(result);
          messages.textContent = result.message;
          messages.classList.add('header-message');
          location.reload();
      } else {
          console.error('Error:', result);
          messages.textContent = result.message;
          messages.classList.add('error-message');
          location.reload();
      }
  } catch (error) {
      console.error('Error:', error);
      messages.textContent =' An error occurred. Please try again';
      messages.classList.add('error-message');
      location.reload();
  }
});



// function entryData() {
//   fetch('/entry/')
//       .then(response => {
//           if (!response.ok) {
//               throw new Error('Network response was not ok ' + response.statusText);
//           }
//           return response.json();
//       })
//       .then(data => {
//           const pharmacy_name = document.querySelector(".pharmacy_name");
//           const invoice_number = document.querySelector(".invoice_number");
//           const id_invoice_date = document.querySelector("#id_invoice_date");
//           const invoice_amount = document.querySelector(".invoice_amount");
//           const payment_amount = document.querySelector(".payment_amount");
//           const balance_amount = document.querySelector(".balance_amount");
//           // Disable or enable fields based on data.Entry value
//           const isEntryDisabled = data.Entry;
//           pharmacy_name.disabled = isEntryDisabled;
//           invoice_number.disabled = isEntryDisabled;
//           id_invoice_date.disabled = isEntryDisabled;
//           invoice_amount.disabled = isEntryDisabled;
//           payment_amount.disabled = isEntryDisabled;
//           balance_amount.disabled = isEntryDisabled;
//           // Add or remove .not-allowed class based on the disabled state
//           if (isEntryDisabled) {
//               pharmacy_name.classList.add('not-allowed');
//               invoice_number.classList.add('not-allowed');
//               id_invoice_date.classList.add('not-allowed');
//               invoice_amount.classList.add('not-allowed');
//               payment_amount.classList.add('not-allowed');
//               balance_amount.classList.add('not-allowed');
//               console.log("Entry is disabled.");
//           } else {
//               pharmacy_name.classList.remove('not-allowed');
//               invoice_number.classList.remove('not-allowed');
//               id_invoice_date.classList.remove('not-allowed');
//               invoice_amount.classList.remove('not-allowed');
//               payment_amount.classList.remove('not-allowed');
//               balance_amount.classList.remove('not-allowed');
              
//               console.log("Entry is enabled.");
//           }
//           console.log(data);
//       })
//       .catch(error => {
//           console.error('There was a problem with the fetch operation:', error);
//       });
// }

// Add event listeners to input fields
// const pharmacy_name = document.querySelector(".pharmacy_name");
// const invoice_number = document.querySelector(".invoice_number");
// const id_invoice_date = document.querySelector("#id_invoice_date");
// const invoice_amount = document.querySelector(".invoice_amount");
// const payment_amount = document.querySelector(".payment_amount");
// const balance_amount = document.querySelector(".balance_amount");

// pharmacy_name.addEventListener('click', entryData);
// invoice_number.addEventListener('click', entryData);
// id_invoice_date.addEventListener('click', entryData);
// invoice_amount.addEventListener('click', entryData);
// payment_amount.addEventListener('click', entryData);
// balance_amount.addEventListener('click', entryData