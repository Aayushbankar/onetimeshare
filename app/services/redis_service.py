import typing
import redis 
from datetime import datetime
from config import Config
from redis import exceptions
import logging


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
                return self.redis_client.exists(token)
            else:
                self.logger.error("Token is None")
                return False

        else:
            self.logger.error("Redis connection error")
            return False

    def list_files(self):
        try:
            files = self.redis_client.keys('*')
            return files
        except Exception as e:
            self.logger.error(f"Redis connection error: {e}")
            return str(e)