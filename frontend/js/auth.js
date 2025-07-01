// Authentication handling for frontend
function fillLogin(username, password) {
    document.getElementById('username').value = username;
    document.getElementById('password').value = password;
}

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // For frontend demo, we'll just show an alert
    // In a real application, this would make an API call to the backend
    alert(`Demo login attempt for ${username}. In a real app, this would authenticate with the backend.`);
});