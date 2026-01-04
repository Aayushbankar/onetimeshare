
from flask import Blueprint, current_app, request, jsonify, render_template
from config import Config
import os 

import redis
from datetime import datetime
from werkzeug.utils import secure_filename
import app.services.redis_service as redis_service
from app.utils.get_uuid import generate_uuid_and_filepath
from flask import send_from_directory
import re 

from app.utils.password_utils import PasswordUtils



from app.utils.serve_and_delete import serve_and_delete


bp = Blueprint('main', __name__)

redis_service = redis_service.RedisService(Config.REDIS_HOST, Config.REDIS_PORT, Config.REDIS_DB)

# redis_service.set_counter("file_count",0)
# redis_service.set_counter("uploads",0)
# redis_service.set_counter("downloads",0)
# redis_service.set_counter("deletions",0)


    
# redis_service.set_counter("/ - visits ",0)
# redis_service.set_counter("/upload - visits ",0)
# redis_service.set_counter("/download - visits ",0)
# redis_service.set_counter("/download - protected - visits ",0)
# redis_service.set_counter("/download - unprotected - visits ",0)
# redis_service.set_counter("/download - 404 - visits ",0)
# redis_service.set_counter("/download - 500 - visits ",0)
# redis_service.set_counter("/list-files - visits ",0)
# redis_service.set_counter("/info - visits ",0)







@bp.route('/')
def index():
    # redis_service.increment_counter("/ - visits ",1)
    redis_service.increment_counter("index_visits",1)
    return render_template('index.html')


@bp.route('/upload', methods=['POST'])
def upload_file():  
    try :
        # step 1 : file sanitation , genrating uuid and saving file
        file = request.files['file']
        file_name, filepath = generate_uuid_and_filepath(file)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True) 
        file.save(filepath)


        # step 1.1 check if the user has kept the passowrd settin gturned on / off 
        password = request.form.get('password')
        password_hash = None
        is_protected = False

        if password:
            password_hash = PasswordUtils.hash_password(password)
            is_protected = True



        # step 2 : store file metadata in redis
        metadata = {
            'filename': file_name,
            'real_filename': secure_filename(file.filename),
            'content_type': file.content_type,
            'token': file_name,
            'is_protected': str(is_protected),
            'password_hash': password_hash if password_hash else "",
            'attempt_to_unlock': '0'  # ← Changed to string!
        }
        
        redis_service.store_file_metadata( file_name, metadata)
        if redis_service.get_file_metadata(file_name):
            # redis_service.increment_counter("uploads",1)
            redis_service.increment_counter("uploads",1)
            return jsonify({"status": "success", "metadata": redis_service.get_file_metadata(file_name)}), 201
        else:
            return jsonify({"status": "error", "message": "Failed to upload file"}), 500

        

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/d/<token>', methods=['GET'])
def download_file(token):
    try :
        directory_path = current_app.config['UPLOAD_FOLDER']
        # metadata = redis_service.atomic_delete(token)
        metadata = redis_service.get_file_metadata(token)

        if not metadata:
            return jsonify({
                "status": "error",
                "error": "File not found or already downloaded  "
            }), 410

        uuid_file_name = metadata.get('filename')
        original_file_name = metadata.get('real_filename')
        if not uuid_file_name or not original_file_name:
            return jsonify({
                "status": "error",
                "error": "Invalid metadata"
            }), 500

        
        try :

            if metadata.get('is_protected') == 'True':
                redis_service.increment_counter("protected_downloads",1)
                return render_download_page(token)
            elif metadata.get('is_protected') == 'False':
                redis_service.increment_counter("unprotected_downloads",1)
                return serve_and_delete(uuid_file_name,original_file_name,directory_path,token,redis_service=redis_service)
            else:
                return jsonify({
                    "status": "error",
                    "error": "File is protected"
                }), 401
               

                
            
        

        except FileNotFoundError:
            current_app.logger.error(f"File not found on disk: {uuid_file_name}")
            return render_template('404.html'), 404

    except Exception as e:
        current_app.logger.error(f"Error in download route: {e}")
        return render_template('404.html'), 500





@bp.route('/download/<token>', methods=['GET'])
def render_download_page(token):
    """Render the download page with file metadata."""
    # redis_service.increment_counter("/download - visits ",1)
    try:
        metadata = redis_service.get_file_metadata(token)
        
        if not metadata:

            # redis_service.increment_counter("/download - 404 - visits ",1)
            return render_template('404.html'), 404
        

        if metadata.get('is_protected') == 'True':
            # redis_service.increment_counter("/download - protected - visits ",1)
            redis_service.increment_counter("protected_downloads_visits",1)
            return render_template('password.html', metadata=metadata, token=token)
        if metadata.get('is_protected') == 'False':
            # redis_service.increment_counter("/download - unprotected - visits ",1)
            redis_service.increment_counter("unprotected_downloads_visits",1)
            return render_template('dl.html', metadata=metadata, token=token)
        
    except Exception as e:
        current_app.logger.error(f"Error in download page route: {e}")
        return render_template('404.html'), 500







