"""
Day 16: Encryption Unit Tests

Pass 4 Note: AI-written tests because user was lazy 😅
This is documented as a learning moment in 11_Pass_4_Notes.md
"""
import os
import sys
import pytest
import tempfile
from cryptography.exceptions import InvalidTag

# Add project root to path BEFORE imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock Config before importing encryption_utils
class MockConfig:
    ARGON2_TIME_COST = 1  # Fast for testing
    ARGON2_MEMORY_COST = 1024  # Low memory for testing
    ARGON2_PARALLELISM = 1

# Patch config module
import config
config.Config = MockConfig

# Now import using direct file import to avoid app/__init__.py
import importlib.util
spec = importlib.util.spec_from_file_location(
    "encryption_utils", 
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "utils", "encryption_utils.py")
)
encryption_utils = importlib.util.module_from_spec(spec)

# Patch config in the module's namespace before loading
sys.modules['config'] = type(sys)('config')
sys.modules['config'].Config = MockConfig

spec.loader.exec_module(encryption_utils)

generate_key = encryption_utils.generate_key
generate_salt = encryption_utils.generate_salt
derive_key_from_password = encryption_utils.derive_key_from_password
encrypt_file_chunked = encryption_utils.encrypt_file_chunked
decrypt_file_chunked = encryption_utils.decrypt_file_chunked
_increment_nonce = encryption_utils._increment_nonce


class TestKeyGeneration:
    """Test key generation functions."""
    
    def test_key_is_32_bytes(self):
        """Key must be 32 bytes (256 bits)."""
        key = generate_key()
        assert len(key) == 32
    
    def test_key_is_bytes(self):
        """Key must be bytes type."""
        key = generate_key()
        assert isinstance(key, bytes)
    
    def test_keys_are_unique(self):
        """Each generation produces different key."""
        key1 = generate_key()
        key2 = generate_key()
        assert key1 != key2


class TestSaltGeneration:
    """Test salt generation."""
    
    def test_salt_is_16_bytes(self):
        """Salt must be 16 bytes."""
        salt = generate_salt()
        assert len(salt) == 16
    
    def test_salts_are_unique(self):
        """Each generation produces different salt."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        assert salt1 != salt2


class TestKeyDerivation:
    """Test Argon2id key derivation."""
    
    def test_derivation_is_deterministic(self):
        """Same password + salt = same key."""
        salt = generate_salt()
        key1 = derive_key_from_password("mypassword", salt)
        key2 = derive_key_from_password("mypassword", salt)
        assert key1 == key2
    
    def test_different_passwords_different_keys(self):
        """Different passwords produce different keys."""
        salt = generate_salt()
        key1 = derive_key_from_password("password1", salt)
        key2 = derive_key_from_password("password2", salt)
        assert key1 != key2
    
    def test_different_salts_different_keys(self):
        """Different salts produce different keys."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        key1 = derive_key_from_password("same", salt1)
        key2 = derive_key_from_password("same", salt2)
        assert key1 != key2
    
    def test_derived_key_is_32_bytes(self):
        """Derived key must be 32 bytes."""
        key = derive_key_from_password("test", generate_salt())
        assert len(key) == 32


class TestNonceIncrement:
    """Test nonce management."""
    
    def test_nonce_is_deterministic(self):
        """Same base + counter = same result."""
        base = os.urandom(12)
        nonce1 = _increment_nonce(base, 5)
        nonce2 = _increment_nonce(base, 5)
        assert nonce1 == nonce2
    
    def test_nonce_is_unique_per_counter(self):
        """Different counters produce different nonces."""
        base = os.urandom(12)
        nonces = [_increment_nonce(base, i) for i in range(10)]
        assert len(set(nonces)) == 10  # All unique
    
    def test_nonce_is_12_bytes(self):
        """Nonce must be 12 bytes."""
        base = os.urandom(12)
        nonce = _increment_nonce(base, 42)
        assert len(nonce) == 12


