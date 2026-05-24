import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

class CryptoService:
    def __init__(self, kek_base64: str = None):
        """
        Initialize the CryptoService with a Key Encryption Key (KEK).
        If not provided, it attempts to load from AGENCY_OS_KEK env var.
        The KEK should be a base64 encoded 32-byte (256-bit) key.
        """
        kek_env = os.environ.get('AGENCY_OS_KEK')
        kek_str = kek_base64 or kek_env
        
        if not kek_str:
            raise ValueError("KEK is not provided and AGENCY_OS_KEK environment variable is missing.")
            
        try:
            self.kek = base64.b64decode(kek_str)
            if len(self.kek) != 32:
                raise ValueError("KEK must be exactly 32 bytes (256 bits) long.")
        except Exception as e:
            raise ValueError(f"Invalid KEK format: {e}")

    @staticmethod
    def generate_key() -> bytes:
        """Generates a random 256-bit (32-byte) key suitable for AES-256."""
        return AESGCM.generate_key(bit_length=256)

    @staticmethod
    def generate_key_base64() -> str:
        """Generates a random 256-bit key and returns it as a base64 string."""
        return base64.b64encode(CryptoService.generate_key()).decode('utf-8')

    def encrypt_dek(self, dek: bytes) -> str:
        """
        Encrypts a Data Encryption Key (DEK) using the KEK.
        Returns a base64 encoded string containing the nonce and ciphertext.
        """
        aesgcm = AESGCM(self.kek)
        nonce = secrets.token_bytes(12) # GCM standard nonce size is 96 bits
        ciphertext = aesgcm.encrypt(nonce, dek, None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    def decrypt_dek(self, encrypted_dek_base64: str) -> bytes:
        """
        Decrypts an encrypted DEK using the KEK.
        """
        try:
            encrypted_data = base64.b64decode(encrypted_dek_base64)
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            aesgcm = AESGCM(self.kek)
            return aesgcm.decrypt(nonce, ciphertext, None)
        except Exception as e:
            raise ValueError(f"Failed to decrypt DEK: {e}")

    @staticmethod
    def encrypt_data(dek: bytes, data: str) -> str:
        """
        Encrypts arbitrary string data (like LLM keys) using a DEK.
        Returns a base64 encoded string containing the nonce and ciphertext.
        """
        aesgcm = AESGCM(dek)
        nonce = secrets.token_bytes(12)
        data_bytes = data.encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, data_bytes, None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    @staticmethod
    def decrypt_data(dek: bytes, encrypted_data_base64: str) -> str:
        """
        Decrypts arbitrary string data (like LLM keys) using a DEK.
        """
        try:
            encrypted_data = base64.b64decode(encrypted_data_base64)
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            aesgcm = AESGCM(dek)
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {e}")

    def encrypt_tenant_data(self, encrypted_dek_base64: str, data: str) -> str:
        """
        Convenience method to decrypt the DEK and then encrypt the data.
        """
        dek = self.decrypt_dek(encrypted_dek_base64)
        return self.encrypt_data(dek, data)

    def decrypt_tenant_data(self, encrypted_dek_base64: str, encrypted_data_base64: str) -> str:
        """
        Convenience method to decrypt the DEK and then decrypt the data.
        """
        dek = self.decrypt_dek(encrypted_dek_base64)
        return self.decrypt_data(dek, encrypted_data_base64)
