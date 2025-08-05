/**
 * TomatoHealth - Main JavaScript File
 * Interactive features and utilities for the tomato disease detection app
 */

// ===========================
// Global Variables
// ===========================

const TomatoHealth = {
    // Configuration
    config: {
        animationDuration: 300,
        fadeInDelay: 100,
        maxFileSize: 5 * 1024 * 1024, // 5MB
        allowedFileTypes: ['image/jpeg', 'image/jpg', 'image/png']
    },
    
    // State management
    state: {
        isUploading: false,
        currentFile: null,
        uploadProgress: 0
    }
};

// ===========================
// Utility Functions
// ===========================

/**
 * Debounce function to limit the rate of function calls
 */
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

/**
 * Format file size in human readable format
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Validate file type and size
 */
function validateFile(file) {
    const errors = [];
    
    // Check file type
    if (!TomatoHealth.config.allowedFileTypes.includes(file.type)) {
        errors.push('Please select a JPG, JPEG, or PNG image file.');
    }
    
    // Check file size
    if (file.size > TomatoHealth.config.maxFileSize) {
        errors.push(`File size must be less than ${formatFileSize(TomatoHealth.config.maxFileSize)}.`);
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast element if it doesn't exist
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = new bootstrap.Toast(document.getElementById(toastId));
    toastElement.show();
    
    // Remove toast element after it's hidden
    document.getElementById(toastId).addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Animate elements on scroll
 */
function animateOnScroll() {
    const elements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animation = element.dataset.animate;
                
                element.style.animation = `${animation} 0.6s ease forwards`;
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Smooth scroll to element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ===========================
// Form Enhancements
// ===========================

/**
 * Enhanced form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation, .auth-form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('input', function() {
                validateInput(this);
            });
            
            input.addEventListener('blur', function() {
                validateInput(this);
            });
        });
    });
}

/**
 * Validate individual input field
 */
function validateInput(input) {
    const isValid = input.checkValidity();
    const feedbackElement = input.parentElement.querySelector('.invalid-feedback');
    
    if (isValid) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        
        if (feedbackElement) {
            feedbackElement.textContent = input.validationMessage;
        }
    }
    
    return isValid;
}

/**
 * Password strength indicator
 */
function initPasswordStrength() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        if (input.name === 'password' || input.id === 'password') {
            const strengthIndicator = createPasswordStrengthIndicator();
            input.parentElement.appendChild(strengthIndicator);
            
            input.addEventListener('input', function() {
                updatePasswordStrength(this, strengthIndicator);
            });
        }
    });
}

function createPasswordStrengthIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'password-strength mt-2';
    indicator.innerHTML = `
        <div class="progress" style="height: 6px;">
            <div class="progress-bar" role="progressbar" style="width: 0%"></div>
        </div>
        <small class="text-muted strength-text">Enter a password</small>
    `;
    return indicator;
}

function updatePasswordStrength(input, indicator) {
    const password = input.value;
    const progressBar = indicator.querySelector('.progress-bar');
    const strengthText = indicator.querySelector('.strength-text');
    
    let strength = 0;
    let text = 'Weak';
    let color = 'bg-danger';
    
    if (password.length >= 6) strength += 1;
    if (password.match(/[a-z]/)) strength += 1;
    if (password.match(/[A-Z]/)) strength += 1;
    if (password.match(/[0-9]/)) strength += 1;
    if (password.match(/[^a-zA-Z0-9]/)) strength += 1;
    
    switch (strength) {
        case 0:
        case 1:
            text = 'Very Weak';
            color = 'bg-danger';
            break;
        case 2:
            text = 'Weak';
            color = 'bg-warning';
            break;
        case 3:
            text = 'Medium';
            color = 'bg-info';
            break;
        case 4:
            text = 'Strong';
            color = 'bg-success';
            break;
        case 5:
            text = 'Very Strong';
            color = 'bg-success';
            break;
    }
    
    const percentage = (strength / 5) * 100;
    progressBar.style.width = percentage + '%';
    progressBar.className = `progress-bar ${color}`;
    strengthText.textContent = text;
}

// ===========================
// Image Upload Enhancements
// ===========================

/**
 * Enhanced drag and drop functionality
 */
function initDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]') || 
                         document.getElementById('fileInput');
        
        if (!fileInput) return;
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, () => highlight(area), false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, () => unhighlight(area), false);
        });
        
        // Handle dropped files
        area.addEventListener('drop', (e) => handleDrop(e, fileInput), false);
        
        // Handle click to open file dialog
        area.addEventListener('click', (e) => {
            if (e.target === area || e.target.closest('.upload-content')) {
                fileInput.click();
            }
        });
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(area) {
    area.classList.add('drag-over');
}

function unhighlight(area) {
    area.classList.remove('drag-over');
}

function handleDrop(e, fileInput) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        processFile(files[0], fileInput);
    }
}

/**
 * Process uploaded file
 */
function processFile(file, fileInput) {
    const validation = validateFile(file);
    
    if (!validation.isValid) {
        validation.errors.forEach(error => {
            showToast(error, 'danger');
        });
        return;
    }
    
    // Update file input
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;
    
    // Create preview
    createImagePreview(file);
    
    // Update UI
    showUploadPreview();
    
    TomatoHealth.state.currentFile = file;
    showToast(`File "${file.name}" uploaded successfully!`, 'success');
}

/**
 * Create image preview
 */
