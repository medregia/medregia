document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add_btn');
    const whatsappLink = document.getElementById('id_Whatsapp_link');
    const messages = document.querySelector('.alert-message');

    messages.textContent = "";
    addBtn.addEventListener('click', async (e) => {
        e.preventDefault();

        const addUserForm = document.getElementById('add_userForm');
        const form_data = new FormData(addUserForm);
        const data = Object.fromEntries(form_data.entries());
        const fields = document.querySelectorAll(".input-field");

        messages.textContent = "Generating a Link ";
        messages.style.color = "green";
        messages.classList.remove('alert-success', 'alert-error', 'shake');

        for (const [key, value] of Object.entries(data)) {
            if (!value) {
                messages.textContent = `${key.replace('_', ' ')} cannot be empty.`;
                messages.style.color = "red";
                return;
            }
        }

        try {
            const response = await fetch('/adminacess/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFTOKEN": data.csrfmiddlewaretoken,
                },
                body: JSON.stringify(data),
            });

            messages.textContent = "";
            messages.style.color = ""; // Reset the color

            if (response.ok) {
                const responseData = await response.json();
                whatsappLink.value = responseData.invite_link;
                messages.textContent = "Link Generated "
                messages.classList.add('alert-success');
                messages.classList.remove('shake');

                console.info("Success");
                // console.log("Response: ", responseData);
            } else {
                console.error("Failed");
                const errorData = await response.json();
                // console.error('Error:', errorData);
                messages.textContent = `Mail sending failed. Please try again. ${errorData.error.message}`;
                messages.classList.add('alert-error', 'shake');
                messages.classList.remove('alert-success');
            }
        } catch (error) {
            console.error(error);
            messages.textContent = `An error occurred. Please try again ${error}`;
            messages.classList.add('alert-error', 'shake');
            messages.classList.remove('alert-success');
        }
    });

    document.getElementById('copy_button').addEventListener('click', function() {
    const input = document.getElementById('id_Whatsapp_link');
    const whatsappStatus = document.querySelector(".alert-message");
    input.select();
    input.setSelectionRange(0, 99999); // For mobile devices

    // Check if the navigator clipboard API is supported
    whatsappStatus.textContent="";
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(input.value).then(() => {

            whatsappStatus.textContent=`Link Copied`
            whatsappStatus.style.color="green";
        }).catch(err => {
            alert('Failed to copy: ', err);
            whatsappStatus.textContent=`Link Not Copied`
            whatsappStatus.style.color="red";
        });
    } 
    else {
        document.execCommand('copy');
        alert('Link copied: ');
    }
    });

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const popup = document.getElementById('message-popup');
    const sendBtn = document.getElementById('send-btn');
    const abortBtn = document.getElementById('abort-btn');
    const form = document.getElementById('popup-form');
    const headerMessage = document.querySelector('.message-header');

    let currentRow = null;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


    document.querySelectorAll('.inviteUser').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log("Clicked")
            const row = event.target.closest('tr');
            const MedicalName = row.querySelector('td:nth-child(2) input').value;
            const dlNumber1 = row.querySelector('td:nth-child(3) input').value;
            const dlNumber2 = row.querySelector('td:nth-child(4) input').value;
            const unique_number = row.querySelector('td:nth-child(7) input').value;

            const medicalInput = document.getElementById('medicalname')
            const UniqueInput = document.getElementById('uniqueno')


            if (dlNumber1 === 'None' || dlNumber2 === 'None') {
                currentRow = row;
                popup.style.display = 'block';
                headerMessage.textContent = MedicalName;
                medicalInput.value = MedicalName;
                UniqueInput.value = unique_number;

            } else {
                Data = 
                fetch('/connect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ medicalName:MedicalName,dl1:dlNumber1, dl2:dlNumber2 ,UniqueNo:unique_number})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                popup.style.display = 'none';
                form.reset();
                currentRow = null;
            })
            .catch(error => {
                console.error('Error:', error);
            });

            }
        });
    });

    sendBtn.addEventListener('click', () => {
        const dl1 = form.querySelector('#dl1').value;
        const dl2 = form.querySelector('#dl2').value;
        const medicalName = form.querySelector('#medicalname').value;
        const UniqueNo = form.querySelector('#uniqueno').value

        if (dl1 && dl2) {
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch('/connect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ medicalName,dl1, dl2 ,UniqueNo})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                popup.style.display = 'none';
                form.reset();
                currentRow = null;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            alert('Please enter both DL numbers.');
        }
    });

    abortBtn.addEventListener('click', () => {
        popup.style.display = 'none';

        form.reset();
        currentRow = null;
        location.reload()
    });


    
    function createNewMedicalRecord(data) {
        fetch('/create_medical/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            showModal('Records are saved successfully.', false);
        })
        .catch((error) => {
            showModal('Error: ' + error.message, false);
        });
    }

});

