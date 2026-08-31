/**
 * Shared notification system for admin pages
 * Creates consistent notifications across all admin pages
 */

// Global notification system
function showNotification(message, type = 'info', duration = 5000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Add animation
    setTimeout(() => {
        notification.classList.add('notification-visible');
    }, 10);
    
    // Auto remove after specified duration
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.remove('notification-visible');
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }
}

// Export for global use
window.showNotification = showNotification;
