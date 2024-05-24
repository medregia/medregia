function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var mainContainer = document.querySelector('.main-container');
   

    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        mainContainer.style.marginLeft = '120px'; // Adjust this value according to your sidebar width
        mainContainer.style.width = 'calc(100% - 120px)';
       
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        mainContainer.style.marginLeft = '20px';
        mainContainer.style.width = 'calc(100% - 20px)';
        
    }
}
