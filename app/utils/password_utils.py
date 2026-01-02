import bcrypt


class PasswordUtils:
    
    
    @staticmethod
    def hash_password(password):
        password = password.encode('utf-8')   
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password.decode('utf-8')

    @staticmethod  
    def check_hash(stored_hash,input_password):
        stored_hash = stored_hash.encode('utf-8')
        input_password = input_password.encode('utf-8')
        if bcrypt.checkpw(input_password,stored_hash):
            return True
        else:
            return False


    