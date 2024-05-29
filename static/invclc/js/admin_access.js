document.addEventListener('DOMContentLoaded',()=>{
    const sendBtn = document.getElementById('submit_button')
    sendBtn.addEventListener('click',async function(){
        const sendForm = document.getElementById('add_user')
        const sendFormData = new FormData(sendForm)
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;


        const data = {
            username:sendFormData.get('user_name'),
            useremail:sendFormData.get('user_email'),
            userphone:sendFormData.get('phone_number'),
            userposition:sendFormData.get('position'),
        }

        try{
            const dataResponse = await fetch('/adminacess/',{
                method:"POST",
                headers: {
                    "Content-Type":"application/json",
                    "X-CSRFTOKEN":csrfToken,
                },
                body:JSON.stringify(data)
                
            });
            console.log("data : ",data)

            if(dataResponse.ok){
                console.log("Success")
            }
            else{
                console.log("Failed")
            }
        }
        catch(error){
            console.warn(error);
        }

    })
})