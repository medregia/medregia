document.addEventListener('DOMContentLoaded', () => {
    const phoneloginData = document.getElementById('phonelogin_form');
    const loginBtn = document.querySelector('.loginbtn');
    const error_message = document.getElementById('error_message')

    loginBtn.addEventListener('click', (e) => {
        e.preventDefault();

        const formData = new FormData(phoneloginData);
        const data = {
            phone_num: formData.get('phone_num'),
            pin: formData.get('pin')
        };
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/phone_login/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                window.location.href = '/index/';
            }
            else {
                // console.error("Error: ", data.error);
                error_message.textContent=data.error
                error_message.style.color = "red"
                // alert(data.error);
            }
        })
        .catch(err => {
            console.error("Error: ", err);
        });
    });
});