class TestEncryptDecrypt:
    """Test encryption/decryption round-trip."""
    
    def test_small_file_roundtrip(self):
        """Small file encrypts and decrypts correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.txt")
            encrypted_path = os.path.join(tmpdir, "encrypted.bin")
            
            # Create test file
            test_data = b"Hello, World! This is a test file."
            with open(input_path, "wb") as f:
                f.write(test_data)
            
            # Encrypt
            key = generate_key()
            nonce = encrypt_file_chunked(input_path, encrypted_path, key)
            
            # Decrypt
            decrypted = b"".join(decrypt_file_chunked(encrypted_path, key, nonce))
            
            assert decrypted == test_data
    
    def test_large_file_roundtrip(self):
        """Large file (multiple chunks) works correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.bin")
            encrypted_path = os.path.join(tmpdir, "encrypted.bin")
            
            # Create 200KB file (>64KB, multiple chunks)
            test_data = os.urandom(200 * 1024)
            with open(input_path, "wb") as f:
                f.write(test_data)
            
            # Encrypt
            key = generate_key()
            nonce = encrypt_file_chunked(input_path, encrypted_path, key)
            
            # Decrypt
            decrypted = b"".join(decrypt_file_chunked(encrypted_path, key, nonce))
            
            assert decrypted == test_data
    
    def test_wrong_key_fails(self):
        """Decryption with wrong key raises InvalidTag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.txt")
            encrypted_path = os.path.join(tmpdir, "encrypted.bin")
            
            with open(input_path, "wb") as f:
                f.write(b"Secret data")
            
            key1 = generate_key()
            key2 = generate_key()
            
            nonce = encrypt_file_chunked(input_path, encrypted_path, key1)
            
            # Wrong key should fail
            with pytest.raises(InvalidTag):
                list(decrypt_file_chunked(encrypted_path, key2, nonce))
    
    def test_wrong_nonce_fails(self):
        """Decryption with wrong nonce raises InvalidTag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.txt")
            encrypted_path = os.path.join(tmpdir, "encrypted.bin")
            
            with open(input_path, "wb") as f:
                f.write(b"Secret data")
            
            key = generate_key()
            nonce = encrypt_file_chunked(input_path, encrypted_path, key)
            wrong_nonce = os.urandom(12)
            
            with pytest.raises(InvalidTag):
                list(decrypt_file_chunked(encrypted_path, key, wrong_nonce))


class TestPasswordProtectedFile:
    """Test password-derived key encryption."""
    
    def test_password_roundtrip(self):
        """File encrypted with password can be decrypted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.txt")
            encrypted_path = os.path.join(tmpdir, "encrypted.bin")
            
            test_data = b"Confidential information"
            password = "MyS3cr3t!"
            
            with open(input_path, "wb") as f:
                f.write(test_data)
            
            # Encrypt with password
            salt = generate_salt()
            key = derive_key_from_password(password, salt)
            nonce = encrypt_file_chunked(input_path, encrypted_path, key)
            
            # Decrypt with same password + salt
            key2 = derive_key_from_password(password, salt)
            decrypted = b"".join(decrypt_file_chunked(encrypted_path, key2, nonce))
            
            assert decrypted == test_data
    
    def test_wrong_password_fails(self):
        """Wrong password fails to decrypt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.txt")
            encrypted_path = os.path.join(tmpdir, "encrypted.bin")
            
            with open(input_path, "wb") as f:
                f.write(b"Secret")
            
            salt = generate_salt()
            key = derive_key_from_password("correct_password", salt)
            nonce = encrypt_file_chunked(input_path, encrypted_path, key)
            
            # Wrong password
            wrong_key = derive_key_from_password("wrong_password", salt)
            
            with pytest.raises(InvalidTag):
                list(decrypt_file_chunked(encrypted_path, wrong_key, nonce))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
