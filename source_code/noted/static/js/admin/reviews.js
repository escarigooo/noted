/**
 * Admin Reviews Dashboard JavaScript
 * Handles dynamic stat calculations, real-time updates, and email preview functionality
 */

class ReviewsDashboard {
    constructor() {
        this.statsConfig = {
            emailTemplates: {
                selector: '.dashboard-section:first-of-type .review-card',
                elementId: 'email-templates-count'
            },
            customerPages: {
                selector: '.dashboard-section:nth-of-type(2) .review-card',
                elementId: 'customer-pages-count',
                basePages: 8 // Core pages: Home, Products, Cart, Checkout, Account, Login, Register, Search
            },
            adminSections: {
                selector: '.dashboard-section:nth-of-type(3) .review-card',
                elementId: 'admin-sections-count',
                basePages: 4 // Dashboard, Users, Categories, Settings
            },
            systemHealth: {
                elementId: 'system-health-percentage'
            }
        };
        
        this.init();
    }

    init() {
        this.calculateAllStats();
        this.updateCurrentTime();
        this.initEmailPreview();
        
        // Update stats every 30 seconds
        setInterval(() => {
            this.calculateAllStats();
            this.updateCurrentTime();
        }, 30000);
        
        // Update system health every 10 seconds
        setInterval(() => {
            this.calculateSystemHealth();
        }, 10000);
    }

    /**
     * Initialize email preview functionality
     */
    initEmailPreview() {
        // Initialize category filtering
        const categoryButtons = document.querySelectorAll('.category-btn');
        categoryButtons.forEach(btn => {
            btn.addEventListener('click', () => this.filterEmailTemplates(btn.dataset.category));
        });
    }

    /**
     * Filter email templates by category
     */
    filterEmailTemplates(category) {
        // Update active button
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === category);
        });

        // Filter template cards
        const cards = document.querySelectorAll('.email-template-card');
        cards.forEach(card => {
            const cardCategory = card.dataset.category;
            const shouldShow = category === 'all' || cardCategory === category;
            card.classList.toggle('hidden', !shouldShow);
        });
    }

    /**
     * Switch between desktop and mobile email preview
     * (Kept for potential future use)
     */
    switchEmailView(view) {
        // Update active tab
        document.querySelectorAll('.email-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.view === view);
        });

        // Update iframe view
        const iframe = document.getElementById('email-preview-frame');
        if (iframe) {
            iframe.classList.toggle('mobile-view', view === 'mobile');
        }
    }

    /**
     * Calculate and update all dashboard statistics
     */
    calculateAllStats() {
        this.calculateEmailTemplates();
        this.calculateCustomerPages();
        this.calculateAdminSections();
        this.calculateSystemHealth();
    }

    /**
     * Count email template cards
     */
    calculateEmailTemplates() {
        const emailCards = document.querySelectorAll(this.statsConfig.emailTemplates.selector);
        const count = emailCards.length;
        
        this.updateStatElement(this.statsConfig.emailTemplates.elementId, count);
        
        console.log(`[Reviews Dashboard] Email Templates: ${count}`);
        return count;
    }

    /**
     * Calculate total customer-facing pages
     */
    calculateCustomerPages() {
        const customerCards = document.querySelectorAll(this.statsConfig.customerPages.selector);
        const reviewablePages = customerCards.length;
        const totalPages = reviewablePages + this.statsConfig.customerPages.basePages;
        
        this.updateStatElement(this.statsConfig.customerPages.elementId, totalPages);
        
        console.log(`[Reviews Dashboard] Customer Pages: ${totalPages} (${reviewablePages} reviewable + ${this.statsConfig.customerPages.basePages} core)`);
        return totalPages;
    }

    /**
     * Calculate total admin sections
     */
    calculateAdminSections() {
        const adminCards = document.querySelectorAll(this.statsConfig.adminSections.selector);
        const reviewableAdminSections = adminCards.length;
        const totalSections = reviewableAdminSections + this.statsConfig.adminSections.basePages;
        
        this.updateStatElement(this.statsConfig.adminSections.elementId, totalSections);
        
        console.log(`[Reviews Dashboard] Admin Sections: ${totalSections} (${reviewableAdminSections} reviewable + ${this.statsConfig.adminSections.basePages} base)`);
        return totalSections;
    }

    /**
     * Calculate system health based on status indicators
     */
    calculateSystemHealth() {
        const allIndicators = document.querySelectorAll('.status-indicator');
        const warningIndicators = document.querySelectorAll('.status-indicator.warning');
        const errorIndicators = document.querySelectorAll('.status-indicator.error');
        
        if (allIndicators.length === 0) {
            this.updateStatElement(this.statsConfig.systemHealth.elementId, '100%', '#28a745');
            return 100;
        }
        
        const healthyIndicators = allIndicators.length - warningIndicators.length - errorIndicators.length;
        const healthPercentage = Math.round((healthyIndicators / allIndicators.length) * 100);
        
        // Determine color based on health percentage
        let color = '#28a745'; // Green
        if (healthPercentage < 95 && healthPercentage >= 85) {
            color = '#ffc107'; // Yellow
        } else if (healthPercentage < 85) {
            color = '#dc3545'; // Red
        }
        
        this.updateStatElement(this.statsConfig.systemHealth.elementId, `${healthPercentage}%`, color);
        
        console.log(`[Reviews Dashboard] System Health: ${healthPercentage}% (${healthyIndicators}/${allIndicators.length} healthy)`);
        return healthPercentage;
    }

    /**
     * Update a stat element with new value and optional color
     */
    updateStatElement(elementId, value, color = null) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
            if (color) {
                element.style.color = color;
            }
        }
    }

    /**
     * Update current time display
     */
    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleString();
        const timeElement = document.getElementById('current-time');
        
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }

    /**
     * Simulate adding a warning indicator (for testing)
     */
    simulateWarning(selector) {
        const indicator = document.querySelector(selector + ' .status-indicator');
        if (indicator && !indicator.classList.contains('warning')) {
            indicator.classList.add('warning');
            this.calculateSystemHealth();
            console.log('[Reviews Dashboard] Warning indicator added');
        }
    }

    /**
     * Simulate removing a warning indicator (for testing)
     */
    removeWarning(selector) {
        const indicator = document.querySelector(selector + ' .status-indicator');
        if (indicator && indicator.classList.contains('warning')) {
            indicator.classList.remove('warning');
            this.calculateSystemHealth();
            console.log('[Reviews Dashboard] Warning indicator removed');
        }
    }

    /**
     * Get current statistics
     */
    getCurrentStats() {
        return {
            emailTemplates: this.calculateEmailTemplates(),
            customerPages: this.calculateCustomerPages(),
            adminSections: this.calculateAdminSections(),
            systemHealth: this.calculateSystemHealth()
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.reviewsDashboard = new ReviewsDashboard();
    
    // Expose some functions for console testing
    window.addWarning = (selector) => window.reviewsDashboard.simulateWarning(selector);
    window.removeWarning = (selector) => window.reviewsDashboard.removeWarning(selector);
    window.getStats = () => window.reviewsDashboard.getCurrentStats();
});