@bp.route('/verify/<token>', methods=['GET','POST'])
def verify_token(token):
    if request.method == 'GET':
        try:
            metadata = redis_service.get_file_metadata(token)
            if not metadata:
                return jsonify({"status": "error", "message": "File not found"}), 404
            return jsonify({"status": "success", "metadata": metadata}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == 'POST':
        try:
            # Get metadata
            metadata = redis_service.get_file_metadata(token)
            
            if not metadata:
                return render_template('404.html'), 404
            
            password = request.form.get('password')
            
            if not password:
                return render_template('password.html',
                                     token=token,
                                     error="Please enter a password"), 400
            
            stored_hash = metadata.get('password_hash')
            
            # Verify password
            if PasswordUtils.verify_password(password, stored_hash):
                # ✅ CORRECT PASSWORD
                # Reset attempt counter
                metadata['attempt_to_unlock'] = '0'
                redis_service.store_file_metadata(token, metadata)
                
                # Serve file
                redis_service.increment_counter("downloads", 1)
                return serve_and_delete(
                    metadata.get('filename'),
                    metadata.get('real_filename'),
                    current_app.config['UPLOAD_FOLDER'],
                    token,
                    redis_service=redis_service
                )
            
            else:
                # ❌ WRONG PASSWORD
                # Increment attempt counter
                current_attempts = int(metadata.get('attempt_to_unlock', 0))
                current_attempts += 1
                
                # Save updated count to Redis
                metadata['attempt_to_unlock'] = str(current_attempts)
                redis_service.store_file_metadata(token, metadata)
                
                # Check if max retries reached
                if current_attempts >= Config.MAX_RETRIES:
                    # Lock the file - max retries reached
                    return render_template('max_retries.html', 
                                         token=token,
                                         attempts=current_attempts), 403
                else:
                    # Show password form with attempts remaining
                    remaining = Config.MAX_RETRIES - current_attempts
                    return render_template('password.html',
                                         token=token,
                                         error=f"Incorrect password! {remaining} attempts remaining",
                                         attempts_used=current_attempts,
                                         max_attempts=Config.MAX_RETRIES), 403
        
        except Exception as e:
            current_app.logger.error(f"Error in verify route: {e}")
            return render_template('404.html'), 500


 


@bp.route('/test-redis')
def test_redis():
    try:
        r = current_app.redis_client
        hits = r.incr('hit_counter')
        return f"Hello! This page has been seen {hits} times. Redis is ALIVE."
    except Exception as e:
        return f"Redis Error: {str(e)}"


@bp.route('/list-files', methods=['GET'])
def list_files():
   try :
    if redis_service.list_files():
        # redis_service.increment_counter("/list-files - visits ",1)
        redis_service.increment_counter("list_files_visits",1)
        return jsonify({"status": "success", "files": redis_service.list_files()}), 200
    elif redis_service.list_files() is None:
        return jsonify({"status": "error", "message": "no files in the db"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to list files"}), 500
   except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/info/<token>', methods=['GET'])
def file_info(token):
   try :
    if redis_service.get_file_metadata(token):
        redis_service.increment_counter("info_visits", 1)
        return jsonify({"status": "success", "metadata": redis_service.get_file_metadata(token)}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to get file metadata"}), 500
   except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@bp.route('/admin/cleanup', methods=['POST'])
def cleanup_orphans():
    """
    Admin endpoint to clean up orphaned files.
    Deletes files that exist on disk but have no Redis metadata.
    """
    try:
        result = redis_service.cleanup_orphan_files()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/admin/cleanup-metadata', methods=['POST'])
def cleanup_orphan_metadata():
    """
    Admin endpoint to clean up orphaned Redis metadata.
    Deletes Redis keys that have no corresponding file on disk.
    """
    try:
        result = redis_service.cleanup_orphan_metadata()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask error handlers
@bp.app_errorhandler(404)
def page_not_found(e):
    """Handle 404 errors globally."""
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors globally."""
    current_app.logger.error(f"Internal server error: {e}")
    return render_template('404.html'), 500

@bp.route('/stats')
def stats():
    """Render stats dashboard HTML page"""
    stats_data = _get_stats_data()
    return render_template('stats.html', stats=stats_data)


@bp.route('/stats-json')
def stats_json():
    """Return stats as JSON for API/AJAX refresh"""
    return jsonify(_get_stats_data())


def _get_stats_data():
    """Helper to get all stats counters"""
    return {
        "uploads": redis_service.get_counter("uploads"),
        "downloads": redis_service.get_counter("downloads"),
        "deletions": redis_service.get_counter("deletions"),
        "index_visits": redis_service.get_counter("index_visits"),
        "list_files_visits": redis_service.get_counter("list_files_visits"),
        "info_visits": redis_service.get_counter("info_visits"),
        "protected_downloads": redis_service.get_counter("protected_downloads"),
        "unprotected_downloads": redis_service.get_counter("unprotected_downloads")
    }