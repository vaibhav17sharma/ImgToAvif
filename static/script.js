document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileCount = document.getElementById('fileCount');
    const convertBtn = document.getElementById('convertBtn');
    const modeInput = document.getElementById('modeInput');
    
    // Mode switching
    document.addEventListener('change', function(e) {
        if (e.target.name === 'mode') {
            const selectedMode = e.target.value;
            modeInput.value = selectedMode;
            
            if (selectedMode === 'avif') {
                document.getElementById('pageTitle').textContent = 'AVIF Converter';
                document.getElementById('pageSubtitle').textContent = 'Convert images to modern AVIF format';
                document.getElementById('uploadText').textContent = 'Drag & drop images here';
                document.getElementById('uploadHint').textContent = 'or click to browse';
                fileInput.accept = '.png,.jpg,.jpeg';
                convertBtn.textContent = 'Convert to AVIF';
            } else {
                document.getElementById('pageTitle').textContent = 'HEIC to PNG Converter';
                document.getElementById('pageSubtitle').textContent = 'Convert HEIC images to PNG format';
                document.getElementById('uploadText').textContent = 'Drag & drop HEIC files here';
                document.getElementById('uploadHint').textContent = 'or click to browse';
                fileInput.accept = '.heic,.heif';
                convertBtn.textContent = 'Convert to PNG';
            }
            
            fileInput.value = '';
            updateFileCount();
        }
    });

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
                img.onerror = () => {
                    img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5JbWFnZTwvdGV4dD48L3N2Zz4=';
                };
                try {
                    img.src = URL.createObjectURL(file);
                    img.onload = () => URL.revokeObjectURL(img.src);
                } catch (e) {
                    img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5JbWFnZTwvdGV4dD48L3N2Zz4=';
                }
                
                const fileName = document.createElement('div');
                fileName.className = 'file-name';
                fileName.textContent = file.name;
                
                const fileSize = document.createElement('div');
                fileSize.className = 'file-size';
                fileSize.textContent = formatFileSize(file.size);
                
                function formatFileSize(bytes) {
                    if (bytes === 0) return '0 Bytes';
                    const k = 1024;
                    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                }
                
                const fileType = document.createElement('div');
                fileType.className = 'file-type';
                const ext = file.name.split('.').pop().toUpperCase();
                fileType.textContent = file.type ? file.type.split('/')[1].toUpperCase() : ext;
                
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



    // Form submission via AJAX
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const mode = document.querySelector('input[name="mode"]:checked').value;
        convertBtn.textContent = mode === 'avif' ? 'Converting to AVIF...' : 'Converting to PNG...';
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
        formData.append('mode', modeInput.value);
        
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
        
        const mode2 = document.querySelector('input[name="mode"]:checked').value;
        convertBtn.textContent = mode2 === 'avif' ? 'Convert to AVIF' : 'Convert to PNG';
        convertBtn.disabled = false;
    });
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
                        <div class="stat-number">${results.files.length > 0 ? (results.files.reduce((sum, f) => sum + (isNaN(f.savings_percent) ? 0 : f.savings_percent), 0) / results.files.length).toFixed(1) : 0}%</div>
                        <div class="stat-label">${results.mode === 'avif' ? 'Average Savings' : 'Size Change'}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">${formatFileSize2(Math.abs(results.files.reduce((sum, f) => sum + (f.original_size - f.converted_size), 0)))}</div>
                        <div class="stat-label">${results.mode === 'avif' ? 'Total Saved' : 'Size Difference'}</div>
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
                                <div class="size-value">${formatFileSize2(file.original_size)}</div>
                            </div>
                            <div class="size-info">
                                <div class="size-label">${results.mode === 'avif' ? 'AVIF' : 'PNG'}</div>
                                <div class="size-value">${formatFileSize2(file.converted_size)}</div>
                            </div>
                        </div>
                        <div class="savings" style="${file.savings_percent < 0 ? 'background: linear-gradient(45deg, #ff9800, #f57c00);' : ''}">
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

function formatFileSize2(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
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