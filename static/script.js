const loginSection = document.getElementById('login-section');
const authorizedMenu = document.getElementById('authorized-menu');
const logoutButton = document.getElementById('logout-btn');
const welcomeMessage = document.getElementById('welcome-message');

if (localStorage.getItem('isLoggedIn') === 'true') {
    if (loginSection) loginSection.style.display = 'none';
    if (authorizedMenu) authorizedMenu.style.display = 'block';
    
    const savedUser = localStorage.getItem('userName');
    if (welcomeMessage && savedUser) {
        welcomeMessage.innerText = ` Welcome Back, ${savedUser}!`;
    }
}

if (logoutButton) {
    logoutButton.addEventListener('click', function() {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userName');
        window.location.reload(); 
    });
}

const sessionName = localStorage.getItem('userName');
const autoNameInputs = document.querySelectorAll('.auto-client-name');

if (sessionName && autoNameInputs.length > 0) {
    autoNameInputs.forEach(input => {
        input.value = sessionName; 
    });
}

// --- Dynamic Dashboard URL Parameter Injection ---
// Resolves authorization boundaries by appending identity to dashboard requests
const dashboardLinks = document.querySelectorAll('.dashboard-link');
if (sessionName && dashboardLinks.length > 0) {
    dashboardLinks.forEach(link => {
        link.href = `/dashboard?user=${encodeURIComponent(sessionName)}`;
    });
}


// --- Client-Side Validation: Prevent Booking Past Dates ---
const today = new Date().toISOString().split('T')[0];

// Apply to search form in rooms.html
const searchDateInput = document.querySelector('input[name="date"]');
if (searchDateInput) {
    searchDateInput.setAttribute('min', today);
}

// Apply to all update forms in dashboard.html
const updateDateInputs = document.querySelectorAll('.future-date-only');
if (updateDateInputs.length > 0) {
    updateDateInputs.forEach(input => {
        input.setAttribute('min', today);
    });
}