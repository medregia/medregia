function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var medregiaHeader = document.getElementById('medregiaHeader');
    var imp_exp_content = document.getElementById('imp_exp_content');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        medregiaHeader.style.display = 'block';
        medregiaHeader.style.opacity = '1'; // Show slowly
        medregiaHeader.style.transition = 'opacity 1s';
        imp_exp_content.style.marginLeft = '150px'; // Adjust this value according to your sidebar width
        imp_exp_content.style.width = '89%';
        // mainContent.style.transition = '0.3s';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        medregiaHeader.style.display = 'none';
        medregiaHeader.style.opacity = '0'; // Hide slowly
        medregiaHeader.style.transition = 'opacity 1s';
        imp_exp_content.style.marginLeft = '50px';
        imp_exp_content.style.width = '96%';
    }
}