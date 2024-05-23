function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var checkmore = document.querySelector('.checkmore-container');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        checkmore.style.marginLeft = '120px'; // Adjust this value according to your sidebar width
        checkmore.style.width = 'calc(100% - 120px)';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        checkmore.style.marginLeft = '10px';
        checkmore.style.width = 'calc(100% - 10px)';
    }
}
