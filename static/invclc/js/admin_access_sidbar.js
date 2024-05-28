function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var adminaccess = document.querySelector('.admin-main-container');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        adminaccess.style.marginLeft = '120px'; // Adjust this value according to your sidebar width
        adminaccess.style.width = 'calc(100% - 120px)';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        adminaccess.style.marginLeft = '10px';
        adminaccess.style.width = 'calc(100% - 10px)';
    }
}