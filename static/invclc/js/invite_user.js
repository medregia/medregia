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

// Populate the inviter's name dynamically
document.getElementById('inviter-name').textContent = new URLSearchParams(window.location.search).get('sendername') || 'Sender Name';

function preventBack() {
  history.pushState(null, null, location.href);
  window.addEventListener('popstate', function () {
    history.pushState(null, null, location.href);
  });
}

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
window.onload = preventBack;
