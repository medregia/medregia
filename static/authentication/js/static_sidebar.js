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