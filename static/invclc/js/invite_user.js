document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('user-details-form');
    const inviteBtn = document.getElementById('invite_userBtn');
  
    const pinField = form.querySelector('input[name="new_userpin"]');
    pinField.addEventListener('input', function() {
        if (pinField.value.length > 4) {
            pinField.value = pinField.value.slice(0, 4); // Limit PIN to 4 digits
        }
    });
  
    inviteBtn.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
  
        // Clear previous error messages
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
  
        // Get input values
        const phoneNumber = form.querySelector('input[name="new_userphonenumber"]').value;
        const password = form.querySelector('input[name="new_userpassword"]').value;
        const confirmPassword = form.querySelector('input[name="new_userconfirmpassword"]').value;
        const pin = form.querySelector('input[name="new_userpin"]').value;
        const position = form.querySelector('input[name="new_userposition"]').value;
  
        // Validate phone number
        if (phoneNumber.length > 10) {
            document.getElementById('new_userphonenumber-error').textContent = 'Phone number cannot exceed 10 digits.';
            return;
        }
  
        // Validate password match
        if (password !== confirmPassword) {
            document.getElementById('new_userconfirmpassword-error').textContent = 'Passwords do not match. Please try again.';
            return;
        }
  
        // Validate password strength
        const passwordValidation = validatePasswordStrength(password);
        if (!passwordValidation.isValid) {
            document.getElementById('new_userpassword-error').textContent = `Password is not strong enough. Suggestions: ${passwordValidation.suggestions.join(', ')}`;
            return;
        }
  
        // Validate PIN length
        if (pin.length !== 4) {
            document.getElementById('new_userpin-error').textContent = 'PIN must be exactly 4 digits.';
            return;
        }
  
        // Enable all disabled form fields before collecting data
        const disabledFields = form.querySelectorAll('input:disabled');
        disabledFields.forEach(field => field.disabled = false);
  
        // Collect form data
        const formData = new FormData(form);
        
        // Convert formData to JSON
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
  
        // Send data to the server
        fetch('/invite/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value // Ensure CSRF token is sent
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Getting a Data : ",data)
            if (data.status === 'error') {
                // Display the error message below the respective field
                const errorField = document.getElementById(`${data.field}-error`);
                if (errorField) {
                    errorField.textContent = data.message;
                }
                 else {
                    // Handle unexpected error fields
                    console.error(`Error field ${data.field}-error not found`);
                    console.log(data.message)
                    alert(`An error occurred: ${data.message}`);
                }
            } else if (data.status === 'success') {
                // Redirect on success
                window.location.href = data.redirect_url;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred: ' + error.message);
        })
        .finally(() => {
            // Re-disable the fields after data is collected
            disabledFields.forEach(field => field.disabled = true);
        });
    });
});


  
    function validatePasswordStrength(password) {
        const suggestions = [];
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const isLongEnough = password.length >= 8;
  
        if (!hasUpperCase) suggestions.push('Add an uppercase letter');
        if (!hasLowerCase) suggestions.push('Add a lowercase letter');
        if (!hasNumbers) suggestions.push('Add a number');
        if (!isLongEnough) suggestions.push('Make it at least 8 characters long');
  
        const isValid = hasUpperCase && hasLowerCase && hasNumbers && isLongEnough;
        return { isValid, suggestions };
    }
  
  function toggleEdit(fieldId) {
    const inputField = document.getElementById(fieldId);
    const icon = inputField.nextElementSibling;
  
    if (inputField.disabled) {
      inputField.disabled = false;
      inputField.focus();
      icon.innerHTML = '&#10004;'; // OK icon
    } else {
      inputField.disabled = true;
      icon.innerHTML = '&#9998;'; // Pencil icon
      // Here you would typically send the updated data to the server via an AJAX request
      // For now, just log the updated value
      console.log(`${fieldId} updated to:`, inputField.value);
    }
  }
  
  function toggleOtherTypeField() {
    const userType = document.getElementById('usertype').value;
    const otherTypeGroup = document.getElementById('other-type-group');
  
    if (userType === 'others') {
      otherTypeGroup.style.display = 'block';
    } else {
      otherTypeGroup.style.display = 'none';
    }
  }
  
  

// // Populate the inviter's name dynamically
// document.getElementById('inviter-name').textContent = new URLSearchParams(window.location.search).get('sendername') || 'Sender Name';

// function preventBack() {
//   history.pushState(null, null, location.href);
//   window.addEventListener('popstate', function () {
//     history.pushState(null, null, location.href);
//   });
// }

// function preventBack() {
//   // Push the current URL to the history stack
//   history.pushState(null, null, location.href);

//   window.addEventListener('popstate', function () {
//     // Redirect to the specific URL when the back button is pressed
//     window.location.href = "https://medregia.com/login/";
//   });
// }



// history.pushState() is a method that allows you to add a new entry to the browser's session history stack.
// The method takes three arguments: state, title, and url.
// state: An object associated with the new history entry (in this case, null).
// title: A string representing the title of the new history entry (not used here, so it's null).
// url: The new URL for the history entry (here, location.href, which is the current URL).
// window.onload = preventBack;
