document.addEventListener("DOMContentLoaded", function() {
    
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (isLoggedIn === 'true') {
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('authorized-menu').classList.remove('hidden-section');

        const userSection = document.getElementById('navbar-user-section');
        if (userSection) {
            userSection.style.display = 'flex';
            userSection.classList.remove('hidden-section');
        }

        const userName = localStorage.getItem('userName');
        if (userName) {
            document.querySelector('.user-greeting').innerText = "Welcome, " + userName + "!";
        }
    }




    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.onclick = function() {
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('userName');
            window.location.reload(); 
        };
    }
});    
