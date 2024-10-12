from cryptography.fernet import Fernet


def encrypt(data, key):
    some_changes = key[:5] + 'Yung' + key[9:]
    fernet = Fernet(some_changes.encode())
    string_encrypt_data = fernet.encrypt(data.encode()).decode()

    return string_encrypt_data


def decrypt(data, key):
    some_changes = key[:5] + 'Yung' + key[9:]
    fernet = Fernet(some_changes.encode())
    decrypt_data = fernet.decrypt(data.encode()).decode()

    return decrypt_data
