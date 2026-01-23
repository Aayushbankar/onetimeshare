import typing
import redis 
from datetime import datetime
from config import Config
from redis import exceptions
import logging
import time

import os 
from flask import current_app


class RedisService:

    exception = redis.exceptions
    logger = logging.getLogger(__name__)
    
    # Class-level cache for connection status
    _connection_checked = False
    _connection_available = False
    _last_check_time = 0
    _check_interval = 30  # Re-check every 30 seconds
    
    def __init__(self, host: str, port: int, db: int = 0) -> None:
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def __check_connection(self):
        """Check Redis connection with caching to prevent log spam."""
        current_time = time.time()
        
        # Return cached result if checked recently
        if RedisService._connection_checked and (current_time - RedisService._last_check_time) < RedisService._check_interval:
            return RedisService._connection_available
        
        try:
            self.redis_client.ping()
            RedisService._connection_available = True
            RedisService._connection_checked = True
            RedisService._last_check_time = current_time
            return True

        except self.exception.ConnectionError as e:
            if not RedisService._connection_checked:
                self.logger.error(f"Redis connection error: {e}")
            RedisService._connection_available = False
            RedisService._connection_checked = True
            RedisService._last_check_time = current_time
            return False
            
        except Exception as e:
            if not RedisService._connection_checked:
                self.logger.error(f"Redis connection error: {e}")
            RedisService._connection_available = False
            RedisService._connection_checked = True
            RedisService._last_check_time = current_time
            return False


    def store_file_metadata(self, token: str, metadata: dict) -> bool:
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
                    "password_hash": metadata['password_hash'],
                    "is_protected": metadata['is_protected'],
                    "attempt_to_unlock": metadata.get('attempt_to_unlock', '0'),  # ← ADD THIS!
                    "TIME_TO_LIVE": str(Config.REDIS_TTL) + " seconds",
                    "is_encrypted": metadata.get("is_encrypted", "True"),
                    "encryption_nonce": metadata.get("encryption_nonce", ""),
                    "encryption_key": metadata.get("encryption_key", ""),
                    "encryption_salt": metadata.get("encryption_salt", ""),
                }) 
                self.redis_client.expire(token,str(Config.REDIS_TTL))
            
            return True
        else:
            self.logger.error("Redis connection error")
            return False
 

    def get_file_metadata(self, token: str) -> typing.Optional[dict]:
        # Get metadata for a file
        # Input: token (str)
        # Returns: metadata dict or None if not found
        if not token is None :
            return self.redis_client.hgetall(token)
        else:
            self.logger.error("Token is None")
            return None

    def delete_file(self, token: str) -> bool:
        # Delete a file
        # Input: token (str)
        # Returns: True if successful, False otherwise
        if not token is None :
                self.redis_client.delete(token)
                return True
        else:
            self.logger.error("Token is None")
            return False
      

    def file_exists(self, token: str) -> bool:
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
        '''
        List all files in the upload folder and redis keys
        '''
        try:
            files = self.redis_client.keys('*')

            resposnse = {
                "redis_keys": files,
                "files": os.listdir(Config.UPLOAD_FOLDER)
            }
        
            return resposnse
            return resposnse
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return str(e)


    def increment_file_attempt(self, token: str) -> int:
        '''
        Atomically increment the attempt_to_unlock counter for a file.
        Returns the new value.
        '''
        try:
            if self.__check_connection():
                return self.redis_client.hincrby(token, "attempt_to_unlock", 1)
            return 9999 # Fail closed if redis down
        except Exception as e:
            self.logger.error(f"Redis error incrementing attempt: {e}")
            return 9999



    def delete_all_keys(self):
        '''
        Delete all keys in redis
        '''
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return False


    def delete_metadata(self, token: str) -> bool:
        '''
        Delete metadata from redis
        '''
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
                metadata = self.redis_client.hgetall(token)
                try:
                    if metadata:
                        pipeline.multi()
                        pipeline.delete(token)
                        pipeline.execute()
                        return metadata
                    else:
                        pipeline.unwatch()
                        return None
                except redis.exceptions.WatchError:
                    self.logger.error(f"Redis error: WatchError")
                    return None
                except Exception as e:
                    self.logger.error(f"Redis connection error: {e}")
                    return None
            else:
                # self.logger.error("Redis connection error")
                return None
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return None
        finally :
            pipeline.reset()



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
            
            # Get all Redis keys (tokens)
            redis_keys = set(self.redis_client.keys('*'))
            
            total_files_checked = 0
            
            # Find orphaned files
            with os.scandir(current_app.config['UPLOAD_FOLDER']) as it:
                for entry in it:
                    if not entry.is_file():
                        continue
                        
                    total_files_checked += 1
                    filename = entry.name
                    
                    # Extract token from filename (e.g., "abc123.pdf" → "abc123")
                    token = os.path.splitext(filename)[0]
                    
                    # If token NOT in Redis → orphaned file!
                    if token not in redis_keys:
                        file_path = entry.path
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
                "total_files_checked": total_files_checked
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
            
            # REMOVED: listdir call to prevent OOM
            # We will check os.path.exists for each key instead
            
            # Check each Redis key
            for key in redis_keys:
                # Check if key is a hash before calling hgetall()
                key_type = self.redis_client.type(key)
                
                if key_type != 'hash':
                    # Skip non-hash keys (not file metadata)
                    continue
                
                # Get metadata to find filename
                try:
                    metadata = self.redis_client.hgetall(key)
                except Exception as e:
                    self.logger.warning(f"Could not get metadata for {key}: {e}")
                    continue
                
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
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(file_path):
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




    def increment_counter(self, key: str, count: int) -> bool:
        """Increment counter by 1"""
        try :
            if not self.__check_connection():
                return False
            self.redis_client.incrby(key,count)
            return True
        except Exception as e:
            self.logger.error(f"Error incrementing counter: {e}")   
            return False
    def decrement_counter(self, key: str, count: int) -> bool:
        """Decrement counter by 1"""
        try :
            if not self.__check_connection():
                return False
            self.redis_client.decrby(key,count)
            return True
        except Exception as e:
            self.logger.error(f"Error decrementing counter: {e}")   
            return False

    def set_counter(self, counter_name, value):
        """Set counter to specific value"""
        try :
            if not self.__check_connection():
                return False
            self.redis_client.set(counter_name, value)
            return True
        except Exception as e:
            self.logger.error(f"Error setting counter: {e}")   
            return False

    def get_counter(self, counter_name):
        try:
            if not self.__check_connection():
                return 0
            value = self.redis_client.get(counter_name)
            return int(value) if value else 0
        except:
            return 0