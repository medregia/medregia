function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var unpaid = document.querySelector('.unpaid-container');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        unpaid.style.marginLeft = '120px'; // Adjust this value according to your sidebar width
        unpaid.style.width = 'calc(100% - 120px)';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        unpaid.style.marginLeft = '10px';
        unpaid.style.width = 'calc(100% - 10px)';
    }
}