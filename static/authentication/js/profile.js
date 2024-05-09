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
        else if (data.message){ // Changed this to 'else if'
            console.log("Message : ", data.message);
            displayMessage.textContent = data.message + ' ' + `"${data.adminName}"`;
            displayMessage.style.color = "green";
        }

        setTimeout(function(){
            displayMessage.textContent = ""; // Clear the message after 3 seconds
        }, 3000);
    })
    .catch(error => console.error("Error:", error));
}

fetch('/get-states/') // Endpoint to retrieve states data
    .then(response => response.json())
    .then(states => {
        const stateDropdown = document.getElementById('state-dropdown');
        states.forEach(state => {
            const option = document.createElement('option');
            option.value = state.Pid; // Assuming Pid is the ID field
            option.text = state.Pname;
            stateDropdown.appendChild(option);
        });
    });

// Event listener for state selection
document.getElementById('state-dropdown').addEventListener('change', function() {
    const stateId = this.value;
    fetch(`/get-districts/?state=${stateId}`) // Endpoint to retrieve districts based on state
    .then(response => response.json())
    .then(districts => {
        const districtDropdown = document.getElementById('district-dropdown');
        districtDropdown.innerHTML = '<option value="">Select District</option>'; // Clear previous options
        districts.forEach(district => {
            const option = document.createElement('option');
            option.value = district.Pid; // Assuming Pid is the ID field
            option.text = district.districtname;
            option.id = district.id; // Set the ID for each option
            districtDropdown.appendChild(option);
        });
    }); 
});


let districtId = ''

document.getElementById('district-dropdown').addEventListener('change', function() {
    const selectedIndex = this.selectedIndex; // Get the index of the selected option
    const selectedOption = this.options[selectedIndex]; // Get the selected option
    districtId = selectedOption.id; // Retrieve the ID attribute of the selected option
    // Now you can use districtId in your logic, such as passing it to another endpoint or performing any other action you need
    // For example, you can fetch data based on the selected district ID
});

// Add an event listener to the button
document.getElementById('submit_button').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    // Get form data
    const formData = {};

    const medicalShopNameElement = document.getElementById('id_MedicalShopName');
    const ProprietaryNameElement = document.getElementById('id_ProprietaryName');
    const ProprietaryNumberElement = document.getElementById('id_ProprietaryNumber');
    const ProprietaryContactElement = document.getElementById('id_ProprietaryContact');
    const DrugLiceneseNumber2Element = document.getElementById('id_DrugLiceneseNumber2');
    const DrugLiceneseNumber1Element = document.getElementById('id_DrugLiceneseNumber1');
    const stateElement = document.getElementById('state-dropdown');
    const districtElement = document.getElementById('district-dropdown');
    const CityElement = document.getElementById('id_City');
    const PincodeElement = document.getElementById('id_Pincode');
    const StreetNumberElement = document.getElementById('id_StreetNumber');
    const DoorNumberElement = document.getElementById('id_DoorNumber');
    const PharmacistNameElement = document.getElementById('id_PharmacistName');
    const RegisteredNumberElement = document.getElementById('id_RegisteredNumber');
    const ContactNumberElement = document.getElementById('id_ContactNumber');

    if (medicalShopNameElement) {
        formData.MedicalShopName = medicalShopNameElement.value;
    }
    if (ProprietaryNameElement) {
        formData.ProprietaryName = ProprietaryNameElement.value;
    }
    if (ProprietaryNumberElement) {
        formData.ProprietaryNumber = ProprietaryNumberElement.value;
    }
    if (ProprietaryContactElement) {
        formData.ProprietaryContact = ProprietaryContactElement.value;
    }
    if (DrugLiceneseNumber2Element) {
        formData.DrugLiceneseNumber2 = DrugLiceneseNumber2Element.value;
    }
    if (DrugLiceneseNumber1Element) {
        formData.DrugLiceneseNumber1 = DrugLiceneseNumber1Element.value;
    }
    if (stateElement) {
        formData.state = stateElement.value;
    }
    if (districtElement) {
        formData.district = districtElement.value;
    }
    if (CityElement) {
        formData.City = CityElement.value;
    }
    if (PincodeElement) {
        formData.Pincode = PincodeElement.value;
    }
    if (StreetNumberElement) {
        formData.StreetNumber = StreetNumberElement.value;
    }
    if (DoorNumberElement) {
        formData.DoorNumber = DoorNumberElement.value;
    }
    if (PharmacistNameElement) {
        formData.PharmacistName = PharmacistNameElement.value;
    }
    if (RegisteredNumberElement) {
        formData.RegisteredNumber = RegisteredNumberElement.value;
    }
    if (ContactNumberElement) {
        formData.ContactNumber = ContactNumberElement.value;
    }

    // Get CSRF token from the page
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!districtId) {
        // Set default districtId here
        // For example, you can set it to the first option's id
        districtId = ''
    }
    // Send data to Django backend
    sendingData(formData, csrfToken, districtId);
    
});


function sendingData(formData, csrf, districtId) {
        formData.districtkey = districtId
        fetch('/profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Profile not Saved with Error');
            }
            return response.json();
        })
        .then(data => {
            // Handle response from backend if needed
            console.log(data);
            alert(" Profile Saved Successfully ... ")
            window.location.reload()
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
            alert(error)
            window.location.reload()
        });
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


