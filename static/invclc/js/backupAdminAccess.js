const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const popup = document.getElementById('message-popup');
    const sendBtn = document.getElementById('send-btn');
    const abortBtn = document.getElementById('abort-btn');
    const form = document.getElementById('popup-form');
    const headerMessage = document.querySelector('.message-header');

    const registerContainer = document.querySelector(".register-medicals");
    const registerh3 = document.querySelector(".register-medicals h3");
    const registerSaveBtn = document.getElementById("saverecord");
    const registerAbortBtn = document.getElementById("abortrecord");

    let currentRow = null;

    document.querySelectorAll('.inviteUser').forEach(button => {
        button.addEventListener('click', (event) => {
            const row = event.target.closest('tr');
            const MedicalName = row.querySelector('td:nth-child(2) input').value;
            const dlNumber1 = row.querySelector('td:nth-child(3) input').value;
            const dlNumber2 = row.querySelector('td:nth-child(4) input').value;
            const unique_number = row.querySelector('td:nth-child(7) input').value;

            const medicalInput = document.getElementById('medicalname');
            const UniqueInput = document.getElementById('uniqueno');

            fetch('/connect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ 
                    medicalName: MedicalName,
                    dl1: dlNumber1,
                    dl2: dlNumber2,
                    UniqueNo: unique_number
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw response;
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                normalPopupMessage(data)
                // popup.style.display = 'none';
                form.reset();
                currentRow = null;
            })
            .catch(error => {
                console.log("Error: ", error);
                error.json().then(errData => {
                    console.log("error : ",error);
                    console.log("errData : ",errData);
                    displayPopupMessage(error.status,errData);
                });
            });
        });
    });

    // popup.style.display = 'block';
    // form.style.display = 'none';
    // headerMessage.textContent = "NO Medical Name found in this name  Click Save Button to Save a New Record ";
    // registerContainer.style.display = 'block';
    // registerh3.textContent = "NO Medical Name found in this name  Click Save Button to Save a New Record"; 

    sendBtn.addEventListener('click', () => {
        const dl1 = form.querySelector('#dl1').value;
        const dl2 = form.querySelector('#dl2').value;
        const medicalName = form.querySelector('#medicalname').value;
        const UniqueNo = form.querySelector('#uniqueno').value;
        
        console.log("dl1 :",dl1)
        console.log("dl2 :",dl2)
        console.log("medicalName :",medicalName)
        console.log("UniqueNo :",UniqueNo)

        if (dl1 && dl2) {
            fetch('/connect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    medicalName:medicalName,
                    dl1:dl1, 
                    dl2:dl2, 
                    UniqueNo:UniqueNo,
                })
            })

            .then(response => {
                if (!response.ok) {
                    throw response;
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                normalPopupMessage(data);
                form.reset();
                currentRow = null;
            })
            .catch(error => {
                console.error('Error:', error);
                error.json().then(errData => {
                    normalPopupMessage(errData)
                })
            });
        } else {
            alert('Please enter both DL numbers.');
        }
    });

    abortBtn.addEventListener('click', () => {
        popup.style.display = 'none';
        form.reset();
        currentRow = null;
        location.reload();
    });

    function createNewMedicalRecord(data) {
        console.log("Create Record : ",data)
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
            console.info(data)
            normalPopupMessage(data)
        })
        .catch((error) => {
            error.json().then(errData => {
                console.error(errData)
                normalPopupMessage(errData);
            });
        });
    }

    function normalPopupMessage(data) {
        console.log("Normal Popup : ",data)
        const popupBodyMessage = document.querySelector('.message-content');
        const popupBodyh4 = document.querySelector('.message-content h3');
        const popupBodyCloseBtn = document.querySelector('.message-content button');

        popup.style.display = 'block';
        headerMessage.textContent = data.message;
        form.style.display = 'none';
        popupBodyMessage.style.display = "block";
        popupBodyh4.textContent = data.message;

        popupBodyCloseBtn.addEventListener('click',()=>{
            popup.style.display = 'none';
            location.reload();
        })
    }   


    function displayPopupMessage(status,message){
        if(status === 400){
            console.error('Error:', message.message);
            console.log('Status Code :',status);
            
            popup.style.display = 'block';
            headerMessage.textContent = message.message;
            const formcontent = document.getElementById('popup-form')
    
            const formData = new FormData(formcontent)
            const DataEntries = Object.entries(formData.entries)
            
            fetch('/connect/',({
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ 
                    DataEntries
                })
                .then(response => {
                    if (!response.ok) {
                        throw response;
                    }
                    return response.json();
                })
                .then(data => {
                   console.log("Display Popup Response : ",data)
                })
                .catch(error =>{
                    console.log("Error: ", error);
                    error.json().then(errData =>{
                        console.log("Display Popup Error : ",errData)
                    })
                })
    
            }))
            
        }

        else if(status === 404 && message.popup){
            popup.style.display = 'block';
            headerMessage.textContent = message.message;
            registerContainer.style.display = 'block';
            registerh3.textContent = message.message

            console.log(data);
            registerSaveBtn.addEventListener('click',()=>{
                createNewMedicalRecord(message)
            })
            // popup.style.display = 'none';
            registerAbortBtn.addEventListener('click',()=>{
                popup.style.display = 'none';
                form.reset();
                currentRow = null;
                location.reload();
            })
            form.reset();
            currentRow = null;  
        }
        else{
            normalPopupMessage(message)
        }
    }