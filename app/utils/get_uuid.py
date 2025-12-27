import uuid
import os 
from config import Config
from flask import jsonify
import logging
from flask import request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileNotAllowedException(Exception):
    def __init__(self, message):
        self.message = message


class FileTooLargeException(Exception):
    def __init__(self, message):
        self.message = message


def check_file(file):
    try :
     

        #check teh file extenion from teh allowed extenions 

        if file.filename.rsplit('.', 1)[1].lower() not in Config.ALLOWED_EXTENSIONS:
            logger.error("File type not allowed")
            raise FileNotAllowedException("File type not allowed")
        #check if file size is less then 20 Mib

        if file.content_length > Config.MAX_FILE_SIZE:
            logger.error("File size too large")
            raise FileTooLargeException("File size too large")
        
    except Exception as e:
        logger.error(f"Error checking file: {str(e)}")
        raise FileNotAllowedException(f"Error checking file: {str(e)}")
    
    return file


def generate_uuid_and_filepath(file):
        logger.info("Generating UUID and file path")
        try:
            file = check_file(file)
            #generate a unique file name 
            file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            filepath = os.path.join(Config.UPLOAD_FOLDER, file_name)

            return file_name, filepath 
        except Exception as e:
            logger.error(f"Error generating UUID and file path: {str(e)}")
            raise FileNotAllowedException(f"Error generating UUID and file path: {str(e)}")
            
