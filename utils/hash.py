import hashlib


def secure_password(password):
    
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()
