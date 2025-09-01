from flask import Flask, request, render_template, send_file, flash, redirect, url_for, session
from PIL import Image
import pillow_avif
import os
import io
import zipfile
import uuid
import tempfile
import math
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max total size

CONVERTED_FOLDER = 'converted'

# Create directories if they don't exist
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ['png', 'jpg', 'jpeg']

def cleanup_old_files():
    """Clean up files older than 10 minutes"""
    import time
    current_time = time.time()
    for folder in [CONVERTED_FOLDER]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath) and current_time - os.path.getctime(filepath) > 600:
                    try:
                        os.remove(filepath)
                    except:
                        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request - return JSON
        return upload_ajax()
    else:
        # Regular form submission - return HTML
        return upload_form()

def upload_ajax():
    # Handle AJAX upload and return JSON response
    cleanup_old_files()
    
    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        return {'success': False, 'error': 'No files selected'}
    
    if len(files) > 50:
        return {'success': False, 'error': 'Maximum 50 files allowed per batch'}
    
    converted_files = []
    errors = []
    skipped = []
    
    for file in files:
        if not file or not file.filename:
            continue
            
        if not allowed_file(file.filename):
            skipped.append(file.filename)
            continue
            
        filename = secure_filename(file.filename)
        if not filename:
            skipped.append(file.filename)
            continue
            
        try:
            # Reset file pointer
            file.stream.seek(0)
            original_size = len(file.read())
            file.stream.seek(0)
            
            # Validate image
            img = Image.open(file.stream)
            img.verify()
            
            # Reset and reopen for conversion
            file.stream.seek(0)
            img = Image.open(file.stream)
            
            # Convert to RGB only for non-transparent formats
            if img.mode in ('LA', 'P'):
                if 'transparency' in img.info:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
            # Keep RGBA for transparent PNGs
            
            # Keep original filename, just change extension
            base_name = filename.rsplit('.', 1)[0]
            avif_filename = f"{base_name}.avif"
            
            # Ensure converted folder exists
            os.makedirs(CONVERTED_FOLDER, exist_ok=True)
            avif_path = os.path.join(CONVERTED_FOLDER, avif_filename)
            
            img.save(avif_path, 'AVIF', lossless=True)
            
            # Get converted file size
            converted_size = os.path.getsize(avif_path)
            savings_percent = ((original_size - converted_size) / original_size) * 100
            
            converted_files.append({
                'filename': avif_filename,
                'original_name': filename,
                'original_size': original_size,
                'converted_size': converted_size,
                'savings_percent': savings_percent
            })
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    if not converted_files:
        return {'success': False, 'error': 'No files were converted successfully'}
    
    return {
        'success': True,
        'files': converted_files,
        'errors': errors,
        'skipped': skipped,
        'is_batch': len(converted_files) > 1
    }

def upload_form():
    cleanup_old_files()
    
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        flash('No files selected')
        return redirect(url_for('index'))
    
    if len(files) > 50:
        flash('Maximum 50 files allowed per batch')
        return redirect(url_for('index'))
    
    converted_files = []
    errors = []
    skipped = []
    
    for file in files:
        if not file or not file.filename:
            continue
            
        if not allowed_file(file.filename):
            skipped.append(file.filename)
            continue
            
        filename = secure_filename(file.filename)
        if not filename:
            skipped.append(file.filename)
            continue
            
        try:
            # Reset file pointer
            file.stream.seek(0)
            original_size = len(file.read())
            file.stream.seek(0)
            
            # Validate image
            img = Image.open(file.stream)
            img.verify()
            
            # Reset and reopen for conversion
            file.stream.seek(0)
            img = Image.open(file.stream)
            
            # Convert to RGB only for non-transparent formats
            if img.mode in ('LA', 'P'):
                if 'transparency' in img.info:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
            # Keep RGBA for transparent PNGs
            
            # Keep original filename, just change extension
            base_name = filename.rsplit('.', 1)[0]
            avif_filename = f"{base_name}.avif"
            
            # Ensure converted folder exists
            os.makedirs(CONVERTED_FOLDER, exist_ok=True)
            avif_path = os.path.join(CONVERTED_FOLDER, avif_filename)
            
            img.save(avif_path, 'AVIF', lossless=True)
            
            # Get converted file size
            converted_size = os.path.getsize(avif_path)
            savings_percent = ((original_size - converted_size) / original_size) * 100
            
            converted_files.append({
                'path': avif_path,
                'filename': avif_filename,
                'original_name': filename,
                'original_size': original_size,
                'converted_size': converted_size,
                'savings_percent': savings_percent
            })
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    # Show summary messages
    if errors:
        for error in errors[:5]:  # Show max 5 errors
            flash(f'Error: {error}')
        if len(errors) > 5:
            flash(f'... and {len(errors) - 5} more errors')
    
    if skipped:
        flash(f'Skipped {len(skipped)} unsupported files')
    
    if not converted_files:
        flash('No files were converted successfully')
        return redirect(url_for('index'))
    
    # Show results on the same page (fallback for non-JS)
    return render_template('index.html', 
                         results={
                             'files': converted_files,
                             'errors': errors,
                             'skipped': skipped,
                             'is_batch': len(converted_files) > 1
                         })

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(CONVERTED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return redirect(url_for('index'))

@app.route('/download_batch')
def download_batch():
    # Create zip for batch download
    zip_filename = f'converted_images_{str(uuid.uuid4())[:8]}.zip'
    zip_path = os.path.join(CONVERTED_FOLDER, zip_filename)
    
    # Get all AVIF files from converted folder
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(CONVERTED_FOLDER):
                if filename.endswith('.avif'):
                    file_path = os.path.join(CONVERTED_FOLDER, filename)
                    zipf.write(file_path, filename)
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    except Exception as e:
        flash(f'Error creating zip file: {str(e)}')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 100MB total.')
    return redirect(url_for('index'))

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

# Make format_file_size available in templates
app.jinja_env.globals.update(format_file_size=format_file_size)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)