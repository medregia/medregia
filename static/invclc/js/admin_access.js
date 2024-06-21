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


    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const popup = document.getElementById('message-popup');
    const sendBtn = document.getElementById('send-btn');
    const abortBtn = document.getElementById('abort-btn');
    const form = document.getElementById('popup-form');
    const headerMessage = document.querySelector('.message-header');

    const medicalNameInput = document.getElementById('medicalname');
    const uniquenoInput = document.getElementById('uniqueno');

    let currentRow = null;
    
    function handleInviteUserClick(event) {
        const row = event.target.closest('tr');
        const MedicalName = row.querySelector('td:nth-child(2) input').value;
        const dlNumber1 = row.querySelector('td:nth-child(3) input').value;
        const dlNumber2 = row.querySelector('td:nth-child(4) input').value;
        const unique_number = row.querySelector('td:nth-child(7) input').value;

        medicalNameInput.value = MedicalName;
        uniquenoInput.value = unique_number;
    
        const data = { 
            medicalName: MedicalName,
            dl1: dlNumber1,
            dl2: dlNumber2,
            UniqueNo: unique_number
        };
    
        sendData('/connect/', data);
    }


    function sendData(url, data) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            MessageforUsers(data);
            form.reset();
            currentRow = null;
        })
        .catch(error => {
            error.json().then(errData => {
                popupmain(error.status, errData, errData.Inputpopup); //status , errorDataObject,popup(True or False)
            });
        });
    }
    
    function attachInviteUserEventListeners() {
        document.querySelectorAll('.inviteUser').forEach(button => {
            button.addEventListener('click', handleInviteUserClick);
        });
    }
    
    // Initialize event listeners when the script loads
    attachInviteUserEventListeners();
    
    function sendBtnClicked(){
        sendBtn.addEventListener('click', () => {
            const dl1 = form.querySelector('#dl1').value;
            const dl2 = form.querySelector('#dl2').value;
            const medicalName = form.querySelector('#medicalname').value;
            const UniqueNo = form.querySelector('#uniqueno').value;
            
            console.log("dl1:", dl1);
            console.log("dl2:", dl2);
            console.log("medicalName:", medicalName);
            console.log("UniqueNo:", UniqueNo);
        
            if (dl1 && dl2) {
                const data = {
                    medicalName: medicalName,
                    dl1: dl1, 
                    dl2: dl2, 
                    UniqueNo: UniqueNo,
                };
                sendData('/connect/', data);
            } else {
                alert('Please enter both DL numbers.');
            }
        });
    }
    
    
    abortBtn.addEventListener('click', () => {
        popup.style.display = 'none';
        form.reset();
        currentRow = null;
        location.reload();
    });
    
    function createNewMedicalRecord(data) {
        console.log("Create Record:", data);
        fetch('/create_medical/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        })
        .then(data => {
            console.info(data);
            MessageforUsers(data);
        })
        .catch(error => {
            error.json().then(errData => {
                console.error(errData);
                MessageforUsers(errData);
            });
        });
    }
    
    function normalPopupMessage(status,data) {
        console.log("Normal Popup:", data);
        console.log("Normal Popup status :", status);
        const registerContainer = document.querySelector(".register-medicals");
        const registerh3 = document.querySelector(".register-medicals h3");
        const registerSaveBtn = document.getElementById("saverecord");
        const registerAbortBtn = document.getElementById("abortrecord");
    
        popup.style.display = 'block';
        headerMessage.textContent = data.message;
        form.style.display = 'none';
    
        registerContainer.style.display = "block";
        registerh3.textContent = data.message;
    
        registerSaveBtn.addEventListener('click', () => {
            popup.style.display = 'none';
    
            registerContainer.style.display = "none";
            createNewMedicalRecord(data.data);
        });
    
        registerAbortBtn.addEventListener('click', () => {
            popup.style.display = 'none';
            location.reload();
        });
    }
    
    function displayPopupMessage(status, data) {
        console.error('Error:', data.message);
        console.log('Status Code:', status);

        popup.style.display = 'block';
        headerMessage.textContent = data.message;
        
        sendBtnClicked()
        
    }
    
    function popupmain(status, data, popup) {
        console.log("Popup Main");
        console.log("status:", status);
        console.log("data:", data);
        console.log("popup:", popup);
    
        if (status === 400 && popup) {
            console.log("Inside");
            displayPopupMessage(status, data);
        } else if (status === 404 && popup) {
            normalPopupMessage(status,data)
        }
        
    }
    
    function MessageforUsers(message) {
        console.log(message);
        console.log(message.message);
    
        const messageContainer = document.querySelector(".message-content");
        const messageContainerh3 = document.querySelector(".message-content h3");
        const messageContainerBtn = document.getElementById("ok_btn");
    
        popup.style.display = 'block';
        form.style.display = 'none';
        headerMessage.textContent = message.message;
        messageContainer.style.display = "block";
        messageContainerh3.textContent = message.message;
    
        messageContainerBtn.addEventListener('click', () => {
            popup.style.display = 'none';
            location.reload();
        });
    }
    
    
});



// .then(data => {
//     popup.style.display = 'block';
//     headerMessage.textContent = errData.message;
//     registerContainer.style.display = 'block';
//     registerh3.textContent = errData.message

//     console.log(data);
//     registerSaveBtn.addEventListener('click',()=>{
//         createNewMedicalRecord(data)
//     })
//     // popup.style.display = 'none';
//     registerAbortBtn.addEventListener('click',()=>{
//         popup.style.display = 'none';
//         form.reset();
//         currentRow = null;
//         location.reload();
//     })
//     form.reset();
//     currentRow = null;
// })
// .catch(error =>{
//     console.log("Error: ", error);
//     error.json().then(errData =>{
//         console.log(errData)
//     })
// })