// Export for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReviewsDashboard;
}

/**
 * Email Preview Global Functions
 * These functions are called directly from the HTML template
 */

/**
 * Preview order status email with selected status
 */
function previewOrderStatusEmail() {
    const statusSelect = document.getElementById('order-status-select');
    const selectedStatus = statusSelect ? statusSelect.value : 'pending';
    
    const previewUrl = `/admin/preview-email/order_status?status=${selectedStatus}`;
    window.open(previewUrl, '_blank');
}

/**
 * Preview specific email template
 */
function previewEmail(templateName) {
    const previewUrl = `/admin/preview-email/${templateName}`;
    window.open(previewUrl, '_blank');
}

/**
 * Send test email (deprecated - kept for reference)
 */
function sendTestEmail(templateType) {
    const testEmail = prompt('Enter email address to send test email to:');
    if (!testEmail) return;
    
    // Show loading state
    const originalText = event.target.textContent;
    event.target.textContent = 'Sending...';
    event.target.disabled = true;
    
    // Prepare payload
    let payload = { email: testEmail, template: templateType };
    
    // Add status for order status emails
    if (templateType === 'order_status') {
        const statusSelect = document.getElementById('order-status-select');
        payload.status = statusSelect ? statusSelect.value : 'pending';
    }
    
    fetch('/admin/send-test-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Test email sent successfully to ${testEmail}!`);
        } else {
            alert(`Failed to send test email: ${data.error || 'Unknown error'}`);
        }
    })
    .catch(error => {
        console.error('Error sending test email:', error);
        alert('Failed to send test email. Please check the console for details.');
    })
    .finally(() => {
        event.target.textContent = originalText;
        event.target.disabled = false;
    });
}

/**
 * Open email preview modal
 */
function openEmailPreviewModal(title, previewUrl) {
    const modal = document.getElementById('email-preview-modal');
    const modalTitle = document.getElementById('email-modal-title');
    const iframe = document.getElementById('email-preview-frame');
    const loading = document.getElementById('email-preview-loading');
    
    if (!modal || !modalTitle || !iframe || !loading) {
        console.error('Email preview modal elements not found');
        return;
    }
    
    // Set title and show modal
    modalTitle.textContent = title;
    modal.classList.add('active');
    
    // Show loading state
    loading.style.display = 'block';
    iframe.style.display = 'none';
    
    // Store current preview info
    window.reviewsDashboard.currentEmailPreview = { title, previewUrl };
    
    // Load email preview
    iframe.onload = () => {
        loading.style.display = 'none';
        iframe.style.display = 'block';
    };
    
    iframe.onerror = () => {
        loading.innerHTML = '<p style="color: #dc3545;">Failed to load email preview</p>';
    };
    
    iframe.src = previewUrl;
}

/**
 * Close email preview modal
 */
function closeEmailModal() {
    const modal = document.getElementById('email-preview-modal');
    const iframe = document.getElementById('email-preview-frame');
    
    if (modal) {
        modal.classList.remove('active');
    }
    
    if (iframe) {
        iframe.src = '';
    }
    
    window.reviewsDashboard.currentEmailPreview = null;
}

/**
 * Refresh current email preview
 */
function refreshEmailPreview() {
    if (window.reviewsDashboard.currentEmailPreview) {
        const { title, previewUrl } = window.reviewsDashboard.currentEmailPreview;
        openEmailPreviewModal(title, previewUrl);
    }
}

/**
 * Open email preview in new tab
 */
function openEmailInNewTab() {
    if (window.reviewsDashboard.currentEmailPreview) {
        const { previewUrl } = window.reviewsDashboard.currentEmailPreview;
        window.open(previewUrl, '_blank');
    }
}
