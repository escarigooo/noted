/**
 * Analytics Data Handler - Update analytics page with JSON structure
 */

// Prevent double declaration
if (typeof AdminAnalytics === 'undefined') {
    class AdminAnalytics {
        constructor() {
            this.dataUrl = '/static/data/analytics.json';
            this.refreshUrl = '/admin/refresh-analytics';  // SUCCESS This works!
            this.data = null;
        }

    async fetchData() {
        try {
            const response = await fetch(this.dataUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.data = await response.json();
            console.log('DATA Analytics data loaded:', this.data);
            return this.data;
        } catch (error) {
            console.error('FAILED Error fetching analytics data:', error);
            return null;
        }
    }

    /**
     * Refresh analytics by running the notebook with improved error handling
     */
    async refreshAnalytics() {
        try {
            console.log('Starting analytics refresh...');
            await this.fetchData();
            // Show loading message
            if (typeof showNotification === 'function') {
                showNotification('Refreshing analytics data...', 'info');
            }
            
            // Get CSRF token if using Flask-WTF
            const csrfToken = document.querySelector('meta[name=csrf-token]')?.content;
            
            const headers = {
                'Content-Type': 'application/json',
            };
            
            // Add CSRF token if available
            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
            }
            
            const response = await fetch(this.refreshUrl, {
                method: 'POST',
                headers: headers,
                credentials: 'same-origin'  // Include cookies for session
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                this.data = result.data;
                
                // Display appropriate message based on notebook execution
                if (result.notebook_executed) {
                    console.log('SUCCESS Analytics refreshed via notebook:', this.data);
                    if (typeof showNotification === 'function') {
                        showNotification('Analytics data refreshed successfully!', 'success');
                    }
                } else {
                    console.log('FALLBACK Using existing analytics data:', this.data);
                    if (typeof showNotification === 'function') {
                        const message = result.notebook_error ? 
                            'Using existing analytics data (notebook execution failed)' : 
                            'Using existing analytics data';
                        showNotification(message, 'warning');
                    }
                }
                
                return this.data;
            } else {
                throw new Error(result.error || 'Failed to refresh analytics');
            }
            
        } catch (error) {
            console.error('FAILED Error refreshing analytics:', error);
            
            // Show error notification
            if (typeof showNotification === 'function') {
                showNotification('Failed to refresh analytics data', 'error');
                
                // Show install suggestion if needed
                if (error.message && error.message.includes('Jupyter not found')) {
                    setTimeout(() => {
                        showNotification('Install Jupyter with: pip install jupyter nbconvert', 'info', 8000);
                    }, 1000);
                }
            }
            
            throw error;
        }
    }

    /**
     * Update analytics page with nested JSON structure
     */
    updateAnalyticsPage() {
        if (!this.data) return;

        const analytics = this.data.analytics || {};
        const dashboard = this.data.dashboard || {};
        
        this.updateStatCard('total-sales', this.formatCurrency(dashboard.total_sales || 0));
        this.updateStatCard('monthly-sales', this.formatCurrency(dashboard.monthly_sales || 0));
        this.updateStatCard('total-orders', dashboard.total_orders || 0);
        this.updateStatCard('monthly-orders', dashboard.monthly_orders || 0);
        this.updateStatCard('total-customers', dashboard.total_customers || 0);
        this.updateStatCard('revenue-growth', this.formatPercentage(dashboard.revenue_growth || 0));
        
        this.updateLastUpdated();
        this.hideLoading();
    }

    /**
     * Update dashboard page with overview data
     */
    updateDashboardPage() {
        if (!this.data) return;

        const dashboard = this.data.dashboard || {};
        
        this.updateStatCard('total-sales', this.formatCurrency(dashboard.total_sales || 0));
        this.updateStatCard('monthly-sales', this.formatCurrency(dashboard.monthly_sales || 0));
        this.updateStatCard('total-orders', dashboard.total_orders || 0);
        this.updateStatCard('total-customers', dashboard.total_customers || 0);
        this.updateStatCard('revenue-growth', this.formatPercentage(dashboard.revenue_growth || 0));
        
        this.updateLastUpdated();
        this.hideLoading();
    }

    /**
     * Update last updated display
     */
    updateLastUpdated() {
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated && this.data) {
            const formattedDate = this.getLastUpdated();
            lastUpdated.textContent = formattedDate || 'Unknown';
        }
    }

    /**
     * Update orders page with available data
     */
    updateOrdersPage() {
        if (!this.data) return;
        
        const orders = this.data.orders || {};
        const dashboard = this.data.dashboard || {};
        
        this.updateStatCard('total-orders', orders.total_orders || 0);
        this.updateStatCard('monthly-orders', orders.monthly_orders || 0);
        this.updateStatCard('paid-orders', Math.floor(orders.paid_orders || 0));
        this.updateStatCard('unpaid-orders', Math.floor(orders.unpaid_orders || 0));
        this.updateStatCard('total-revenue', this.formatCurrency(dashboard.total_sales || 0));
        
        this.updateLastUpdated();
        this.hideLoading();
    }

    updateProductsPage() {
        if (!this.data) return;
        
        const products = this.data.products || {};
        
        this.updateStatCard('total-products', products.total_products || 0);
        this.updateStatCard('out-of-stock', products.out_of_stock_count || 0);
        this.updateStatCard('low-stock-count', products.low_stock_count || 0);
        this.updateStatCard('total-categories', products.total_categories || 0);
        
        this.updateLastUpdated();
        this.hideLoading();
    }

    updateCategoriesPage() {
        if (!this.data) return;
        
        const products = this.data.products || {};
        
        this.updateStatCard('total-categories', products.total_categories || 0);
        this.updateStatCard('active-categories', products.total_categories || 0); // Using total as active
        this.updateStatCard('products-assigned', products.total_products || 0);
        
        this.updateLastUpdated();
        this.hideLoading();
    }

    updateUsersPage() {
        if (!this.data) return;
        
        const users = this.data.users || {};
        
        this.updateStatCard('total-users', users.total_users || 0);
        this.updateStatCard('total-admins', Math.floor(users.total_admins || 0));
        this.updateStatCard('total-customers', Math.floor(users.total_customers || 0));
        this.updateStatCard('users-with-orders', users.users_with_orders || 0);
        
        this.updateLastUpdated();
        this.hideLoading();
    }

    updateStatCard(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        } else {
            // Try alternative selectors for different page structures
            const altElement = document.querySelector(`#${elementId}, .stat-number[id="${elementId}"]`);
            if (altElement) {
                altElement.textContent = value;
            } else {
                console.warn(`Element not found: ${elementId}`);
            }
        }
    }

    formatCurrency(amount) {
        const num = parseFloat(amount) || 0;
        return new Intl.NumberFormat('pt-PT', {
            style: 'currency',
            currency: 'EUR'
        }).format(num);
    }

    formatNumber(num) {
        return new Intl.NumberFormat('pt-PT').format(num || 0);
    }

    formatPercentage(num) {
        const value = parseFloat(num) || 0;
        const sign = value >= 0 ? '+' : '';
        return `${sign}${value.toFixed(1)}%`;
    }

    getLastUpdated() {
        if (!this.data || !this.data.last_updated) return null;
        
        const date = new Date(this.data.last_updated);
        return new Intl.DateTimeFormat('pt-PT', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    }

    hideLoading() {
        // Loading state removed, now using notifications only
    }
}

// Export classes for global use - don't auto-initialize on analytics page
window.AdminAnalytics = AdminAnalytics;

} // End of AdminAnalytics class protection

