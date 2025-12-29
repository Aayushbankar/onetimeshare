
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
    try:

        if not redis_service.get_file_metadata(token):
            return jsonify({"status": "error", "message": "File not found"}), 404   
        

        metadata = redis_service.get_file_metadata(token)
        uuid_filename = metadata['filename']
        original_filename = metadata['real_filename']
    
    # Step 3: Serve file safely
        response_file = send_from_directory(
        directory=Config.UPLOAD_FOLDER,
        path=uuid_filename,
        as_attachment=True,
        download_name=original_filename  # Shows original name to user
    )

        return response_file
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@bp.route('/download/<token>', methods=['GET'])
def render_download_page(token):
    try:


        if not redis_service.get_file_metadata(token):
            return jsonify({"status": "error", "message": "File not found"}), 404   
        

        metadata = redis_service.get_file_metadata(token)
        # return render_template('dl.html', metadata=metadata, token=token)/
        return render_template('dl.html', metadata=metadata, token=token)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
        