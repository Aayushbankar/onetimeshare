
import os
from typing import Generator
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from argon2.low_level import hash_secret_raw, Type
from config import Config





def generate_key():
    return os.urandom(32)




def generate_salt():
    return os.urandom(16)




def derive_key_from_password(password: str, salt: bytes) -> bytes:

    return hash_secret_raw(
        secret=password.encode('utf-8'),
        salt=salt,
        time_cost=Config.ARGON2_TIME_COST,
        memory_cost=Config.ARGON2_MEMORY_COST,
        parallelism=Config.ARGON2_PARALLELISM,
        hash_len=32,
        type=Type.ID 
    )



def _increment_nonce(base_nonce , counter):
    base_nonce = int.from_bytes(base_nonce, 'big')
    new_nonce_int = base_nonce ^ counter

    return new_nonce_int.to_bytes(12, 'big')



def encrypt_file_chunked(input_path, output_path, key) -> bytes:
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

def decrypt_file_chunked(input_path, key, base_nonce) -> Generator:
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