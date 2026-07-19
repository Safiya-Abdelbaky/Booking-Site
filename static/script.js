// 1. Get user data from browser memory (Local Storage)
const sessionName = localStorage.getItem('userName');
const isLoggedIn = localStorage.getItem('isLoggedIn');

// 2. Control the view (Show/Hide elements based on login status)
const loginSection = document.getElementById('login-section');
const authorizedMenu = document.getElementById('authorized-menu');

// Navbar Elements
const navUserSection = document.getElementById('navbar-user-section');
const navGreeting = document.getElementById('nav-greeting');

if (isLoggedIn === 'true') {
    if (loginSection) {
        loginSection.style.display = 'none'; // Hide login form
    }
    if (authorizedMenu) {
        authorizedMenu.style.display = 'block'; // Show user menu (VIP Area)
    }
    
    // Show navbar user section and set greeting
    if (navUserSection) {
        navUserSection.style.display = 'flex'; 
    }
    if (navGreeting && sessionName) {
        navGreeting.innerText = `Welcome, ${sessionName}!`; 
    }
}

// 3. Logout function (Clear memory and refresh)
const logoutButton = document.getElementById('logout-btn');

if (logoutButton) {
    logoutButton.addEventListener('click', function() {
        localStorage.removeItem('isLoggedIn'); // Delete login status
        localStorage.removeItem('userName');   // Delete user name
        window.location.reload();              // Refresh the page
    });
}

// 4. Auto-fill the client name in booking forms
const autoNameInputs = document.querySelectorAll('.auto-client-name');

if (sessionName) {
    autoNameInputs.forEach(function(input) {
        input.value = sessionName; // Put the saved name inside the input
    });
}

// 5. Add user name to dashboard links
const dashboardLinks = document.querySelectorAll('.dashboard-link');

if (sessionName) {
    dashboardLinks.forEach(function(link) {
        link.href = `/dashboard?user=${encodeURIComponent(sessionName)}`; // Update URL
    });
}

// 6. Prevent users from selecting past dates
const today = new Date().toISOString().split('T')[0]; // Get today's date (YYYY-MM-DD)

// For the search form
const searchDateInput = document.querySelector('input[name="date"]');
if (searchDateInput) {
    searchDateInput.setAttribute('min', today); // Set minimum date
}

// For the update forms
const updateDateInputs = document.querySelectorAll('.future-date-only');
if (updateDateInputs) {
    updateDateInputs.forEach(function(input) {
        input.setAttribute('min', today); // Set minimum date
    });
}