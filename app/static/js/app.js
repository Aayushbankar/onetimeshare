/**
 * OneTimeShare - Upload Page JavaScript
 * Day 4 Final Version - Polished and Clean
 * 
 * Work Split:
 * - Professor: Boilerplate, UI helpers
 * - Aayush: Validation, file handling, upload logic (with autocomplete)
 */

document.addEventListener('DOMContentLoaded', () => {
    // =========================================================
    // DOM ELEMENTS
    // =========================================================
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const removeFile = document.getElementById('remove-file');
    const progressContainer = document.getElementById('progress-container');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadBtnText = document.getElementById('upload-btn-text');
    const uploadSection = document.getElementById('upload-section');
    const successSection = document.getElementById('success-section');
    const errorSection = document.getElementById('error-section');
    const shareLink = document.getElementById('share-link');
    const copyBtn = document.getElementById('copy-btn');
    const uploadAnother = document.getElementById('upload-another');
    const errorMessage = document.getElementById('error-message');
    const tryAgain = document.getElementById('try-again');
    
    // Password Elements
    const usePassword = document.getElementById('use-password');
    const passwordContainer = document.getElementById('password-container');
    const filePassword = document.getElementById('file-password');
    const togglePassword = document.getElementById('toggle-password');

    // =========================================================
    // CONFIG
    // =========================================================
    const ALLOWED_EXTENSIONS = ['pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'env','md'];
    const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB
    
    let selectedFile = null;

    // =========================================================
    // PASSWORD LOGIC (Added by AI Mentor)
    // =========================================================
    
    // Toggle Password Field Visibility
    usePassword.addEventListener('change', (e) => {
        if (e.target.checked) {
            passwordContainer.classList.remove('hidden');
            filePassword.focus();
        } else {
            passwordContainer.classList.add('hidden');
            filePassword.value = ''; // Clear password if unchecked
        }
    });

    // Toggle Password Text Visibility (Eye Icon)
    togglePassword.addEventListener('click', () => {
        const type = filePassword.getAttribute('type') === 'password' ? 'text' : 'password';
        filePassword.setAttribute('type', type);
        togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
    });

    // =========================================================
    // DROP ZONE INTERACTIONS
    // =========================================================
    
    // Click to open file picker (but not if clicking the label/button which handles itself)
    dropZone.addEventListener('click', (e) => {
        // Don't trigger if clicking on label or its children (label already triggers file input)
        if (e.target.tagName === 'LABEL' || e.target.closest('label')) {
            return;
        }
        fileInput.click();
    });

    // Drag over - required for drop to work
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    // Drag enter - visual feedback
    dropZone.addEventListener('dragenter', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-active');
    });

    // Drag leave - remove visual feedback
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-active');
    });

    // Drop - handle the dropped file
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-active');
        const file = e.dataTransfer.files[0];
        if (file) handleFileSelect(file);
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFileSelect(file);
    });

    // =========================================================
    // FILE VALIDATION (Aayush coded)
    // =========================================================
    function validateFile(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        
        if (!ALLOWED_EXTENSIONS.includes(ext)) {
            return { 
                valid: false, 
                error: `File type ".${ext}" not allowed. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}` 
            };
        }
        
        if (file.size > MAX_FILE_SIZE) {
            return { 
                valid: false, 
                error: `File too large (${formatFileSize(file.size)}). Maximum: 20 MB` 
            };
        }
        
        return { valid: true, error: null };
    }

    // =========================================================
    // FILE SELECT HANDLER (Aayush coded)
    // =========================================================
    function handleFileSelect(file) {
        const validation = validateFile(file);
        
        if (!validation.valid) {
            showError(validation.error);
            return;
        }
        
        // Store selected file
        selectedFile = file;
        
        // Update UI
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.classList.remove('hidden');
        dropZone.classList.add('hidden');
        uploadBtn.disabled = false;
    }

    // =========================================================
    // REMOVE FILE (Aayush coded)
    // =========================================================
    removeFile.addEventListener('click', () => {
        selectedFile = null;
        fileInfo.classList.add('hidden');
        dropZone.classList.remove('hidden');
        uploadBtn.disabled = true;
        fileInput.value = '';
    });

    // =========================================================
    // UPLOAD FILE (Aayush coded with autocomplete)
    // =========================================================
    uploadBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Disable button and show progress
        uploadBtn.disabled = true;
        uploadBtnText.textContent = 'UPLOADING...';
        progressContainer.classList.remove('hidden');
        progressFill.style.width = '10%';
        progressText.textContent = '10%';

        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Add Password if enabled
        if (usePassword.checked) {
            const password = filePassword.value;
            if (!password || password.length < 8) {
                showError("Password must be at least 8 characters long.");
                uploadBtn.disabled = false;
                uploadBtnText.textContent = 'UPLOAD SECURELY';
                progressContainer.classList.add('hidden');
                return;
            }
            formData.append('password', password);
        }

        try {
            // Simulate progress (fetch doesn't support upload progress easily)
            progressFill.style.width = '50%';
            progressText.textContent = '50%';

            // Make the request
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            // Complete progress
            progressFill.style.width = '100%';
            progressText.textContent = '100%';

            // Small delay for visual feedback
            await new Promise(resolve => setTimeout(resolve, 300));

            // Handle error responses (non-2xx status codes)
            if (!response.ok) {
                // Server returned an error - redirect to error page
                window.location.href = `/error/${response.status}`;
                return;
            }

            // Parse successful JSON response
            const data = await response.json();

            // Handle result
            if (data.status === 'success') {
                const link = window.location.origin + '/download/' + data.metadata.token;
                const isProtected = data.metadata.is_protected === 'True';
                showSuccess(link, isProtected);
            } else {
                showError(data.message || 'Upload failed');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        }
    });

    // =========================================================
    // UI STATE FUNCTIONS
    // =========================================================
    
    function showSuccess(link, isProtected = false) {
        uploadSection.classList.add('hidden');
        successSection.classList.remove('hidden');
        shareLink.value = link;
        
        // Show/hide protected badge
        const protectedBadge = document.getElementById('protected-badge');
        if (protectedBadge) {
            if (isProtected) {
                protectedBadge.classList.remove('hidden');
            } else {
                protectedBadge.classList.add('hidden');
            }
        }
    }

    function showError(message) {
        uploadSection.classList.add('hidden');
        errorSection.classList.remove('hidden');
        errorMessage.textContent = message;
    }

    function resetUI() {
        // Show upload section
        uploadSection.classList.remove('hidden');
        successSection.classList.add('hidden');
        errorSection.classList.add('hidden');
        
        // Reset file state
        selectedFile = null;
        fileInput.value = '';
        fileInfo.classList.add('hidden');
        dropZone.classList.remove('hidden');
        
        // Reset button
        uploadBtn.disabled = true;
        uploadBtnText.textContent = 'UPLOAD SECURELY';
        
        // Reset progress
        progressFill.style.width = '0%';
        progressText.textContent = '0%';
        progressContainer.classList.add('hidden');
        
        // Reset password field
        if (usePassword) {
            usePassword.checked = false;
            passwordContainer.classList.add('hidden');
            filePassword.value = '';
        }
        
        // Hide protected badge
        const protectedBadge = document.getElementById('protected-badge');
        if (protectedBadge) protectedBadge.classList.add('hidden');
        
        // Hide copy toast
        const copyToast = document.getElementById('copy-toast');
        if (copyToast) copyToast.classList.add('hidden');
    }

    // =========================================================
    // COPY TO CLIPBOARD
    // =========================================================
    copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(shareLink.value);
            showCopySuccess();
        } catch (err) {
            // Fallback for older browsers
            shareLink.select();
            document.execCommand('copy');
            showCopySuccess();
        }
    });
    
    function showCopySuccess() {
        const copyBtnText = document.getElementById('copy-btn-text');
        const copyToast = document.getElementById('copy-toast');
        
        // Update button text
        if (copyBtnText) {
            copyBtnText.textContent = '✓ COPIED!';
            setTimeout(() => { copyBtnText.textContent = '📋 COPY'; }, 2000);
        }
        
        // Show toast
        if (copyToast) {
            copyToast.classList.remove('hidden');
            setTimeout(() => { copyToast.classList.add('hidden'); }, 2000);
        }
    }

    // =========================================================
    // RESET HANDLERS
    // =========================================================
    uploadAnother.addEventListener('click', resetUI);
    tryAgain.addEventListener('click', resetUI);

    // =========================================================
    // HELPER FUNCTIONS
    // =========================================================
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
});
