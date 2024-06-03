document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('submit_button');
    
    sendBtn.addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        const sendForm = document.getElementById('add_user');
        const sendFormData = new FormData(sendForm);
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
        const mailStatus = document.querySelector(".mail-status");

        mailStatus.textContent = "Mail Sending Be Patient ...";
        mailStatus.style.color = "green";

        const data = {
            username: sendFormData.get('user_name'),
            useremail: sendFormData.get('user_email'),
            userphone: sendFormData.get('phone_number'),
            userposition: sendFormData.get('position'),
        };

        for (const [key, value] of Object.entries(data)) {
            if (!value) {
                mailStatus.textContent = `${key.replace('_', ' ')} cannot be empty.`;
                mailStatus.style.color = "red";
                return; 
            }
        }

        try {
            const response = await fetch('/adminacess/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFTOKEN": csrfToken,
                },
                body: JSON.stringify(data),
            });

            mailStatus.textContent = "";
            mailStatus.style.color = ""; // Reset the color
            
            if (response.ok) {
                console.log("Success");
                location.reload();
            } else {
                console.log("Failed");
                const errorData = await response.json();
                console.error('Error:', errorData);
                mailStatus.textContent = "Mail sending failed. Please try again.";
                mailStatus.style.color = "red";
            }
        } catch (error) {
            console.warn(error);
            mailStatus.textContent = "An error occurred. Please try again.";
            mailStatus.style.color = "red";
        }
    });
});

document.getElementById('copy_button').addEventListener('click', function() {
    const input = document.getElementById('id_Whatsapp_link');
    const whatsappStatus = document.querySelector(".mail-status");
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
    // else {
    //     document.execCommand('copy');
    //     alert('Link copied: ' + input.value);
    // }
});