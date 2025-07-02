document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('https://feedbacksystemt-production.up.railway.app/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',  // Include cookies for session support if needed
            body: JSON.stringify({
                email: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token);
            alert('Login successful!');
            window.location.href = '/dashboard.html'; // Or any page after login
        } else {
            alert(data.message || 'Invalid login credentials.');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again later.');
    }
});

// Helper to auto-fill demo accounts
function fillLogin(username, password) {
    document.getElementById('username').value = username;
    document.getElementById('password').value = password;
}
