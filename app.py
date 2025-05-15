import os
import platform
import psutil
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort, Response
import secrets
import datetime
import uuid
import socket

# Create Flask app with correct template folder path
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "templates"))
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max file size

# Store shared links
# Format: {link_id: {path: path, password: password, expiry: datetime, readonly: True}}
shared_links = {}

# Store mounted storage devices
mounted_devices = {}

def get_system_drives():
    """Get list of available drives based on the operating system."""
    drives = []
    if platform.system() == "Windows":
        import win32api
        drives_list = win32api.GetLogicalDriveStrings()
        drives = [drive.rstrip('\\') for drive in drives_list.split('\x00') if drive]
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        # On Unix systems, get mounted devices
        partitions = psutil.disk_partitions(all=False)
        drives = [p.mountpoint for p in partitions]
    
    return drives

def get_local_ip():
    """Get the local IP address to help users share links properly."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route('/')
def index():
    """Home page showing the application interface."""
    return render_template('index.html')

@app.route('/select-storage', methods=['GET', 'POST'])
def select_storage():
    """Allow users to select a storage device or folder to share."""
    system_drives = get_system_drives()
    
    if request.method == 'POST':
        folder_path = request.form.get('folder_path')
        if not folder_path or not os.path.exists(folder_path):
            flash('Please select a valid folder path')
            return redirect(url_for('select_storage'))
        
        # Generate a unique ID for this share
        share_id = str(uuid.uuid4())
        
        # Store the selected path
        mounted_devices[share_id] = {
            'path': folder_path,
            'date_added': datetime.datetime.now(),
            'status': 'active'
        }
        
        flash(f'Storage "{folder_path}" has been mounted successfully!')
        return redirect(url_for('share_options', device_id=share_id))
    
    return render_template('select_storage.html', system_drives=system_drives)

@app.route('/share-options/<device_id>', methods=['GET', 'POST'])
def share_options(device_id):
    """Configure sharing options for a selected device."""
    if device_id not in mounted_devices:
        flash('Invalid device selected')
        return redirect(url_for('select_storage'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        # Convert hours to datetime
        hours = int(request.form.get('expiry_hours', 24))
        expiry_time = datetime.datetime.now() + datetime.timedelta(hours=hours)
        readonly = request.form.get('readonly', 'on') == 'on'
        
        # Generate a unique link ID
        link_id = str(uuid.uuid4())[:8]
        
        # Store link details
        shared_links[link_id] = {
            'device_id': device_id,
            'path': mounted_devices[device_id]['path'],
            'password': password,
            'expiry': expiry_time,
            'readonly': readonly,
            'created_at': datetime.datetime.now()
        }
        
        # Generate the actual shareable link
        local_ip = get_local_ip()
        share_url = f"http://{local_ip}:{request.host.split(':')[1] if ':' in request.host else '5000'}/shared/{link_id}"
        return render_template('link_created.html', link=share_url, link_id=link_id)
    
    return render_template('share_options.html', device_id=device_id)

@app.route('/shared/<link_id>', methods=['GET', 'POST'])
def access_shared(link_id):
    """Access a shared folder via a generated link."""
    # Check if link exists
    if link_id not in shared_links:
        abort(404, description="Link not found or has expired")
    
    link_info = shared_links[link_id]
    
    # Check if link has expired
    if datetime.datetime.now() > link_info['expiry']:
        # Remove expired link
        shared_links.pop(link_id)
        abort(410, description="This link has expired")
    
    # Check password if required
    if link_info['password'] and request.method == 'GET':
        return render_template('password_prompt.html', link_id=link_id)
    
    if link_info['password'] and request.method == 'POST':
        entered_password = request.form.get('password', '')
        if entered_password != link_info['password']:
            flash('Incorrect password')
            return render_template('password_prompt.html', link_id=link_id)
    
    # Get subfolder path if provided
    subfolder = request.args.get('subfolder', '')
    current_path = link_info['path']
    
    if subfolder:
        # Ensure the subfolder is within the shared directory (prevent path traversal)
        full_subfolder_path = os.path.normpath(os.path.join(current_path, subfolder))
        if not full_subfolder_path.startswith(os.path.normpath(current_path)):
            abort(403, description="Access denied - attempted path traversal")
        current_path = full_subfolder_path
    
    # List directory contents
    items = []
    
    try:
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            item_type = 'dir' if os.path.isdir(item_path) else 'file'
            
            # Get relative path for links
            rel_path = os.path.join(subfolder, item) if subfolder else item
            
            # Safely get size and modified time
            try:
                size = os.path.getsize(item_path) if not os.path.isdir(item_path) else 0
            except Exception:
                size = 0
            try:
                modified = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
            except Exception:
                modified = None
            
            items.append({
                'name': item,
                'is_dir': os.path.isdir(item_path),
                'size': size,
                'modified': modified,
                'path': rel_path,
                'is_media': any(item.lower().endswith(ext) for ext in ['.mp3', '.wav', '.ogg', '.mp4', '.webm', '.mov', '.jpg', '.jpeg', '.png', '.gif'])
            })
    except PermissionError:
        abort(403, description="Permission denied to access this directory")
    except FileNotFoundError:
        abort(404, description="Directory not found")
    
    # Sort items - directories first, then files
    items.sort(key=lambda x: (0 if x['is_dir'] else 1, x['name'].lower()))
    
    return render_template('browse_files.html', 
                          items=items, 
                          link_id=link_id, 
                          current_path=current_path,
                          subfolder=subfolder,
                          parent_folder=os.path.dirname(subfolder) if subfolder else None,
                          readonly=link_info['readonly'])

@app.route('/shared/<link_id>/download', methods=['GET'])
def download_file(link_id):
    """Download a file from a shared folder."""
    if link_id not in shared_links:
        abort(404, description="Link not found or has expired")
    
    link_info = shared_links[link_id]
    
    # Check if link has expired
    if datetime.datetime.now() > link_info['expiry']:
        # Remove expired link
        shared_links.pop(link_id)
        abort(410, description="This link has expired")
    
    try:
        # Get the file path from the request
        file_path = request.args.get('file', '')
        if not file_path:
            abort(400, description="No file specified")
        
        # Ensure the file is within the shared directory (prevent path traversal)
        full_path = os.path.normpath(os.path.join(link_info['path'], file_path))
        if not full_path.startswith(os.path.normpath(link_info['path'])):
            abort(403, description="Access denied - attempted path traversal")
        
        if not os.path.exists(full_path) or os.path.isdir(full_path):
            abort(404, description="File not found")
        
        directory = os.path.dirname(full_path)
        file = os.path.basename(full_path)
        return send_from_directory(directory, file, as_attachment=True)
    
    except Exception as e:
        abort(500, description=str(e))

@app.route('/shared/<link_id>/stream/<path:file_path>')
def stream_media(link_id, file_path):
    """Stream a media file from a shared folder."""
    if link_id not in shared_links:
        abort(404, description="Link not found or has expired")

    link_info = shared_links[link_id]

    if datetime.datetime.now() > link_info['expiry']:
        shared_links.pop(link_id)
        abort(410, description="This link has expired")

    try:
        full_path = os.path.normpath(os.path.join(link_info['path'], file_path))
        if not full_path.startswith(os.path.normpath(link_info['path'])):
            abort(403, description="Access denied - attempted path traversal")

        if not os.path.exists(full_path) or os.path.isdir(full_path):
            abort(404, description="File not found")

        # Determine MIME type
        mime_type = None
        if file_path.lower().endswith(('.mp4', '.mov', '.webm')):
            mime_type = 'video/' + file_path.split('.')[-1]
        elif file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
            mime_type = 'audio/' + file_path.split('.')[-1]
        elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            mime_type = 'image/' + file_path.split('.')[-1]
        
        if mime_type:
            return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path), mimetype=mime_type, as_attachment=False)
        else:
            # Fallback to download if not a recognized media type for streaming
            return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path), as_attachment=True)

    except Exception as e:
        app.logger.error(f"Error streaming file: {e}")
        abort(500, description=str(e))

@app.route('/shared/<link_id>/view/<path:file_path>')
def view_media_page(link_id, file_path):
    """Render a page to view a media file."""
    if link_id not in shared_links:
        abort(404, description="Link not found or has expired")

    link_info = shared_links[link_id]

    if datetime.datetime.now() > link_info['expiry']:
        shared_links.pop(link_id)
        abort(410, description="This link has expired")

    # Basic password check (if navigating directly to this page)
    if link_info['password'] and not request.cookies.get(f'password_verified_{link_id}'):
        # This is a simplified check. In a real app, you might redirect to password_prompt
        # or ensure the session/cookie is robustly set after password verification.
        flash("Password required to view this content.")
        return redirect(url_for('access_shared', link_id=link_id))

    media_type = None
    file_lower = file_path.lower()
    if any(file_lower.endswith(ext) for ext in ['.mp4', '.webm', '.mov', '.ogg']): # .ogg can be video too
        media_type = 'video'
    elif any(file_lower.endswith(ext) for ext in ['.mp3', '.wav', '.aac']):
        media_type = 'audio'
    elif any(file_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']):
        media_type = 'image'
    else:
        abort(400, description="Unsupported file type for viewing.")

    # Determine the parent folder for the 'Back to files' link
    # The file_path is relative to the shared root. 
    # If file_path is 'folder1/image.jpg', parent is 'folder1'
    # If file_path is 'image.jpg', parent is '' (root of the share)
    parent_folder = os.path.dirname(file_path)

    return render_template('view_media.html', 
                           link_id=link_id, 
                           file_path=file_path, 
                           file_name=os.path.basename(file_path),
                           media_type=media_type,
                           parent_folder=parent_folder)

@app.route('/dashboard')
def dashboard():
    """Dashboard showing all active shared links and mounted devices."""
    # Clean up expired links
    current_time = datetime.datetime.now()
    expired_links = [link_id for link_id, info in shared_links.items() if current_time > info['expiry']]
    for link_id in expired_links:
        shared_links.pop(link_id)
    
    # Calculate usage stats for mounted devices
    for device_id, info in mounted_devices.items():
        try:
            total, used, free = shutil.disk_usage(info['path'])
            info['total'] = total
            info['used'] = used
            info['free'] = free
            info['used_percent'] = round((used / total) * 100, 1)
        except:
            # If we can't get disk usage, set defaults
            info['total'] = 0
            info['used'] = 0
            info['free'] = 0
            info['used_percent'] = 0
    
    return render_template('dashboard.html', 
                          shared_links=shared_links, 
                          mounted_devices=mounted_devices,
                          current_time=current_time)

@app.route('/revoke/<link_id>')
def revoke_link(link_id):
    """Revoke a shared link."""
    if link_id in shared_links:
        shared_links.pop(link_id)
        flash('Link has been revoked successfully')
    else:
        flash('Link not found')
    return redirect(url_for('dashboard'))

@app.route('/unmount/<device_id>')
def unmount_device(device_id):
    """Unmount a shared device."""
    if device_id in mounted_devices:
        # Check if any active links are using this device
        active_links = [link_id for link_id, info in shared_links.items() 
                        if info['device_id'] == device_id and datetime.datetime.now() <= info['expiry']]
        
        if active_links:
            flash('Cannot unmount device with active shared links')
        else:
            mounted_devices.pop(device_id)
            flash('Device has been unmounted successfully')
    else:
        flash('Device not found')
    return redirect(url_for('dashboard'))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', error=error), 403

@app.errorhandler(410)
def gone(error):
    return render_template('error.html', error=error), 410

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=error), 500

if __name__ == '__main__':
    # Add libraries to requirements.txt if they don't exist
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    missing_packages = []
    if 'psutil' not in requirements:
        missing_packages.append('psutil')
    if platform.system() == "Windows" and 'pywin32' not in requirements:
        missing_packages.append('pywin32')
    
    if missing_packages:
        with open('requirements.txt', 'a') as f:
            for package in missing_packages:
                f.write(f'\n{package}')
    
    print(f"LFSP is running at http://{get_local_ip()}:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)