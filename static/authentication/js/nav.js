document.addEventListener("DOMContentLoaded", function() {
  const notify = document.querySelector(".notifications");
  const bell_icon = document.querySelector("#bell");
  const menu = document.querySelector('.menu div')
  const navLinks = document.querySelector('.nav-links')
  const userPic = document.querySelector('.user-pic')
  const profileContent = document.querySelector('.profile-content')
  // Check if bell_icon exists before adding event listener
  if (bell_icon) {
    bell_icon.addEventListener("click", () => {
      notify.classList.remove("hide");
    });
  }

  // Check if notify exists before adding event listener
  if (notify) {
    document.addEventListener("click", (event) => {
      if (!notify.contains(event.target) && event.target !== bell_icon) {
        notify.classList.add("hide");
      }
    });
  }

  const admin = document.getElementById("admin_action");

  // Check if admin exists before adding event listener
  if (admin) {
    admin.addEventListener('submit', function() {
      admin.classList.add('hide');  // hides the form when it's submitted
    });
  }

  navLinks.classList.add('showmenu')
  menu.addEventListener('click',()=>{
    navLinks.classList.toggle('showmenu')
    userPic.classList.toggle('showmenu')
    profileContent.textContent = "Profile"
  })
});
