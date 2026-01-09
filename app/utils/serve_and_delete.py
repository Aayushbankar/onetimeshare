"""
serve_and_delete.py - Streaming decrypted file download with cleanup

Day 16-17: Encryption/Decryption Implementation
"""
import os
import logging
import base64
from flask import Response
from app.utils.encryption_utils import decrypt_file_chunked, derive_key_from_password


def serve_and_delete(uuid_file_name, original_file_name, directory_path,
                     token, redis_service, password, metadata):
    """
    Stream decrypted file to client, then cleanup.
    
    Args:
        uuid_file_name: Token-based filename on disk
        original_file_name: Original filename for download
        directory_path: Upload folder path
        token: File token for Redis
        redis_service: Redis service instance
        password: Password for decryption (None if not protected)
        metadata: File metadata from Redis
    """
    file_path = os.path.join(directory_path, uuid_file_name)
    
    # Get decryption key
    if metadata.get("encryption_salt"):
        salt = bytes.fromhex(metadata["encryption_salt"])
        key = derive_key_from_password(password, salt)
    else:
        key = base64.b64decode(metadata["encryption_key"])
    
    base_nonce = bytes.fromhex(metadata.get("encryption_nonce"))
    
    # Generator with cleanup in finally
    def generate():
        try:
            for chunk in decrypt_file_chunked(file_path, key, base_nonce):
                yield chunk
        finally:
            # Cleanup AFTER streaming completes
            redis_service.atomic_delete(token)
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"✅ Deleted file: {uuid_file_name}")
            redis_service.increment_counter("downloads", 1)
            redis_service.increment_counter("deletions", 1)
    
    # Return Response (OUTSIDE generator)
    return Response(
        generate(),
        mimetype=metadata.get('content_type', 'application/octet-stream'),
        headers={
            'Content-Disposition': f'attachment; filename="{original_file_name}"'
        }
    )