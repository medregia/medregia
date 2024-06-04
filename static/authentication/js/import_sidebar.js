function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    // var medregiaHeader = document.getElementById('medregiaHeader');
    var imp_exp_content = document.getElementById('imp_exp_content');
    
    if (sidebar.classList.contains('sidebar-closed')) {
        sidebar.classList.remove('sidebar-closed');
        sidebar.classList.add('sidebar-open');
        imp_exp_content.style.marginLeft = '150px'; // Adjust this value according to your sidebar width
        imp_exp_content.style.width = '89%';
        // mainContent.style.transition = '0.3s';
        
    } else {
        sidebar.classList.remove('sidebar-open');
        sidebar.classList.add('sidebar-closed');
        imp_exp_content.style.marginLeft = '50px';
        imp_exp_content.style.width = '96%';
    }
}