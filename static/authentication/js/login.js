document.addEventListener("DOMContentLoaded", () => {
    const disable = document.querySelector(".disable");
    const alertElement = document.querySelector(".alert-danger");
  
    if(disable && alertElement){
      disable.addEventListener("click", ()=>{
        alertElement.classList.add("hide");
      });
  
      alertElement.classList.remove("hide");
    }
  });