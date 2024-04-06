function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var medregiaHeader = document.getElementById('medregiaHeader');
    var mainContent = document.getElementById('mainContent');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        medregiaHeader.style.display = 'block';
        medregiaHeader.style.opacity = '1'; // Show slowly
        medregiaHeader.style.transition = 'opacity 1s';
        mainContent.style.marginLeft = '170px'; // Adjust this value according to your sidebar width
        mainContent.style.width = '85%';
        mainContent.style.transition = '1s';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        medregiaHeader.style.display = 'none';
        medregiaHeader.style.opacity = '0'; // Hide slowly
        medregiaHeader.style.transition = 'opacity 1s';
        mainContent.style.marginLeft = '70px';
        mainContent.style.width = '94%';
    }
}