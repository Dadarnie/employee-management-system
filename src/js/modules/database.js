/* ============================================
   DATABASE MODULE (API Client)
   Connects to backend SQLite database via REST API
   ============================================ */

class Database {
    constructor() {
        // Browser can't access process.env, use hardcoded backend URL
        // Can be changed with setApiURL() if needed
        this.apiURL = 'http://localhost:5001/api';
        this.token = localStorage.getItem('token');
    }
    
    /**
     * Set API URL
     */
    setApiURL(url) {
        this.apiURL = url;
    }
    
    /**
     * Set authentication token
     */
    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
        }
    }
    
    /**
     * Get authorization headers
     */
    getHeaders() {
        const headers = { 'Content-Type': 'application/json' };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }
    
    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.apiURL}${endpoint}`;
        const fetchOptions = {
            headers: this.getHeaders(),
            ...options
        };
        
        try {
            const response = await fetch(url, fetchOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }
    
    // ============ Authentication Operations ============
    async registerUser(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }
    
    async loginUser(email, password) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (response.token) {
            this.setToken(response.token);
            this.setCurrentUser(response.user);
        }
        
        return response;
    }
    
    async verifyToken() {
        try {
            return await this.request('/auth/verify');
        } catch (error) {
            this.setToken(null);
            return null;
        }
    }
    
    // ============ User Operations ============
    async createUser(userData) {
        return this.request('/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }
    
    async getUsers() {
        return this.request('/users');
    }
    
    async getUserById(id) {
        return this.request(`/users/${id}`);
    }
    
    async updateUser(id, userData) {
        return this.request(`/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }
    
    async deleteUser(id) {
        return this.request(`/users/${id}`, {
            method: 'DELETE'
        });
    }
    
    // ============ Employee Operations ============
    async createEmployee(empData) {
        return this.request('/employees', {
            method: 'POST',
            body: JSON.stringify(empData)
        });
    }
    
    async getEmployees(filters = {}) {
        const params = new URLSearchParams();
        
        if (filters.search) params.append('search', filters.search);
        if (filters.department) params.append('department', filters.department);
        if (filters.isActive !== undefined) params.append('isActive', filters.isActive);
        if (filters.sortBy) params.append('sortBy', filters.sortBy);
        if (filters.order) params.append('order', filters.order);
        
        const query = params.toString() ? `?${params.toString()}` : '';
        return this.request(`/employees${query}`);
    }
    
    async getEmployeeById(id) {
        return this.request(`/employees/${id}`);
    }
    
    async updateEmployee(id, empData) {
        return this.request(`/employees/${id}`, {
            method: 'PUT',
            body: JSON.stringify(empData)
        });
    }
    
    async deleteEmployee(id) {
        return this.request(`/employees/${id}`, {
            method: 'DELETE'
        });
    }
    
    async getEmployeeStats() {
        return this.request('/employees/stats');
    }
    
    async getDepartments() {
        return this.request('/employees/departments');
    }
    
    // ============ Session Management ============
    setCurrentUser(user) {
        if (user) {
            localStorage.setItem('currentUser', JSON.stringify(user));
        } else {
            localStorage.removeItem('currentUser');
        }
    }
    
    getCurrentUser() {
        const user = localStorage.getItem('currentUser');
        return user ? JSON.parse(user) : null;
    }
    
    clearCurrentUser() {
        localStorage.removeItem('currentUser');
        this.setToken(null);
    }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Database;
}