import bcrypt


class PasswordUtils:
    
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        password_bytes = password.encode('utf-8')   
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')

    @staticmethod  
    def check_hash(stored_hash: str, input_password: str) -> bool:
        """Verify a password against a stored hash."""
        stored_hash_bytes = stored_hash.encode('utf-8')
        input_password_bytes = input_password.encode('utf-8')
        return bcrypt.checkpw(input_password_bytes, stored_hash_bytes)


    @staticmethod
    def verify_password(password: str, metadata_hash: str) -> bool:
        """Helper to verify metadata hash."""
        if not metadata_hash:
            return False
        return PasswordUtils.check_hash(metadata_hash, password)