from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from PIL import Image
import pillow_avif
import os
import io
import zipfile
import uuid
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max total size

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ['png', 'jpg', 'jpeg']

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    import time
    current_time = time.time()
    for folder in [CONVERTED_FOLDER]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath) and current_time - os.path.getctime(filepath) > 3600:
                try:
                    os.remove(filepath)
                except:
                    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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
            
            # Validate image
            img = Image.open(file.stream)
            img.verify()
            
            # Reset and reopen for conversion
            file.stream.seek(0)
            img = Image.open(file.stream)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Generate unique filename to avoid conflicts
            base_name = filename.rsplit('.', 1)[0]
            unique_id = str(uuid.uuid4())[:8]
            avif_filename = f"{base_name}_{unique_id}.avif"
            avif_path = os.path.join(CONVERTED_FOLDER, avif_filename)
            
            img.save(avif_path, 'AVIF', lossless=True, quality=100)
            converted_files.append((avif_path, avif_filename, filename))
            
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
    
    if len(converted_files) == 1:
        flash(f'Successfully converted 1 file to AVIF (lossless)!')
        return send_file(converted_files[0][0], as_attachment=True, download_name=converted_files[0][1])
    
    # Create zip for multiple files with unique name
    zip_filename = f'converted_images_{str(uuid.uuid4())[:8]}.zip'
    zip_path = os.path.join(CONVERTED_FOLDER, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, avif_filename, original_name in converted_files:
                # Use original name structure in zip
                zip_entry_name = original_name.rsplit('.', 1)[0] + '.avif'
                zipf.write(file_path, zip_entry_name)
        
        flash(f'Successfully converted {len(converted_files)} files to AVIF (lossless)!')
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    except Exception as e:
        flash(f'Error creating zip file: {str(e)}')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 100MB total.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)