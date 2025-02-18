from config import get_cipher

class EncryptionManager:
    def __init__(self, password):
        self.cipher = get_cipher(password)
    
    def encrypt_text(self, text):
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt_text(self, text):
        return self.cipher.decrypt(text.encode()).decode()