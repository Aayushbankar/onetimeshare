
import os
from typing import Generator
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from argon2.low_level import hash_secret_raw, Type
from config import Config





def generate_key() -> bytes:
    return os.urandom(32)




def generate_salt() -> bytes:
    return os.urandom(16)




def derive_key_from_password(password: str, salt: bytes) -> bytes:
    '''
    Derive a key from a password using Argon2
    '''
    return hash_secret_raw(
        secret=password.encode('utf-8'),
        salt=salt,
        time_cost=Config.ARGON2_TIME_COST,
        memory_cost=Config.ARGON2_MEMORY_COST,
        parallelism=Config.ARGON2_PARALLELISM,
        hash_len=32,
        type=Type.ID 
    )



def _increment_nonce(base_nonce: bytes, counter: int) -> bytes:
    '''
    Increment a nonce by a counter value
    '''
    base_int = int.from_bytes(base_nonce, 'big')
    new_int = base_int + counter
    # Handle overflow (96-bit limit)
    if new_int > (1 << 96) - 1:
        raise OverflowError("Nonce overflow")
    return new_int.to_bytes(12, 'big')



def encrypt_file_chunked(input_path: str, output_path: str, key: bytes) -> bytes:
    '''
    Encrypt a file using ChaCha20Poly1305
    '''
    base_nonce = os.urandom(12)  # Random per file!
    cipher = ChaCha20Poly1305(key)

    # with open(input_path, 'rb') as f:
    #     chunk_num = 0
    #     while True :
    #         chunk = f.read(64 * 1024)
    #         if not(chunk):
    #             break
    #         else:
    #             chunk_nonce = _increment_nonce(base_nonce, chunk_num)
    #             encrypted = cipher.encrypt(chunk_nonce, chunk, None)
    #             chunk_num += 1
                

    with open(input_path,'rb') as infile , open(output_path,'wb') as outfile:
        chunk_num = 0
        while True:
            chunk = infile.read(64 * 1024)
            if not(chunk):
                break
            else:
                chunk_nonce = _increment_nonce(base_nonce, chunk_num)
                encrypted = cipher.encrypt(chunk_nonce, chunk, None)
                chunk_num += 1
                length_bytes = len(encrypted).to_bytes(4, 'big')
                outfile.write(length_bytes + encrypted)

    return base_nonce

def decrypt_file_chunked(input_path: str, key: bytes, base_nonce: bytes) -> Generator[bytes, None, None]:
    '''
    Decrypt a file using ChaCha20Poly1305
    '''
    cipher = ChaCha20Poly1305(key)
    with open (input_path, 'rb') as f:
        chunk_num = 0
        while True:
            length_bytes = f.read(4)
            if not(length_bytes):
                break

            chunk_length = int.from_bytes(length_bytes, 'big')
            chunk = f.read(chunk_length)
            chunk_nonce = _increment_nonce(base_nonce, chunk_num)
            decrypted = cipher.decrypt(chunk_nonce, chunk, None)
            chunk_num += 1
            yield decrypted