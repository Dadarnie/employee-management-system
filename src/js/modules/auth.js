/* ============================================
   AUTHENTICATION MODULE
   ============================================ */

class AuthModule {
    constructor(db) {
        this.db = db;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Sign In Form
        const signInForm = document.getElementById('signin-form');
        if (signInForm) {
            signInForm.addEventListener('submit', (e) => this.handleSignIn(e));
        }
        
        // Sign Up Form
        const signUpForm = document.getElementById('signup-form');
        if (signUpForm) {
            signUpForm.addEventListener('submit', (e) => this.handleSignUp(e));
        }
        
        // Forgot Password Form
        const forgotForm = document.getElementById('forgot-form');
        if (forgotForm) {
            forgotForm.addEventListener('submit', (e) => this.handleForgotPassword(e));
        }
    }
    
    switchAuthTab(tab) {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        event.target.classList.add('active');
        
        document.querySelectorAll('.auth-form').forEach(f => f.classList.add('hidden'));
        
        if (tab === 'signin') {
            document.getElementById('signin-form').classList.remove('hidden');
        } else if (tab === 'signup') {
            document.getElementById('signup-form').classList.remove('hidden');
        }
        
        this.clearAlerts();
    }
    
    showForgotPassword() {
        document.querySelectorAll('.auth-form').forEach(f => f.classList.add('hidden'));
        document.getElementById('forgot-form').classList.remove('hidden');
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        this.clearAlerts();
    }
    
    showSignIn() {
        document.querySelectorAll('.auth-form').forEach(f => f.classList.add('hidden'));
        document.getElementById('signin-form').classList.remove('hidden');
        document.querySelectorAll('.auth-tab')[0].classList.add('active');
        this.clearAlerts();
    }
    
    handleSignIn(e) {
        e.preventDefault();
        
        const email = document.getElementById('signin-email').value;
        const password = document.getElementById('signin-password').value;
        
        this.db.loginUser(email, password)
            .then(response => {
                showAlert('success', 'Welcome back! Redirecting...');
                
                setTimeout(() => {
                    showDashboard();
                }, 1000);
            })
            .catch(error => {
                const errorData = error.response || {};
                
                // Check for locked account
                if (errorData.locked) {
                    const remaining = errorData.remaining_cooldown || 30;
                    showAlert('error', `Account locked. Try again in ${remaining} seconds. ⏰`);
                    
                    // Disable input for cooldown period
                    const inputs = document.querySelectorAll('#signin-form input, #signin-form button');
                    inputs.forEach(input => input.disabled = true);
                    
                    setTimeout(() => {
                        inputs.forEach(input => input.disabled = false);
                        showAlert('success', 'Account unlocked. You can try again now.');
                    }, remaining * 1000);
                    
                    return;
                }
                
                // Check for warning (3+ attempts)
                if (errorData.warning) {
                    const remaining = errorData.attempts_remaining || 2;
                    showAlert('warning', `⚠️ WARNING: ${remaining} attempt(s) remaining before 30-second cooldown!`);
                    return;
                }
                
                // Check for remaining attempts
                if (errorData.attempts_remaining !== undefined) {
                    showAlert('error', `Invalid email or password. Attempts remaining: ${errorData.attempts_remaining}`);
                    return;
                }
                
                showAlert('error', error.message || 'Invalid email or password');
            });
    }
    
    handleSignUp(e) {
        e.preventDefault();
        
        const name = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        const confirm = document.getElementById('signup-confirm').value;
        
        if (password !== confirm) {
            showAlert('error', 'Passwords do not match!');
            return;
        }
        
        this.db.registerUser({ name, email, password })
            .then(response => {
                this.db.setCurrentUser(response.user);
                this.db.setToken(response.token);
                
                showAlert('success', 'Account created! Redirecting...');
                
                setTimeout(() => {
                    showDashboard();
                }, 1000);
            })
            .catch(error => {
                showAlert('error', error.message);
            });
    }
    
    handleForgotPassword(e) {
        e.preventDefault();
        
        const email = document.getElementById('forgot-email').value;
        showAlert('success', 'Password reset link sent to ' + email);
        
        setTimeout(() => {
            this.showSignIn();
        }, 2000);
    }
    
    clearAlerts() {
        document.getElementById('alert-container').innerHTML = '';
    }
}
