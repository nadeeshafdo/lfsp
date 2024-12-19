const state = {
    isAuthenticated: false,
    currentUser: null,
    token: null
};

const sections = {
    login: document.getElementById('login-section'),
    register: document.getElementById('register-section'),
    fileManagement: document.getElementById('file-management-section'),
    publicFiles: document.getElementById('public-files-section')
};

const buttons = {
    loginSidebar: document.getElementById('btn-login-sidebar'),
    registerSidebar: document.getElementById('btn-register-sidebar'),
    filesSidebar: document.getElementById('btn-files-sidebar'),
    publicSidebar: document.getElementById('btn-public-sidebar')
};

const backendUrl = "http://localhost:8080/api"; // Replace with your backend URL

// Create a notification system
const NotificationManager = {
    container: document.getElementById('notification-container'),
    
    show: function(message, type = 'info', duration = 3000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.classList.add('notification');
        
        // Add type-specific class
        if (type === 'success') {
            notification.classList.add('success');
        } else if (type === 'error') {
            notification.classList.add('error');
        }
        
        // Create notification content
        const messageSpan = document.createElement('span');
        messageSpan.textContent = message;
        
        // Create close button
        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.classList.add('notification-close');
        closeButton.addEventListener('click', () => this.remove(notification));
        
        // Append elements
        notification.appendChild(messageSpan);
        notification.appendChild(closeButton);
        
        // Add to container
        this.container.appendChild(notification);
        
        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => this.remove(notification), duration);
        }
    },
    
    remove: function(notification) {
        notification.style.animation = 'slideOut 0.3s ease-out';
        notification.addEventListener('animationend', () => {
            notification.remove();
        });
    },
    
    success: function(message, duration = 3000) {
        this.show(message, 'success', duration);
    },
    
    error: function(message, duration = 3000) {
        this.show(message, 'error', duration);
    }
};

function hideAllSections() {
    Object.values(sections).forEach(section => section.classList.add('hidden'));
}

function showSection(section) {
    hideAllSections();
    section.classList.remove('hidden');
}

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value.trim();

    if (!username || !password) {
        NotificationManager.error('Please fill out all fields.');
        return;
    }

    try {
        const response = await fetch(`${backendUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            state.isAuthenticated = true;
            state.currentUser = username;
            state.token = data.token;
            NotificationManager.success('Login successful!');
            updateUIAfterLogin();
        } else if (response.status === 401) {
            NotificationManager.error('Invalid credentials. Please try again.');
        } else {
            NotificationManager.error('An error occurred while logging in. Please try again later.');
        }
    } catch (error) {
        console.error('Network error during login:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('register-username').value.trim();
    const password = document.getElementById('register-password').value.trim();
    const confirmPassword = document.getElementById('confirm-password').value.trim();

    if (!username || !password || !confirmPassword) {
        NotificationManager.error('Please fill out all fields.');
        return;
    }

    if (password !== confirmPassword) {
        NotificationManager.error('Passwords do not match.');
        return;
    }

    try {
        const response = await fetch(`${backendUrl}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            NotificationManager.success('Registration successful. You can now log in.');
            showSection(sections.login);
        } else if (response.status === 400) {
            const errorData = await response.json();
            NotificationManager.error(`Registration failed: ${errorData.message}`);
        } else {
            NotificationManager.error('An error occurred during registration. Please try again later.');
        }
    } catch (error) {
        console.error('Network error during registration:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

async function populateFileTable() {
    const tableBody = document.getElementById('file-table-body');
    tableBody.innerHTML = '';

    try {
        const response = await fetch(`${backendUrl}/files`, {
            headers: { Authorization: `Bearer ${state.token}` }
        });

        if (response.ok) {
            const files = await response.json();
            if (files.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="4">No files found.</td></tr>';
            } else {
                files.forEach(file => {
                    const row = tableBody.insertRow();
                    row.innerHTML = `
                        <td>${file.name}</td>
                        <td>${file.type}</td>
                        <td>${file.size}</td>
                        <td>
                            <button onclick="downloadFile('${file.id}')" class="btn">Download</button>
                            <button onclick="deleteFile('${file.id}')" class="btn">Delete</button>
                        </td>
                    `;
                });
            }
        } else {
            NotificationManager.error('Failed to fetch files. Please try again later.');
        }
    } catch (error) {
        console.error('Network error while fetching files:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

async function handleFileUpload() {
    const fileInput = document.getElementById('file-upload');
    const files = fileInput.files;

    if (files.length === 0) {
        NotificationManager.error('Please select at least one file to upload.');
        return;
    }

    const formData = new FormData();
    Array.from(files).forEach(file => formData.append('files', file));

    try {
        const response = await fetch(`${backendUrl}/files/upload`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${state.token}` },
            body: formData
        });

        if (response.ok) {
            NotificationManager.success('Files uploaded successfully.');
            populateFileTable();
        } else if (response.status === 413) {
            NotificationManager.error('File size exceeds the allowed limit.');
        } else {
            NotificationManager.error('Failed to upload files. Please try again later.');
        }
    } catch (error) {
        console.error('Network error while uploading files:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

async function searchPublicFiles() {
    const username = document.getElementById('search-user').value.trim();
    const publicFileList = document.getElementById('public-file-list');

    if (!username) {
        NotificationManager.error('Please enter a username to search.');
        return;
    }

    publicFileList.innerHTML = '';

    try {
        const response = await fetch(`${backendUrl}/public-files?username=${username}`);

        if (response.ok) {
            const files = await response.json();
            if (files.length === 0) {
                publicFileList.innerHTML = '<p>No public files found for this user.</p>';
                NotificationManager.error('No public files found for this user.');
            } else {
                publicFileList.innerHTML = files.map(file => `
                    <div class="card">
                        <h3>${file.username}'s Files</h3>
                        <ul>
                            <li>${file.name} (${file.type})</li>
                        </ul>
                    </div>
                `).join('');
                NotificationManager.success(`Found ${files.length} public files.`);
            }
        } else {
            NotificationManager.error('Failed to search public files. Please try again later.');
        }
    } catch (error) {
        console.error('Network error while searching public files:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

async function downloadFile(fileId) {
    try {
        const response = await fetch(`${backendUrl}/files/download/${fileId}`, {
            method: 'GET',
            headers: { Authorization: `Bearer ${state.token}` }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "downloaded-file";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            NotificationManager.success('File downloaded successfully.');
        } else {
            NotificationManager.error('Failed to download file. Please try again later.');
        }
    } catch (error) {
        console.error('Network error while downloading file:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

async function deleteFile(fileId) {
    try {
        const response = await fetch(`${backendUrl}/files/${fileId}`, {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${state.token}` }
        });

        if (response.ok) {
            NotificationManager.success('File deleted successfully.');
            populateFileTable();
        } else {
            NotificationManager.error('Failed to delete file. Please try again later.');
        }
    } catch (error) {
        console.error('Network error while deleting file:', error);
        NotificationManager.error('Unable to connect to the server. Please check your network connection.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    buttons.loginSidebar.addEventListener('click', () => showSection(sections.login));
    buttons.registerSidebar.addEventListener('click', () => showSection(sections.register));
    buttons.filesSidebar.addEventListener('click', () => showSection(sections.fileManagement));
    buttons.publicSidebar.addEventListener('click', () => showSection(sections.publicFiles));

    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('btn-upload').addEventListener('click', handleFileUpload);
    document.getElementById('btn-search').addEventListener('click', searchPublicFiles);
});

function updateUIAfterLogin() {
    showSection(sections.fileManagement);
    populateFileTable();
}
