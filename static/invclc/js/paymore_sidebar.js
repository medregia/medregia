function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var paymore = document.querySelector('.paymore-container');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        paymore.style.marginLeft = '120px'; // Adjust this value according to your sidebar width
        paymore.style.width = 'calc(100% - 120px)';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        paymore.style.marginLeft = '10px';
        paymore.style.width = 'calc(100% - 10px)';
    }
}