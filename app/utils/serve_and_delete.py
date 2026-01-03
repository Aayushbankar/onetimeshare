import flask 
from flask import send_from_directory
import os 
from app.services.redis_service import RedisService
from flask import current_app
import logging




def serve_and_delete(uuid_file_name,original_file_name,directory_path,token,redis_service):


    response = send_from_directory(
                    directory=directory_path,
                    path=uuid_file_name,
                    as_attachment=True,
                    download_name=original_file_name
                )
    redis_service.atomic_delete(token)
    file_path = os.path.join(directory_path, uuid_file_name)

    try :
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"✅ Deleted file: {uuid_file_name}")
        else:
            logging.warning(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Failed to delete: {e}")      
        # Don't fail the request!

    return response 