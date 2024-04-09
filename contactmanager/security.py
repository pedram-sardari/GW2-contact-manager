from cryptography.fernet import Fernet
import constants as cs
import string


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


def check_common_passwords_list(password):
    with open(cs.Paths.COMMON_PASSWORD_FILE_PATH, 'r') as f:
        common_passwords = f.read()
        if password in common_passwords:
            return True
        return False


def check_character_types(password) -> int:
    lower = upper = digit = special_char = 0
    for letter in password:
        if upper and lower and digit and special_char:
            break
        elif not upper and letter in string.ascii_uppercase:
            upper = 1
        elif not lower and letter in string.ascii_lowercase:
            lower = 1
        elif not digit and letter in string.digits:
            digit = 1
        elif not special_char and letter in string.punctuation:
            special_char = 1

    return sum((lower, upper, digit, special_char))


def check_length(password):
    score = 0
    password_length = len(password)
    if password_length > 8:
        score += 1
    if password_length > 12:
        score += 1
    if password_length > 16:
        score += 1
    if password_length > 20:
        score += 1
    return score


def score_password(password):
    score = 0
    is_common_password = check_common_passwords_list(password)
    score += check_character_types(password)
    score += check_length(password)
    if is_common_password:
        return cs.Messages.COMMON_PASSWORD_MSG
    elif score < 4:
        return cs.Messages.WEAK_PASSWORD_MSG.format(score)
    elif score == 4:
        return cs.Messages.OK_PASSWORD_MSG.format(score)
    elif 4 < score < 6:
        return cs.Messages.PRETTY_GOOD_PASSWORD_MSG.format(score)
    elif score >= 6:
        return cs.Messages.STRONG_PASSWORD_MSG.format(score)


if __name__ == '__main__':
    print(__name__)
    # encrypted_content = encrypt("hello".encode())
    # print(encrypted_content)
    # decrypted_content = decrypt(encrypted_content)
    # print(decrypted_content)
    print(score_password('1234'))
