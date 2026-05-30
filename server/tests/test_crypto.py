import pytest
import os
import base64
from server.utils.crypto import CryptoService

def test_crypto_service_initialization_with_env_var(monkeypatch):
    test_kek = CryptoService.generate_key_base64()
    monkeypatch.setenv("AGENCY_OS_KEK", test_kek)
    
    service = CryptoService()
    assert service.kek == base64.b64decode(test_kek)

def test_crypto_service_initialization_with_param():
    test_kek = CryptoService.generate_key_base64()
    
    service = CryptoService(kek_base64=test_kek)
    assert service.kek == base64.b64decode(test_kek)

def test_crypto_service_initialization_missing_kek():
    # Ensure env var is not set
    if "AGENCY_OS_KEK" in os.environ:
        del os.environ["AGENCY_OS_KEK"]
        
    with pytest.raises(ValueError, match="KEK is not provided and AGENCY_OS_KEK / ENCRYPTION_KEY environment variable is missing."):
        CryptoService()

def test_crypto_service_initialization_invalid_kek():
    with pytest.raises(ValueError, match="KEK must be exactly 32 bytes"):
        # 16 byte key base64 encoded
        invalid_kek = base64.b64encode(b'1234567890123456').decode('utf-8')
        CryptoService(kek_base64=invalid_kek)

def test_generate_key():
    key = CryptoService.generate_key()
    assert isinstance(key, bytes)
    assert len(key) == 32

def test_generate_key_base64():
    key_b64 = CryptoService.generate_key_base64()
    assert isinstance(key_b64, str)
    key_bytes = base64.b64decode(key_b64)
    assert len(key_bytes) == 32

def test_encrypt_decrypt_dek():
    kek_b64 = CryptoService.generate_key_base64()
    service = CryptoService(kek_base64=kek_b64)
    
    dek = CryptoService.generate_key()
    
    encrypted_dek_b64 = service.encrypt_dek(dek)
    assert encrypted_dek_b64 != base64.b64encode(dek).decode('utf-8')
    
    decrypted_dek = service.decrypt_dek(encrypted_dek_b64)
    assert decrypted_dek == dek

def test_encrypt_decrypt_data():
    dek = CryptoService.generate_key()
    
    test_data = "sk-test-llm-key-12345"
    
    encrypted_data_b64 = CryptoService.encrypt_data(dek, test_data)
    assert encrypted_data_b64 != test_data
    
    decrypted_data = CryptoService.decrypt_data(dek, encrypted_data_b64)
    assert decrypted_data == test_data

def test_encrypt_decrypt_tenant_data():
    kek_b64 = CryptoService.generate_key_base64()
    service = CryptoService(kek_base64=kek_b64)
    
    dek = CryptoService.generate_key()
    encrypted_dek_b64 = service.encrypt_dek(dek)
    
    test_data = "sk-tenant-specific-api-key"
    
    encrypted_tenant_data = service.encrypt_tenant_data(encrypted_dek_b64, test_data)
    
    decrypted_tenant_data = service.decrypt_tenant_data(encrypted_dek_b64, encrypted_tenant_data)
    
    assert decrypted_tenant_data == test_data

def test_decrypt_invalid_data():
    dek = CryptoService.generate_key()
    with pytest.raises(ValueError, match="Failed to decrypt data"):
        CryptoService.decrypt_data(dek, "invalid_base64_data")
