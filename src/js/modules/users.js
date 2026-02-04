/* ============================================
   USER MANAGEMENT MODULE
   ============================================ */

class UserModule {
    constructor(db) {
        this.db = db;
    }
    
    loadUsers() {
        // Call async API to get users
        this.db.getUsers()
            .then(users => {
                const tbody = document.getElementById('users-tbody');
                tbody.innerHTML = '';
                
                users.forEach(user => {
                    const tr = document.createElement('tr');
                    const date = new Date(user.createdAt).toLocaleDateString();
                    
                    tr.innerHTML = `
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td>${user.role}</td>
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
}
