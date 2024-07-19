function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var staticcontent = document.getElementById('staticcontent');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        staticcontent.style.marginLeft = '150px'; // Adjust this value according to your sidebar width
        staticcontent.style.width = '89%';
        // mainContent.style.transition = '0.3s';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        staticcontent.style.marginLeft = '50px';
        staticcontent.style.width = '96%';
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const notificationIcon = document.getElementById('notification-icon');
    const notificationPopup = document.getElementById('notification-popup');
    const closePopupBtn = document.getElementById('close-popup');
    const popupBackdrop = document.getElementById('popup-backdrop');
    const mainContent = document.querySelector('.main-content'); // Add a class to your main content container
    const viewAllBtn = document.getElementById('view-all-btn'); // Get the View All button

    notificationIcon.addEventListener('click', function() {
        notificationPopup.classList.add('show');
        popupBackdrop.classList.add('show');
        mainContent.classList.add('blurred-background');
    });

    closePopupBtn.addEventListener('click', function() {
        notificationPopup.classList.remove('show');
        popupBackdrop.classList.remove('show');
        mainContent.classList.remove('blurred-background');
        
        setTimeout(() => {
            popupBackdrop.style.display = 'none';
        }, 300); // Match the transition duration
    });

    popupBackdrop.addEventListener('transitionend', function(event) {
        if (!popupBackdrop.classList.contains('show')) {
            popupBackdrop.style.display = 'none';
        }
    });

    window.addEventListener('click', function(event) {
        if (event.target == popupBackdrop) {
            notificationPopup.classList.remove('show');
            popupBackdrop.classList.remove('show');
            mainContent.classList.remove('blurred-background');
            
            setTimeout(() => {
                popupBackdrop.style.display = 'none';
            }, 300); // Match the transition duration
        }
    });

    // Add event listener for View All button
    viewAllBtn.addEventListener('click', function() {
        window.location.href =  "/all_notification/"; // Replace "view_all_page" with the actual URL or URL name
    });
});
