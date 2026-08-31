/**
 * Button loading state manager
 * Utility functions to manage button loading states
 */

// Set button to loading state
function setButtonLoading(buttonId, loadingText = 'Loading...') {
    const button = document.getElementById(buttonId);
    if (!button) return;
    
    // Store original text for later restoration
    button.setAttribute('data-original-text', button.textContent);
    button.textContent = loadingText;
    button.disabled = true;
}

// Restore button from loading state
function restoreButton(buttonId) {
    const button = document.getElementById(buttonId);
    if (!button) return;
    
    const originalText = button.getAttribute('data-original-text') || buttonId;
    button.textContent = originalText;
    button.disabled = false;
}

// Execute a function while showing loading state on a button
async function withButtonLoading(buttonId, asyncFunction, options = {}) {
    const {
        loadingText = 'Loading...',
        successNotification = null,
        errorNotification = 'Operation failed. See console for details.'
    } = options;
    
    setButtonLoading(buttonId, loadingText);
    
    try {
        const result = await asyncFunction();
        
        if (successNotification && typeof showNotification === 'function') {
            showNotification(successNotification, 'success');
        }
        
        return result;
    } catch (error) {
        console.error(`Error in operation for button ${buttonId}:`, error);
        
        if (errorNotification && typeof showNotification === 'function') {
            showNotification(errorNotification, 'error');
        }
        
        throw error;
    } finally {
        restoreButton(buttonId);
    }
}
