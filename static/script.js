const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileCount = document.getElementById('fileCount');
const convertBtn = document.getElementById('convertBtn');

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    fileInput.files = e.dataTransfer.files;
    updateFileCount();
});

fileInput.addEventListener('change', updateFileCount);

function updateFileCount() {
    const count = fileInput.files.length;
    const filePreview = document.getElementById('filePreview');
    const fileList = document.getElementById('fileList');
    
    if (count > 0) {
        fileCount.textContent = `${count} file${count > 1 ? 's' : ''} selected`;
        convertBtn.disabled = false;
        
        // Show file preview
        filePreview.style.display = 'block';
        fileList.innerHTML = '';
        
        Array.from(fileInput.files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            
            // Create image preview
            const img = document.createElement('img');
            img.className = 'file-preview-img';
            img.src = URL.createObjectURL(file);
            img.onload = () => URL.revokeObjectURL(img.src);
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            fileName.textContent = file.name;
            
            const fileSize = document.createElement('div');
            fileSize.className = 'file-size';
            fileSize.textContent = formatFileSize(file.size);
            
            const fileType = document.createElement('div');
            fileType.className = 'file-type';
            fileType.textContent = file.type.split('/')[1].toUpperCase();
            
            fileItem.appendChild(img);
            fileItem.appendChild(fileName);
            fileItem.appendChild(fileSize);
            fileItem.appendChild(fileType);
            fileList.appendChild(fileItem);
        });
    } else {
        fileCount.textContent = '';
        convertBtn.disabled = true;
        filePreview.style.display = 'none';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form submission via AJAX
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    convertBtn.textContent = 'Converting...';
    convertBtn.disabled = true;
    
    // Clear any existing flash messages
    const flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
    
    const formData = new FormData();
    Array.from(fileInput.files).forEach(file => {
        formData.append('files', file);
    });
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResults(result);
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('Upload failed: ' + error.message);
    }
    
    convertBtn.textContent = 'Convert to AVIF';
    convertBtn.disabled = false;
});

function showResults(results) {
    // Hide upload section
    document.querySelector('form').style.display = 'none';
    document.querySelector('.features').style.display = 'none';
    document.querySelector('.stats').style.display = 'none';
    
    // Show results
    const resultsHTML = `
        <div class="results-section">
            <div class="success-icon">🎉</div>
            <h2>Conversion Complete!</h2>
            
            <div class="summary">
                <div class="summary-title">Successfully converted ${results.files.length} file${results.files.length > 1 ? 's' : ''}</div>
                <div class="summary-stats">
                    <div class="stat">
                        <div class="stat-number">${(results.files.reduce((sum, f) => sum + f.savings_percent, 0) / results.files.length).toFixed(1)}%</div>
                        <div class="stat-label">Average Savings</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">${formatFileSize(results.files.reduce((sum, f) => sum + (f.original_size - f.converted_size), 0))}</div>
                        <div class="stat-label">Total Saved</div>
                    </div>
                </div>
            </div>
            
            <div class="cleanup-timer">
                ⏰ Files will be auto-deleted in: <span class="timer-value" id="cleanupTimer">10:00</span>
            </div>
            
            <div class="files-grid">
                ${results.files.map(file => `
                    <div class="file-card">
                        <img src="/download/${file.filename}" class="result-preview-img" alt="${file.filename}">
                        <div class="file-name">${file.filename}</div>
                        <div class="file-sizes">
                            <div class="size-info">
                                <div class="size-label">Original</div>
                                <div class="size-value">${formatFileSize(file.original_size)}</div>
                            </div>
                            <div class="size-info">
                                <div class="size-label">AVIF</div>
                                <div class="size-value">${formatFileSize(file.converted_size)}</div>
                            </div>
                        </div>
                        <div class="savings">
                            ${file.savings_percent > 0 ? 
                                `🎯 ${file.savings_percent.toFixed(1)}% smaller` : 
                                `📈 ${(-file.savings_percent).toFixed(1)}% larger`
                            }
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div class="download-section">
                ${results.is_batch ? 
                    '<a href="/download_batch" class="download-btn">📦 Download All as ZIP</a>' :
                    `<a href="/download/${results.files[0].filename}" class="download-btn">⬇️ Download ${results.files[0].filename}</a>`
                }
                <button onclick="location.reload()" class="download-btn back-btn">🔄 Convert More Files</button>
            </div>
            
            ${results.errors && results.errors.length > 0 ? `
                <div class="errors">
                    <div class="error-title">⚠️ Some files couldn't be converted:</div>
                    ${results.errors.map(error => `<div class="error-item">${error}</div>`).join('')}
                </div>
            ` : ''}
        </div>
    `;
    
    document.querySelector('.container').insertAdjacentHTML('beforeend', resultsHTML);
    
    // Start cleanup timer
    startCleanupTimer();
}

function showError(message) {
    const errorHTML = `
        <div class="flash-messages">
            <div class="flash-message error">${message}</div>
        </div>
    `;
    document.querySelector('.container').insertAdjacentHTML('afterbegin', errorHTML);
}

// Cleanup timer function
function startCleanupTimer() {
    let timeLeft = 600; // 10 minutes in seconds
    const timerElement = document.getElementById('cleanupTimer');
    
    const timer = setInterval(() => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        if (timeLeft <= 0) {
            clearInterval(timer);
            timerElement.textContent = 'Files deleted';
            timerElement.parentElement.style.background = 'rgba(220, 53, 69, 0.1)';
            timerElement.parentElement.style.borderColor = '#dc3545';
        }
        
        timeLeft--;
    }, 1000);
}

// Clear flash messages on page load after 5 seconds
window.addEventListener('load', () => {
    setTimeout(() => {
        const flashMessages = document.querySelector('.flash-messages');
        if (flashMessages) {
            flashMessages.style.opacity = '0';
            flashMessages.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                flashMessages.style.display = 'none';
            }, 500);
        }
    }, 5000);
});