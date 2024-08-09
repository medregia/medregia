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

  // Remove error and header messages
  messages.classList.remove('error-message', 'header-message');

  // Gather form data
  const data = {
      pharmacy_name: formData.get('pharmacy_name'),
      dl_num1:formData.get('dlnum1'),
      dl_num2:formData.get('dlnum2'),
      invoice_number: formData.get('invoice_number'),
      invoice_date: formData.get('invoice_date'),
      invoice_amount: formData.get('invoice_amount'),
      payment_amount: formData.get('payment_amount'),
  };

  // Check if any field is empty
  for (const [key, value] of Object.entries(data)) {
      if (!value) {
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
      } else if (response.status === 404) {
          popup404(result);
      } else {
          console.error('Error:', result);
          togglePopup(data);
          messages.textContent = result.message;
          messages.style.color = "red";
          messages.classList.add('error-message');
      }
  } catch (error) {
      console.error('Error:', error);
      togglePopup(data);
      messages.textContent = 'An error occurred. Please try again';
      messages.classList.add('error-message');
  }
});

function popup404(message) {
  const medicalNotFound = document.getElementById('medicalnotfound');
  const contentPtag = document.querySelector('#content404 p');
  const overlay = document.querySelector('.hide-background');
  const acceptButton = document.getElementById('AcceptButton');

  if (medicalNotFound && contentPtag && overlay) {
      overlay.style.display = "block";
      medicalNotFound.style.display = "flex";
      contentPtag.innerHTML = `<span style="color:red">Note :</span> No Medical Found in this Name <span style="color:green">${message.message}</span>`;
  }

  acceptButton.addEventListener('click', (e) => {
      e.preventDefault();
      overlay.style.display = "none";
      medicalNotFound.style.display = "none";
      location.reload();
  });
}

function togglePopup(data) {
  const entryButton = document.getElementById('not_accessable_profile');
  const closeBtn = document.getElementById("popup-btn");
  const popupMsg = document.getElementById("popup-1");
  const popupMessages = document.querySelector(".overlay-content h2");
  const popupBody = document.querySelector(".overlay-content p");

  if (entryButton) {
      popupMessages.textContent = "Invoice Update Failed";
      popupMessages.style.color = "red";
      popupMsg.classList.add("active");

      closeBtn.addEventListener("click", async () => {
          const pharmacyName = document.getElementById('pharmacy_name').value;
          const dl1 = document.getElementById('dl1').value;
          const dl2 = document.getElementById('dl2').value;
          const csrf_token = document.querySelector("input[name='csrfmiddlewaretoken']").value;

          // Prepare data for the Django view
          const profileData = {
              pharmacy_name: pharmacyName,
              dl1: dl1,
              dl2: dl2,
              medicalName: data.pharmacy_name,
              invoice_number: data.invoice_number,
              invoice_date: data.invoice_date,
              invoice_amount: data.invoice_amount,
              payment_amount: data.payment_amount
          };

          try {
              const profileResponse = await fetch('/update_profile/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrf_token
                  },
                  body: JSON.stringify(profileData)
              });

              const profileResult = await profileResponse.json();
              if (profileResponse.ok) {
                  console.log(profileResult);
                  popupMsg.classList.remove("active");
                  location.reload();
              } else {
                  console.error('Profile Update Error:', profileResult);
                  popupMessages.textContent = "Profile Update Failed";
                  popupBody.classList.add('error-message');
                  popupBody.textContent = profileResult.message || "An error occurred while updating the profile.";
              }
          } catch (error) {
              console.error('Profile Update Error:', error);
              popupMessages.textContent = "Profile Update Failed";
              popupBody.classList.add('error-message');
              popupBody.textContent = "An error occurred while updating the profile.";
          }
      });
  } else {
      console.error('Entry button not found');
  }
}


//  Serach Result

