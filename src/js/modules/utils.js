/* ============================================
   UTILITY FUNCTIONS MODULE
   ============================================ */

function showAlert(type, message) {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    container.innerHTML = '';
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function showModalAlert(type, message) {
    const container = document.getElementById('modal-alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    container.innerHTML = '';
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Global functions for HTML onclick handlers
function switchAuthTab(tab) {
    authModule.switchAuthTab(tab);
}

function showForgotPassword() {
    authModule.showForgotPassword();
}

function showSignIn() {
    authModule.showSignIn();
}

function showDashboard() {
    dashboardModule.show();
}

function showAuth() {
    dashboardModule.showAuth();
}

function logout() {
    dashboardModule.logout();
}

function openEmployeeModal() {
    employeeModule.openModal();
}

function closeEmployeeModal() {
    employeeModule.closeModal();
}

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const modal = document.getElementById('employee-modal');
    if (e && e.target === modal) {
        employeeModule.closeModal();
    }
});