function createImagePreview(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const previewImg = document.getElementById('previewImg');
        const fileName = document.getElementById('fileName');
        
        if (previewImg) {
            previewImg.src = e.target.result;
            previewImg.style.animation = 'fadeIn 0.5s ease';
        }
        
        if (fileName) {
            fileName.textContent = `${file.name} (${formatFileSize(file.size)})`;
        }
    };
    
    reader.readAsDataURL(file);
}

/**
 * Show upload preview section
 */
function showUploadPreview() {
    const uploadArea = document.getElementById('uploadArea');
    const imagePreview = document.getElementById('imagePreview');
    
    if (uploadArea && imagePreview) {
        uploadArea.classList.add('d-none');
        imagePreview.classList.remove('d-none');
        imagePreview.style.animation = 'fadeIn 0.5s ease';
    }
}

/**
 * Reset upload form
 */
function resetUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const imagePreview = document.getElementById('imagePreview');
    const fileInput = document.getElementById('fileInput');
    const previewImg = document.getElementById('previewImg');
    const fileName = document.getElementById('fileName');
    
    if (uploadArea) uploadArea.classList.remove('d-none');
    if (imagePreview) imagePreview.classList.add('d-none');
    if (fileInput) fileInput.value = '';
    if (previewImg) previewImg.src = '';
    if (fileName) fileName.textContent = '';
    
    TomatoHealth.state.currentFile = null;
}

// Make resetUpload available globally
window.resetUpload = resetUpload;

// ===========================
// Loading States
// ===========================

/**
 * Show loading spinner on buttons
 */
function showButtonLoading(button, text = 'Loading...') {
    if (!button.dataset.originalText) {
        button.dataset.originalText = button.innerHTML;
    }
    
    button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
    button.disabled = true;
}

/**
 * Hide loading spinner on buttons
 */
function hideButtonLoading(button) {
    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
        delete button.dataset.originalText;
    }
    button.disabled = false;
}

/**
 * Form submission with loading state
 */
function initFormSubmission() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            
            if (submitButton && !this.querySelector('.is-invalid')) {
                const loadingText = submitButton.dataset.loading || 'Processing...';
                showButtonLoading(submitButton, loadingText);
                
                // For file uploads, show additional progress
                if (this.enctype === 'multipart/form-data') {
                    TomatoHealth.state.isUploading = true;
                    showUploadProgress();
                }
            }
        });
    });
}

function showUploadProgress() {
    // You can enhance this to show actual upload progress
    // For now, we'll show a modal
    const modal = document.getElementById('loadingModal');
    if (modal) {
        const loadingModal = new bootstrap.Modal(modal);
        loadingModal.show();
    }
}

// ===========================
// Statistics Animations
// ===========================

/**
 * Animate numbers on dashboard
 */
function animateNumbers() {
    const numberElements = document.querySelectorAll('[data-count]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    numberElements.forEach(element => {
        observer.observe(element);
    });
}

function animateNumber(element) {
    const target = parseInt(element.dataset.count || element.textContent);
    const duration = 2000; // 2 seconds
    const start = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(progress * target);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target;
        }
    }
    
    requestAnimationFrame(update);
}

// ===========================
// Theme Switching (Optional)
// ===========================

/**
 * Initialize theme switching
 */
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Add theme toggle if needed
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// ===========================
// Performance Optimizations
// ===========================

/**
 * Lazy load images
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Preload critical resources
 */
function preloadCriticalResources() {
    // Preload common icons and images
    const criticalResources = [
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2'
    ];
    
    criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'font';
        link.type = 'font/woff2';
        link.crossOrigin = 'anonymous';
        link.href = resource;
        document.head.appendChild(link);
    });
}

// ===========================
// Error Handling
// ===========================

/**
 * Global error handler
 */
function initErrorHandling() {
    window.addEventListener('error', function(e) {
        console.error('JavaScript Error:', e.error);
        showToast('An unexpected error occurred. Please refresh the page.', 'danger');
    });
    
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled Promise Rejection:', e.reason);
        showToast('An error occurred while processing your request.', 'danger');
    });
}

// ===========================
// Accessibility Enhancements
// ===========================

/**
 * Keyboard navigation support
 */
function initKeyboardNavigation() {
    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) modal.hide();
            }
        }
    });
    
    // Focus management for forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const firstInput = form.querySelector('input, select, textarea');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    });
}

/**
 * ARIA live region updates
 */
function updateAriaLiveRegion(message) {
    let liveRegion = document.getElementById('ariaLiveRegion');
    if (!liveRegion) {
        liveRegion = document.createElement('div');
        liveRegion.id = 'ariaLiveRegion';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);
    }
    
    liveRegion.textContent = message;
}

// ===========================
// Initialization
// ===========================

/**
 * Initialize all features when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('TomatoHealth: Initializing application...');
    
    // Core features
    initFormValidation();
    initFormSubmission();
    initDragAndDrop();
    
    // Enhancements
    initPasswordStrength();
    initTheme();
    initKeyboardNavigation();
    initErrorHandling();
    
    // Performance
    initLazyLoading();
    preloadCriticalResources();
    
    // Animations
    animateOnScroll();
    animateNumbers();
    
    console.log('TomatoHealth: Application initialized successfully!');
});

// ===========================
// Service Worker Registration (Optional)
// ===========================

/**
 * Register service worker for offline support
 */
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Export for use in other modules
window.TomatoHealth = TomatoHealth;