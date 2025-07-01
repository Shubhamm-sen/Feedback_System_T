document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('https://your-railway-backend-url.com/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: username, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            // Login successful - store token if using JWT
            localStorage.setItem('token', data.token);  // Optional: only if using JWT
            alert('Login successful!');
            window.location.href = '/dashboard.html';  // or wherever you want to redirect
        } else {
            alert('Login failed: ' + (data.message || 'Invalid credentials'));
        }

    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again later.');
    }
});



// // Authentication handling for frontend
// function fillLogin(username, password) {
//     document.getElementById('username').value = username;
//     document.getElementById('password').value = password;
// }

// document.getElementById('loginForm').addEventListener('submit', function(e) {
//     e.preventDefault();
    
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;
    
//     // For frontend demo, we'll just show an alert
//     // In a real application, this would make an API call to the backend
//     alert(`Demo login attempt for ${username}. In a real app, this would authenticate with the backend.`);
// });
