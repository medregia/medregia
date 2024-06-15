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

    function toggleEditIcon(icon) {
        const row = icon.closest('tr');
        const type = icon.getAttribute('data-type');
        const input = row.querySelector(`td:nth-child(${type === 'dl_number1' ? 3 : 4}) input`);
        if (icon.classList.contains('edit-icon')) {
            input.removeAttribute('disabled');
            icon.innerHTML = '&#10003;';
            icon.classList.remove('edit-icon');
            icon.classList.add('save-icon');
        } else if (icon.classList.contains('save-icon')) {
            input.setAttribute('disabled', true);
            icon.innerHTML = '&#9998;';
            icon.classList.remove('save-icon');
            icon.classList.add('edit-icon');

            const dl_number1 = row.querySelector('td:nth-child(3) input').value;
            const dl_number2 = row.querySelector('td:nth-child(4) input').value;

            const button = row.querySelector('.inviteUser');
            const statusIcon = row.querySelector('.icon.disabled');
            if (dl_number1 && dl_number2) {
                button.removeAttribute('disabled');
                if (statusIcon) {
                    statusIcon.innerHTML = '&#10003;';
                    statusIcon.classList.remove('disabled');
                }
            } else {
                button.setAttribute('disabled', true);
                if (statusIcon) {
                    statusIcon.innerHTML = '&#10060;';
                    statusIcon.classList.add('disabled');
                }
            }
        }
    }

    document.querySelectorAll('.edit-icon, .save-icon').forEach(icon => {
        icon.addEventListener('click', function () {
            toggleEditIcon(icon);
        });
    });

    document.querySelectorAll('.inviteUser').forEach(button => {
        button.addEventListener('click', function () {
            const row = button.closest('tr');
            const name = row.querySelector('td:nth-child(2) input').value;
            const dl_number1 = row.querySelector('td:nth-child(3) input').value;
            const dl_number2 = row.querySelector('td:nth-child(4) input').value;
            const uniqueNumber = row.querySelector('td:nth-child(7) input').value;

            const data = {
                name: name,
                dl_number1: dl_number1,
                dl_number2: dl_number2,
                unique_number: uniqueNumber
            };

            fetch('/connect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Data : ",data)
                console.log("Data Data : ",data.data)
                console.log("status : ",data.status)
                if (data.status === 404 && data.data) {
                    showModal(data.message, true, data.data);
                } else {
                    showModal(data.message, false);
                }
            })
            .catch((error) => {
                showModal('Error: ' + error.message, false);
            });
        });
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

    function showModal(message, showButtons, data) {
        const modal = document.getElementById('myModal');
        const modalMessage = document.getElementById('modal-message');
        const modalOkButton = document.getElementById('modal-ok-button');
        const modalCancelButton = document.getElementById('modal-cancel-button');

        modalMessage.textContent = message;
        modal.style.display = "block";

        if (showButtons) {
            modalOkButton.style.display = "inline-block";
            modalCancelButton.style.display = "inline-block";

            modalOkButton.onclick = function() {
                createNewMedicalRecord(data);
                modal.style.display = "none";
            };

            modalCancelButton.onclick = function() {
                modal.style.display = "none";
                showModal('Collaboration request failed.', false);
            };
        } else {
            modalOkButton.style.display = "none";
            modalCancelButton.style.display = "none";
        }
    }

    document.querySelector('.close').onclick = function() {
        const modal = document.getElementById('myModal');
        modal.style.display = "none";
    }

    document.getElementById('modal-ok-button').onclick = function() {
        const modal = document.getElementById('myModal');
        modal.style.display = "none";
    }

    document.getElementById('modal-cancel-button').onclick = function() {
        const modal = document.getElementById('myModal');
        modal.style.display = "none";
        showModal('Collaboration request failed.', false);
    }

});

