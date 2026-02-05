/* ============================================
   USER MANAGEMENT MODULE
   ============================================ */

class UserModule {
    constructor(db) {
        this.db = db;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        const userForm = document.getElementById('user-form');
        if (userForm) {
            userForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    }
    
    loadUsers() {
        // Call async API to get users
        this.db.getUsers()
            .then(users => {
                const tbody = document.getElementById('users-tbody');
                tbody.innerHTML = '';
                
                if (!Array.isArray(users) || users.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No users found</td></tr>';
                    return;
                }
                
                users.forEach(user => {
                    const tr = document.createElement('tr');
                    const date = new Date(user.created_at).toLocaleString();
                    
                    tr.innerHTML = `
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td><span class="badge ${user.role === 'admin' ? 'badge-info' : 'badge-success'}">${user.role}</span></td>
                        <td>${date}</td>
                        <td class="action-buttons">
                            <button class="btn-delete" onclick="userModule.deleteUser(${user.id})">Delete</button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(error => {
                console.error('Error loading users:', error);
                showAlert('error', 'Failed to load users');
            });
    }
    
    deleteUser(id) {
        const currentUser = this.db.getCurrentUser();
        
        if (currentUser.id === id) {
            alert('You cannot delete your own account!');
            return;
        }
        
        if (confirm('Are you sure you want to delete this user?')) {
            this.db.deleteUser(id)
                .then(() => {
                    this.loadUsers();
                    showAlert('success', 'User deleted successfully!');
                })
                .catch(error => {
                    console.error('Error deleting user:', error);
                    showAlert('error', 'Failed to delete user');
                });
        }
    }
    
    openModal(userId = null) {
        const modal = document.getElementById('user-modal');
        const form = document.getElementById('user-form');
        const title = document.getElementById('user-modal-title');
        
        form.reset();
        document.getElementById('user-id').value = '';
        this.clearModalAlerts();
        
        if (userId) {
            // Edit mode (not implemented for users yet)
            title.textContent = 'Edit User';
        } else {
            // Add mode
            title.textContent = 'Add User';
        }
        
        modal.classList.add('active');
    }
    
    closeModal() {
        document.getElementById('user-modal').classList.remove('active');
        document.getElementById('user-form').reset();
        this.clearModalAlerts();
    }
    
    handleFormSubmit(e) {
        e.preventDefault();
        
        const name = document.getElementById('user-name').value;
        const email = document.getElementById('user-email').value;
        const password = document.getElementById('user-password').value;
        const role = document.getElementById('user-role').value;
        
        if (!name || !email || !password || !role) {
            this.showModalAlert('error', 'All fields are required!');
            return;
        }
        
        this.db.createUser({
            name: name,
            email: email,
            password: password,
            role: role
        })
        .then(() => {
            this.showModalAlert('success', 'User created successfully!');
            setTimeout(() => {
                this.closeModal();
                this.loadUsers();
            }, 1000);
        })
        .catch(error => {
            console.error('Error creating user:', error);
            const errorMsg = error.response?.error || error.message || 'Failed to create user';
            this.showModalAlert('error', errorMsg);
        });
    }
    
    showModalAlert(type, message) {
        const alertContainer = document.getElementById('user-modal-alert-container');
        alertContainer.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    }
    
    clearModalAlerts() {
        const alertContainer = document.getElementById('user-modal-alert-container');
        alertContainer.innerHTML = '';
    }
}
