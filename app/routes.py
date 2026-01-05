
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
from functools import wraps


from app.utils.serve_and_delete import serve_and_delete


def handle_redis_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except redis.exceptions.ConnectionError as e:
            current_app.logger.error(f"Redis connection error: {e}")
            return jsonify({"error": "Redis connection error"}), 503

        except redis.exceptions.TimeoutError as e:
            current_app.logger.error(f"Redis timeout error: {e}")
            return jsonify({"error": "Redis timeout error"}), 504

        except redis.exceptions.ResponseError as e:
            current_app.logger.error(f"Redis response error: {e}")
            return jsonify({"error": "Redis response error"}), 500

        except redis.exceptions.WatchError as e:
            current_app.logger.error(f"Redis watch error: {e}")
            return jsonify({"error": "Redis watch error"}), 500


        except redis.RedisError as e:
            current_app.logger.error(f"Redis error: {e}")
            return jsonify({"error": "Redis error"}), 500

        except Exception as e:
            current_app.logger.error(f"Error: {e}")
            return jsonify({"error": "Internal server error"}), 500
    return wrapper
bp = Blueprint('main', __name__)







redis_service = redis_service.RedisService(Config.REDIS_HOST, Config.REDIS_PORT, Config.REDIS_DB)



@bp.route('/')
def index():
    # redis_service.increment_counter("/ - visits ",1)
    redis_service.increment_counter("index_visits",1)
    return render_template('index.html')


@bp.route('/upload', methods=['POST'])
@handle_redis_error
def upload_file():  
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




@bp.route('/d/<token>', methods=['GET'])
@handle_redis_error
def download_file(token):

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
            redis_service.delete_metadata(token)
            return render_template('404.html'), 404







@bp.route('/download/<token>', methods=['GET'])
@handle_redis_error
def render_download_page(token):
    """Render the download page with file metadata."""
    # redis_service.increment_counter("/download - visits ",1)

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
    







@bp.route('/verify/<token>', methods=['GET','POST'])
@handle_redis_error
def verify_token(token):
    if request.method == 'GET':

            metadata = redis_service.get_file_metadata(token)
            if not metadata:
                return jsonify({"status": "error", "message": "File not found"}), 404
            return jsonify({"status": "success", "metadata": metadata}), 200


    if request.method == 'POST':

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
        





# TODO: Add admin authentication before Day 13
# These routes should only be accessible by CLI-generated admin token
@bp.route('/list-files', methods=['GET'])
@handle_redis_error
def list_files():
    """Debug endpoint to list all files. TODO: Protect with admin auth."""
    files = redis_service.list_files()
    if files:
        redis_service.increment_counter("list_files_visits", 1)
        return jsonify({"status": "success", "files": files}), 200
    elif files is None or len(files) == 0:
        return jsonify({"status": "success", "message": "No files in the db", "files": []}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to list files"}), 500



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
        


# Flask error handlers
@bp.app_errorhandler(404)
def page_not_found(e):
    """Handle 404 errors globally."""
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors globally."""
    current_app.logger.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

# Error page route for JS redirects
@bp.route('/error/<int:code>')
def error_page(code):
    """Render error page for given status code."""
    templates = {
        400: '400.html',
        401: '401.html', 
        403: '403.html',
        404: '404.html',
        410: '410.html',
        500: '500.html',
        503: '503.html',
        504: '504.html'
    }
    template = templates.get(code, '500.html')
    return render_template(template), code

@bp.route('/stats')
def stats():
    """Render stats dashboard HTML page"""
    stats_data = _get_stats_data()
    return render_template('stats.html', stats=stats_data)


@bp.route('/stats-json')
@handle_redis_error
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