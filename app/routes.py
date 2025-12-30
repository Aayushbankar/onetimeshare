
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





bp = Blueprint('main', __name__)

redis_service = redis_service.RedisService(Config.REDIS_HOST, Config.REDIS_PORT, )


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/upload', methods=['POST'])
def upload_file():  
    try :
        # step 1 : file sanitation , genrating uuid and saving file
        file = request.files['file']
        file_name, filepath = generate_uuid_and_filepath(file)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True) 
        file.save(filepath)

        # step 2 : store file metadata in redis
        metadata = {
            'filename': file_name,
            'real_filename': secure_filename(file.filename),
            'content_type': file.content_type,
            'token': file_name
        }
        
        redis_service.store_file_metadata( file_name, metadata)
        if redis_service.get_file_metadata(file_name):
            return jsonify({"status": "success", "metadata": redis_service.get_file_metadata(file_name)}), 201
        else:
            return jsonify({"status": "error", "message": "Failed to upload file"}), 500

        

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/d/<token>', methods=['GET'])
def download_file(token):
    try :
        directory_path = current_app.config['UPLOAD_FOLDER']
        metadata = redis_service.atomic_delete(token)

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
            response = send_from_directory(
                directory=directory_path,
                path=uuid_file_name,
                as_attachment=True,
                download_name=original_file_name
            )

            
            file_path = os.path.join(directory_path, uuid_file_name)

            try :
                if os.path.exists(file_path):
                    os.remove(file_path)
                    current_app.logger.info(f"✅ Deleted file: {uuid_file_name}")
                else:
                    current_app.logger.warning(f"File not found: {file_path}")
            except Exception as e:
                current_app.logger.error(f"Failed to delete: {e}")
                # Don't fail the request!

            return response

        except FileNotFoundError:
            current_app.logger.error(f"File not found on disk: {uuid_file_name}")
            return jsonify({
                "status": "error",
                "error": "File not found on disk"
            }), 404

    except Exception as e:
        current_app.logger.error(f"Error in download route: {e}")
        return render_template('404.html'), 500

@bp.route('/download/<token>', methods=['GET'])
def render_download_page(token):
    """Render the download page with file metadata."""
    try:
        metadata = redis_service.get_file_metadata(token)
        
        if not metadata:
            return render_template('404.html'), 404
        
        return render_template('dl.html', metadata=metadata, token=token)
        
    except Exception as e:
        current_app.logger.error(f"Error in download page route: {e}")
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
