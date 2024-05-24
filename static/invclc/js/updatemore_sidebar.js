function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var updatemore = document.querySelector('.checkmore-container');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        updatemore.style.marginLeft = '120px'; // Adjust this value according to your sidebar width
        updatemore.style.width = 'calc(100% - 120px)';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        updatemore.style.marginLeft = '10px';
        updatemore.style.width = 'calc(100% - 10px)';
    }
}