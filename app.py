import math
import shutil
from flask import Flask, request, render_template, send_file, flash, redirect, url_for, session, after_this_request
from PIL import Image
import pillow_avif
import pillow_heif
import os
import io
import zipfile
import uuid
import tempfile
import math
from werkzeug.utils import secure_filename

# Register HEIF opener
pillow_heif.register_heif_opener()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max total size

CONVERTED_FOLDER = 'converted'

# Create directories if they don't exist
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename, mode='avif'):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if mode == 'avif':
        return ext in ['png', 'jpg', 'jpeg']
    elif mode == 'png':
        return ext in ['heic', 'heif']
    elif mode == 'compress':
        return ext in ['png', 'jpg', 'jpeg']
    return False

import time
import threading

def cleanup_old_files():
    """Clean up folders older than 10 minutes"""
    current_time = time.time()
    if os.path.exists(CONVERTED_FOLDER):
        for batch_id in os.listdir(CONVERTED_FOLDER):
            batch_path = os.path.join(CONVERTED_FOLDER, batch_id)
            if os.path.isdir(batch_path):
                # Check if the folder itself is old
                if current_time - os.path.getctime(batch_path) > 600:
                    try:
                        shutil.rmtree(batch_path)
                    except:
                        pass
            elif os.path.isfile(batch_path) and batch_id.startswith('converted_') and batch_id.endswith('.zip'):
                # Clean up temporary zip files
                if current_time - os.path.getctime(batch_path) > 300: # 5 minutes for zips
                    try:
                        os.remove(batch_path)
                    except:
                        pass

def start_cleanup_thread():
    def run_cleanup():
        while True:
            cleanup_old_files()
            time.sleep(60)
    
    thread = threading.Thread(target=run_cleanup, daemon=True)
    thread.start()

# Start background cleanup
if not os.environ.get('WERKZEUG_RUN_MAIN'): # Prevent double-start in debug mode
    start_cleanup_thread()

# ... (start_cleanup_thread remains same, just ensuring it calls this updated version)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return upload_ajax()
    else:
        return upload_form()

