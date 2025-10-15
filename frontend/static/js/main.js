/**
 * KoloCloud Main JavaScript
 * Global utility functions and common functionality
 */

// Show notification
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-${getIconForType(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Logout function
async function logout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        if (response.ok) {
            window.location.href = '/login';
        } else {
            showNotification('Помилка виходу', 'error');
        }
    } catch (error) {
        showNotification('Помилка з\'єднання', 'error');
    }
}

// Format file size
function formatFileSize(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'Н/Д';
    const date = new Date(dateString);
    return date.toLocaleString('uk-UA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format date relative (e.g., "2 hours ago")
function formatDateRelative(dateString) {
    if (!dateString) return 'Н/Д';
    const date = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds
    
    if (diff < 60) return 'щойно';
    if (diff < 3600) return `${Math.floor(diff / 60)} хв тому`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} год тому`;
    if (diff < 604800) return `${Math.floor(diff / 86400)} днів тому`;
    
    return formatDate(dateString);
}

// Copy to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Скопійовано в буфер обміну', 'success');
        });
    } else {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showNotification('Скопійовано в буфер обміну', 'success');
    }
}

// Download text as file
function downloadTextAsFile(text, filename) {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Loading indicator
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Завантаження...';
    element.disabled = true;
    
    return () => {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// Confirm dialog
function confirmAction(message) {
    return new Promise((resolve) => {
        const result = confirm(message);
        resolve(result);
    });
}

// Get file icon class
function getFileIcon(fileType) {
    const icons = {
        'pdf': 'fa-file-pdf',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'xls': 'fa-file-excel',
        'xlsx': 'fa-file-excel',
        'ppt': 'fa-file-powerpoint',
        'pptx': 'fa-file-powerpoint',
        'txt': 'fa-file-alt',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'png': 'fa-file-image',
        'gif': 'fa-file-image',
        'zip': 'fa-file-archive',
        'rar': 'fa-file-archive',
        'mp4': 'fa-file-video',
        'mp3': 'fa-file-audio'
    };
    
    return icons[fileType?.toLowerCase()] || 'fa-file';
}

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password strength
function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    if (strength <= 2) return 'weak';
    if (strength <= 4) return 'medium';
    return 'strong';
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Parse query string
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Set page title
function setPageTitle(title) {
    document.title = `${title} - KoloCloud`;
}

// Check if user is online (navigator.onLine)
function checkOnlineStatus() {
    return navigator.onLine;
}

// Event listeners for online/offline
window.addEventListener('online', () => {
    showNotification('З\'єднання відновлено', 'success');
});

window.addEventListener('offline', () => {
    showNotification('Втрачено з\'єднання', 'warning');
});

// Initialize tooltips on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 KoloCloud initialized');
    
    // Add CSRF token to all fetch requests if needed
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        if (args[1] && args[1].headers) {
            // Can add custom headers here if needed
        }
        return originalFetch.apply(this, args);
    };
});

// Export functions for use in other scripts
window.KoloCloud = {
    showNotification,
    logout,
    formatFileSize,
    formatDate,
    formatDateRelative,
    copyToClipboard,
    downloadTextAsFile,
    debounce,
    showLoading,
    confirmAction,
    getFileIcon,
    isValidEmail,
    checkPasswordStrength,
    escapeHtml,
    getQueryParam,
    setPageTitle,
    checkOnlineStatus
};
