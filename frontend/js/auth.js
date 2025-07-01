document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('https://your-railway-app.up.railway.app/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
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