// Auto-load data when page loads (only for non-analytics pages)
document.addEventListener('DOMContentLoaded', async () => {
    const currentPage = window.location.pathname;
    
    // Skip auto-initialization on analytics page (handled in analytics.html)
    if (currentPage.includes('/admin/analytics')) {
        console.log('DATA Analytics page detected - skipping auto-init');
        return;
    }
    
    console.log('LAUNCH Loading analytics data for:', currentPage);
    
    const adminAnalytics = new AdminAnalytics();
    await adminAnalytics.fetchData();
    
    console.log(' Current page:', currentPage);
    
    if (currentPage.includes('/admin/dashboard') || currentPage === '/admin' || currentPage.endsWith('/admin/')) {
        adminAnalytics.updateDashboardPage();
    } else if (currentPage.includes('/admin/orders')) {
        adminAnalytics.updateOrdersPage();
    } else if (currentPage.includes('/admin/products')) {
        adminAnalytics.updateProductsPage();
    } else if (currentPage.includes('/admin/categories')) {
        adminAnalytics.updateCategoriesPage();
    } else if (currentPage.includes('/admin/users')) {
        adminAnalytics.updateUsersPage();
    }
});

// Refresh function for manual use (non-analytics pages)
async function refreshAnalytics() {
    // For analytics page, use the handler from analytics.html
    if (window.location.pathname.includes('/admin/analytics') && window.analyticsHandler) {
        return; // Let analytics.html handle this
    }
    
    const refreshBtn = document.querySelector('button[onclick="refreshAnalytics()"]');
    
    try {
        // Disable refresh button while loading
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.textContent = 'refreshing...';
        }
        
        // Create a new instance for refresh
        const adminAnalytics = new AdminAnalytics();
        await adminAnalytics.refreshAnalytics();
        
        // Update the current page
        const currentPage = window.location.pathname;
        if (currentPage.includes('/admin/dashboard') || currentPage === '/admin' || currentPage.endsWith('/admin/')) {
            adminAnalytics.updateDashboardPage();
        } else if (currentPage.includes('/admin/orders')) {
            adminAnalytics.updateOrdersPage();
        } else if (currentPage.includes('/admin/products')) {
            adminAnalytics.updateProductsPage();
        } else if (currentPage.includes('/admin/categories')) {
            adminAnalytics.updateCategoriesPage();
        } else if (currentPage.includes('/admin/users')) {
            adminAnalytics.updateUsersPage();
        }
        
        // Show success message
        console.log('Data refreshed successfully!');        } catch (error) {
        console.error('Refresh failed:', error);
        alert('failed to refresh data: ' + error.message);
    } finally {
        // Hide loading state
        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Refresh Data';
        }
    }
}

// Export refresh function for global use on analytics page only
window.refreshAnalytics = refreshAnalytics;