document.addEventListener('DOMContentLoaded', () => {
  const searchMedicalName = document.getElementById('id_pharmacy_name');
  const dbData = document.getElementById('db_data');
  const resultsList = document.createElement('ul'); // Create a list for results

  if (dbData) {
    dbData.appendChild(resultsList); // Add the list to the dbData container
  }

  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

  if (searchMedicalName && dbData) {
    // Initially hide dbData
    dbData.classList.remove('show');
    dbData.classList.add('hide');

    searchMedicalName.addEventListener('input', (e) => {
      e.preventDefault();
      const query = searchMedicalName.value.trim(); // Get the input value and trim whitespace

      if (query === "") {
        dbData.classList.remove('show');
        dbData.classList.add('hide');
        resultsList.innerHTML = ''; // Clear previous results
      } else {
        // Show the dbData div and perform the search
        dbData.classList.add('show');
        dbData.classList.remove('hide');

        // Perform the search request
        fetch('/search/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ medicalNameSearch: query }),
        })
        .then(response => response.json())
        .then(data => {
          resultsList.innerHTML = ''; // Clear previous results
          if (data.message === 'Results Found' || data.message === "Medical name found, but DL numbers not found") {
            data.results.forEach(result => {
              const listItem = document.createElement('li');
              listItem.innerHTML = `
                <span style="font-weight: 700;">${result.medicals_name}</span>,
                <span style="font-weight: 300;">${result.dlnumber_1}</span>,
                <span style="font-weight: 300;">${result.dlnumber_2}</span>`;
              // Add data attributes to store the full result data
              listItem.dataset.medicalName = result.medicals_name;
              listItem.dataset.dlnumber1 = result.dlnumber_1;
              listItem.dataset.dlnumber2 = result.dlnumber_2;
              resultsList.appendChild(listItem);
            });
          } else {
            resultsList.innerHTML = `<li>${data.message}</li>`;
          }
        })
        .catch(err => {
          console.error(err);
        });
      }
    });

    // Handle clicks on result items
    resultsList.addEventListener('click', (e) => {
      const listItem = e.target.closest('li');
      if (listItem) {
        // Populate the input fields with data from the clicked item
        searchMedicalName.value = listItem.dataset.medicalName;
        document.getElementById('id_dlnum1').value = listItem.dataset.dlnumber1;
        document.getElementById('id_dlnum2').value = listItem.dataset.dlnumber2;
        // Uncomment and update if you need these fields
        // document.getElementById('id_invoice_number').value = listItem.dataset.invoiceNumber;
        // document.getElementById('id_invoice_date').value = listItem.dataset.invoiceDate;
        // document.getElementById('id_invoice_amount').value = listItem.dataset.invoiceAmount;
        // document.getElementById('id_payment_amount').value = listItem.dataset.paymentAmount;

        // Optionally hide the results div after selection
        dbData.classList.remove('show');
        dbData.classList.add('hide');
        resultsList.innerHTML = ''; // Clear results if needed
      }
    });

    document.addEventListener('click', (e) => {
      // Check if the click was outside of searchMedicalName and dbData
      if (!searchMedicalName.contains(e.target) && !dbData.contains(e.target)) {
        dbData.classList.remove('show');
        dbData.classList.add('hide');
      }
    });
  }
});





















// if(status === 404 && message.popup){
//   popup.style.display = 'block';
//   headerMessage.textContent = message.message;
//   registerContainer.style.display = 'block';
//   registerh3.textContent = message.message

//   console.log(data);
//   registerSaveBtn.addEventListener('click',()=>{
//       createNewMedicalRecord(message)
//   })
//   // popup.style.display = 'none';
//   registerAbortBtn.addEventListener('click',()=>{
//       popup.style.display = 'none';
//       form.reset();
//       currentRow = null;
//       location.reload();
//   })
//   form.reset();
//   currentRow = null;  
// }
// else{
//   normalPopupMessage(message)
// }

