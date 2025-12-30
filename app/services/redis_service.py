import typing
import redis 
from datetime import datetime
from config import Config
from redis import exceptions
import logging

import os 
from flask import current_app


class RedisService:

    exception = redis.exceptions
    logger = logging.getLogger(__name__)
    def __init__(self, host, port):
        self.redis_client = redis.Redis(host=host, port=port, db=0,decode_responses=True)

    def __check_connection(self):

        # helper fucntion to chekc of connetion is there before any fucntion cllas are donr 

        try:
            self.redis_client.ping()
            return True

        except self.exception.ConnectionError as e:
            self.logger.error(f"Redis connection error: {e}")
            return False
            
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return False

    def store_file_metadata(self , token, metadata) :
        # Store metadata for a file
        # Input: token (str), metadata (dict)
        # Returns: True if successful, False otherwise
        if self.__check_connection() :
            if not metadata is None :
                self.redis_client.hset(token, mapping={
                    "token": metadata['token'],
                    "filename": metadata['filename'],
                    "real_filename":metadata['real_filename'],
                    "content_type": metadata['content_type'],
                    "upload_time": datetime.utcnow().isoformat(),
                    "TIME_TO_LIVE": str(Config.REDIS_TTL) + " seconds",
                }) 
                self.redis_client.expire(token,str(Config.REDIS_TTL))
            
            return True
        else:
            self.logger.error("Redis connection error")
            return False
 

    def get_file_metadata(self, token) :
        # Get metadata for a file
        # Input: token (str)
        # Returns: metadata dict or None if not found
        if not token is None :
            return self.redis_client.hgetall(token)
        else:
            self.logger.error("Token is None")
            return None

    def delete_file(self, token) :
        # Delete a file
        # Input: token (str)
        # Returns: True if successful, False otherwise
        if not token is None :
                self.redis_client.delete(token)
                return True
        else:
            self.logger.error("Token is None")
            return False
      

    def file_exists(self, token) :
        # Check if a file exists
        # Input: token (str)
        # Returns: True if file exists, False otherwise
        if self.__check_connection() :
            if not token is None :
                return self.redis_client.exists(token) > 0
            else:
                self.logger.error("Token is None")
                return False

        else:
            self.logger.error("Redis connection error")
            return False

    def list_files(self):
        try:
            files = self.redis_client.keys('*')

            resposnse = {
                "redis_keys": files,
                "files": os.listdir(Config.UPLOAD_FOLDER)
            }
        
            return resposnse
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return str(e)



    def delete_all_keys(self):
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return False


    def delete_metadata(self, token):
        try :
            if self.__check_connection() :
                if self.redis_client.delete(token) > 0 :
                    return True
                else:
                    return False
            else:
                # self.logger.error("Redis connection error")
                return False
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return False
            

    def atomic_delete(self, token):
        try :
            if self.__check_connection() :
                pipeline = self.redis_client.pipeline()
                pipeline.watch(token)
            #    pipeline.multi()
                metadata = pipeline.hgetall(token)
                if metadata:
                    pipeline.multi()
                    pipeline.delete(token)
                    pipeline.execute()
                    return metadata
                else:
                    pipeline.unwatch()
                    return None
            else:
                # self.logger.error("Redis connection error")
                return None
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return None




    def delete_file_and_metadata(self,token):

        status = {
            "metadata_deleted": False,
            "file_deleted": False,
            "file_path": None,
            "file_name": None 
        }

        metadata = self.atomic_delete(token)
        if metadata is None :
            status["error"] = "File not found or already deleted"
            return status
        status["metadata_deleted"] = True
        try:
            file_name = metadata.get('filename')
            if not file_name:
                status["error"] = "Filename not in metadata"
                return status
            
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                status["file_deleted"] = True
                status["file_path"] = file_path
                status["file_name"] = file_name
                status["success"] = True
            else:
                status["error"] = "File not found on disk"
                
        except PermissionError as e:
            status["error"] = f"Permission denied: {e}"
        except Exception as e:
            status["error"] = f"Error deleting file: {e}"


    def cleanup_orphan_files(self):
        """
        Delete files from disk that have no metadata in Redis.
        This happens when TTL expires but file wasn't downloaded.
        """
        try:
            deleted_count = 0
            
            # Get all files on disk
            files_on_disk = os.listdir(current_app.config['UPLOAD_FOLDER'])
            
            # Get all Redis keys (tokens)
            redis_keys = set(self.redis_client.keys('*'))
            
            # Find orphaned files
            for filename in files_on_disk:
                # Extract token from filename (e.g., "abc123.pdf" → "abc123")
                token = os.path.splitext(filename)[0]
                
                # If token NOT in Redis → orphaned file!
                if token not in redis_keys:
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        self.logger.info(f"✅ Deleted orphan file: {filename}")
                    except Exception as e:
                        self.logger.error(f"Failed to delete orphan {filename}: {e}")
            
            self.logger.info(f"Cleanup complete: {deleted_count} orphan files deleted")
            return {
                "success": True,
                "deleted_count": deleted_count,
                "total_files_checked": len(files_on_disk)
            }
            




        except Exception as e:
            self.logger.error(f"Error in orphan cleanup: {e}")
            return {
                "success": False,
                "error": str(e)
            }


        
    def cleanup_orphan_metadata(self):
        """
        Delete Redis keys that have no corresponding file on disk.
        This happens when files are deleted but Redis data persists (e.g., Docker restart).
        """
        try:
            deleted_count = 0
            
            # Get all Redis keys
            redis_keys = self.redis_client.keys('*')
            
            # Get all files on disk
            files_on_disk = set(os.listdir(current_app.config['UPLOAD_FOLDER']))
            
            # Check each Redis key
            for key in redis_keys:
                # Get metadata to find filename
                metadata = self.redis_client.hgetall(key)
                
                if not metadata:
                    # Empty key, delete it
                    self.redis_client.delete(key)
                    deleted_count += 1
                    self.logger.info(f"Deleted empty key: {key}")
                    continue
                
                filename = metadata.get('filename')
                
                if not filename:
                    # No filename in metadata, delete it
                    self.redis_client.delete(key)
                    deleted_count += 1
                    self.logger.info(f"Deleted key with no filename: {key}")
                    continue
                
                # Check if file exists on disk
                if filename not in files_on_disk:
                    # File doesn't exist → orphaned metadata!
                    self.redis_client.delete(key)
                    deleted_count += 1
                    self.logger.info(f"✅ Deleted orphaned metadata: {key} (file: {filename})")
            
            self.logger.info(f"Metadata cleanup complete: {deleted_count} orphaned keys deleted")
            return {
                "success": True,
                "deleted_count": deleted_count,
                "total_keys_checked": len(redis_keys)
            }
            
        except Exception as e:
            self.logger.error(f"Error in metadata cleanup: {e}")
            return {
                "success": False,
                "error": str(e)
            }
