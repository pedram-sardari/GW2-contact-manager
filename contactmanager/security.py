from cryptography.fernet import Fernet
import constants as cs


def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
        print("Key is generated!")


def load_key(key_path=cs.Paths.SECRET_KEY_FILE_PATH):
    with open(key_path, "rb") as key_file:
        return key_file.read()


def encrypt(content):
    fernet = Fernet(load_key())
    return fernet.encrypt(content)


def decrypt(encrypted_content):
    fernet = Fernet(load_key())
    return fernet.decrypt(encrypted_content)


if __name__ == '__main__':
    encrypted_content = encrypt("hello".encode())
    print(encrypted_content)
    decrypted_content = decrypt(encrypted_content)
    print(decrypted_content)
