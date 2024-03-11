document.addEventListener('DOMContentLoaded', function () {
  const paymentTableBody = document.getElementById('paymentTableBody');
//   const headerMessages = document.querySelector('.header-messages');

  paymentTableBody.addEventListener('click', function (event) {
    const target = event.target;
    const row = target.closest('tr');

    if (target.classList.contains('payBtn')) {
      const paymentField = row.querySelector('input[name="payment_amount"]');
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
      });

      // Add an event listener to the save/pay button
      target.addEventListener('click', function () {
        const invoiceId = row.getAttribute('data-invoice-id');
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
        .then(response => response.json())
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
        });
      });
    }
  });
});
