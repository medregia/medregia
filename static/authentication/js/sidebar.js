function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.getElementById('mainContent');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        mainContent.style.marginLeft = '170px'; // Adjust this value according to your sidebar width
        mainContent.style.width = '85%';
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        mainContent.style.marginLeft = '70px';
        mainContent.style.width = '94%';
    }
}