def upload_ajax():
    files = request.files.getlist('files')
    mode = request.form.get('mode', 'avif')
    
    if not files or all(f.filename == '' for f in files):
        return {'success': False, 'error': 'No files selected'}
    
    batch_id = str(uuid.uuid4())[:12]
    batch_folder = os.path.join(CONVERTED_FOLDER, batch_id)
    os.makedirs(batch_folder, exist_ok=True)
    
    converted_files = []
    errors = []
    skipped = []
    
    for file in files:
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename, mode):
            skipped.append(file.filename)
            continue
        filename = secure_filename(file.filename)
        try:
            file.stream.seek(0)
            original_size = len(file.read())
            file.stream.seek(0)
            img = Image.open(file.stream)
            img.verify()
            file.stream.seek(0)
            img = Image.open(file.stream)
            
            base_name = filename.rsplit('.', 1)[0]
            if mode == 'avif':
                if img.mode in ('LA', 'P'):
                    img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
                output_filename = f"{base_name}.avif"
                output_path = os.path.join(batch_folder, output_filename)
                img.save(output_path, 'AVIF', lossless=True)
            elif mode == 'png':
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                output_filename = f"{base_name}.png"
                output_path = os.path.join(batch_folder, output_filename)
                img.save(output_path, 'PNG')
            elif mode == 'compress':
                original_ext = filename.rsplit('.', 1)[1].lower()
                if original_ext in ['jpg', 'jpeg']:
                    if img.mode in ('RGBA', 'LA'): img = img.convert('RGB')
                    output_filename = f"{base_name}.jpg"
                    output_path = os.path.join(batch_folder, output_filename)
                    img.save(output_path, 'JPEG', quality=95, optimize=True)
                else:
                    output_filename = f"{base_name}.png"
                    output_path = os.path.join(batch_folder, output_filename)
                    img.save(output_path, 'PNG', optimize=True)
            
            converted_size = os.path.getsize(output_path)
            savings_percent = ((original_size - converted_size) / original_size) * 100
            
            converted_files.append({
                'filename': output_filename,
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
        'batch_id': batch_id,
        'files': converted_files,
        'errors': errors,
        'skipped': skipped,
        'is_batch': len(converted_files) > 1,
        'mode': mode
    }

def upload_form():
    mode = request.form.get('mode', 'avif')
    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        flash('No files selected')
        return redirect(url_for('index'))
    
    batch_id = str(uuid.uuid4())[:12]
    batch_folder = os.path.join(CONVERTED_FOLDER, batch_id)
    os.makedirs(batch_folder, exist_ok=True)
    
    converted_files = []
    errors = []
    skipped = []
    
    for file in files:
        if not file or not file.filename: continue
        if not allowed_file(file.filename, mode):
            skipped.append(file.filename)
            continue
        filename = secure_filename(file.filename)
        try:
            file.stream.seek(0)
            original_size = len(file.read())
            file.stream.seek(0)
            img = Image.open(file.stream)
            img.verify()
            file.stream.seek(0)
            img = Image.open(file.stream)
            base_name = filename.rsplit('.', 1)[0]
            if mode == 'avif':
                if img.mode in ('LA', 'P'):
                    img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
                output_filename = f"{base_name}.avif"
                output_path = os.path.join(batch_folder, output_filename)
                img.save(output_path, 'AVIF', lossless=True)
            elif mode == 'png':
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                output_filename = f"{base_name}.png"
                output_path = os.path.join(batch_folder, output_filename)
                img.save(output_path, 'PNG')
            else:
                original_ext = filename.rsplit('.', 1)[1].lower()
                if original_ext in ['jpg', 'jpeg']:
                    if img.mode in ('RGBA', 'LA'): img = img.convert('RGB')
                    output_filename = f"{base_name}.jpg"
                    output_path = os.path.join(batch_folder, output_filename)
                    img.save(output_path, 'JPEG', quality=95, optimize=True)
                else:
                    output_filename = f"{base_name}.png"
                    output_path = os.path.join(batch_folder, output_filename)
                    img.save(output_path, 'PNG', optimize=True)
            
            converted_size = os.path.getsize(output_path)
            converted_files.append({
                'filename': output_filename,
                'original_name': filename,
                'original_size': original_size,
                'converted_size': converted_size,
                'savings_percent': ((original_size - converted_size) / original_size) * 100
            })
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    if not converted_files:
        flash('No files were converted successfully')
        return redirect(url_for('index'))

    return render_template('index.html', results={
        'batch_id': batch_id,
        'files': converted_files,
        'errors': errors,
        'skipped': skipped,
        'is_batch': len(converted_files) > 1,
        'mode': mode
    })

@app.route('/download/<batch_id>/<filename>')
def download_file(batch_id, filename):
    file_path = os.path.join(CONVERTED_FOLDER, batch_id, filename)
    if os.path.exists(file_path):
        should_download = request.args.get('download') == '1'
        return send_file(file_path, as_attachment=should_download, download_name=filename)
    return redirect(url_for('index'))

@app.route('/download_batch/<batch_id>')
def download_batch(batch_id):
    batch_folder = os.path.join(CONVERTED_FOLDER, batch_id)
    if not os.path.exists(batch_folder):
        return redirect(url_for('index'))
        
    zip_filename = f'converted_{batch_id}.zip'
    zip_path = os.path.join(CONVERTED_FOLDER, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(batch_folder):
                file_path = os.path.join(batch_folder, filename)
                zipf.write(file_path, filename)
        
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
    except Exception as e:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/clear_files/<batch_id>', methods=['POST'])
def clear_files(batch_id):
    batch_folder = os.path.join(CONVERTED_FOLDER, batch_id)
    try:
        if os.path.exists(batch_folder):
            import shutil
            shutil.rmtree(batch_folder)
        return {'success': True}
    except:
        return {'success': False}

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 100MB total.')
    return redirect(url_for('index'))

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    # Handle negative sizes (for size increases)
    prefix = "-" if size_bytes < 0 else ""
    size_bytes = abs(size_bytes)
    
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{prefix}{s} {size_names[i]}"

# Make format_file_size available in templates
app.jinja_env.globals.update(format_file_size=format_file_size)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)