document.addEventListener("DOMContentLoaded", function() {
  const notify = document.querySelector(".notifications");
  const bell_icon = document.querySelector("#bell")

  const admin = document.getElementById("admin_action");


  bell_icon.addEventListener("click", () => {
    notify.classList.remove("hide");
  });

  document.addEventListener("click", (event) => {
    if (!notify.contains(event.target) && event.target !== bell_icon) {
      notify.classList.add("hide");
    }
  });

  admin.addEventListener('submit', function() {
    admin.classList.add('hide');  // hides the form when it's submitted
  });
});



