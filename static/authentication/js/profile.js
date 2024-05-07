document.addEventListener("DOMContentLoaded", () => {
  const unique_id = document.getElementById("unique_id");
  const unique_id_span = document.querySelector(".left-bottom-unique-id span");

  // Check if the unique_id value contains specific strings
  if (unique_id.value.includes("####") || unique_id.value.includes("####") || unique_id.value.includes("####")) {
    unique_id_span.style.backgroundColor = "red";
  } else {
    unique_id_span.style.backgroundColor = "green";
  }

  document.getElementById("admin-input").addEventListener("keypress", function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission
        // Call the function to send the request here
        sendRequest();
    }
});

document.getElementById("admin-input").addEventListener("input", function() {
  document.getElementById("send-request-button").addEventListener("input", function(event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent default form submission
      // Call the function to send the request here
      sendRequest();
  }
  })
});

document.getElementById("send-request-button").addEventListener("click", function() {
  sendRequest();
});

function sendRequest() {
  var adminName = document.getElementById("admin-input").value;

  // Get the CSRF token from the form
  var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  fetch("/profile/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken  // Include the CSRF token in the headers
      },
      body: JSON.stringify({ adminName: adminName })
  })
  .then(response => response.json())
  .then(data => {
      // Update the response container with the received data
      let displayMessage = document.getElementById("response-container");
      console.log(data);
      if (data.error){
          console.log("Error Message : ", data.error.message, data.error.adminName);
          displayMessage.textContent = data.error.message + ' ' +`"${data.error.adminName}"`;
          displayMessage.style.color = "red";
      }
      if (data.message){
          console.log("Message : ", data.message);
          displayMessage.textContent = data.message + ' ' + `"${data.adminName}"`;
          displayMessage.style.color = "green";
      }

      setTimeout(function(){
        displayMessage.style.display = "None"
      },3000)
  })
  .catch(error => console.error("Error:", error));
}


});

// for submit button
$(function() {
    $( "#button" ).click(function() {
      $( "#button" ).addClass( "onclic", 250, validate);
    });
  
    function validate() {
      setTimeout(function() {
        $( "#button" ).removeClass( "onclic" );
        $( "#button" ).addClass( "validate", 450, callback );
      }, 2250 );
    }
      function callback() {
        setTimeout(function() {
          $( "#button" ).removeClass( "validate" );
        }, 1250 );
      }
});


// for state dropdowns
$(document).ready(function() {
    $('#id_state').select2({
        placeholder: "Select a State",
        allowClear: true
    });
});

// for district dropdowns
$(document).ready(function() {
    $('#id_district').select2({
        placeholder: "Select a district",
        allowClear: true
    });
});


