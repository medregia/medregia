// document.addEventListener('DOMContentLoaded', () => {
//     const openPopupButtons = document.querySelectorAll('.openPopup');
//     const closePopup = document.getElementById('closePopup');
//     const popup = document.getElementById('popup');
//     const sendBtn = document.getElementById('submit_button');
//     const mailStatus = document.querySelector(".mail-status");
//     const whatsappLink = document.getElementById('id_Whatsapp_link');

//     openPopupButtons.forEach(button => {
//         button.addEventListener('click', () => {
//             popup.style.display = 'block';
//         });
//     });

//     closePopup.addEventListener('click', () => {
//         popup.style.display = 'none';
//         whatsappLink.value = ""
//         location.reload()
//     });

//     sendBtn.addEventListener('click', async function(event) {
//         event.preventDefault(); // Prevent the default form submission
        
//         const sendForm = document.getElementById('add_user');
//         const sendFormData = new FormData(sendForm);
//         const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

//         mailStatus.textContent = "Generating Link ...";
//         mailStatus.style.color = "green";

//         const data = {
//             username: sendFormData.get('user_name'),
//             useremail: sendFormData.get('user_email'),
//             userphone: sendFormData.get('phone_number'),
//         };

//         for (const [key, value] of Object.entries(data)) {
//             if (!value) {
//                 mailStatus.textContent = `${key.replace('_', ' ')} cannot be empty.`;
//                 mailStatus.style.color = "red";
//                 return; 
//             }
//         }

//         try {
//             const response = await fetch('/adminacess/', {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFTOKEN": csrfToken,
//                 },
//                 body: JSON.stringify(data),
//             });

//             mailStatus.textContent = "";
//             mailStatus.style.color = ""; // Reset the color
            
//             if (response.ok) {
//                 const responseData = await response.json();
//                 whatsappLink.value = responseData.invite_link;
//                 console.log("Success");
//                 console.log("Response: ", responseData);
//             } else {
//                 console.log("Failed");
//                 const errorData = await response.json();
//                 console.error('Error:', errorData);
//                 mailStatus.textContent = "Mail sending failed. Please try again.";
//                 mailStatus.style.color = "red";
//             }
//         } catch (error) {
//             console.warn(error);
//             mailStatus.textContent = "An error occurred. Please try again.";
//             mailStatus.style.color = "red";
//         }
//     });
// });



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



    const inviteUsers = document.querySelectorAll('.inviteUser');
    inviteUsers.forEach(inviteUser => {
        inviteUser.addEventListener('click', () => {
            alert("We will update it soon");
        });
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
});

