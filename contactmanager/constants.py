class Paths:
    # User
    CONTACTS_DIRECTORY_PATH = './db/contacts'
    USERS_FILE_PATH = './db/users.pickle'
    LAST_LOGIN_PICKLE_FILE_PATH = './db/last_login_data.pickle'


class Constants:
    LOGIN_DURATION_SEC = 5 * 60


class Messages:
    # User
    USER_ALREADY_EXISTS_MSG = "Username '{}' already exists."
    INVALID_USERNAME_OR_PASSWORD_MSG = "Invalid username or password. If you haven't registered, please register first."

    # PickleHandler
    INVALID_MODE_MSG = 'Invalid mode, must be one of these {}'
    CANNOT_READ_MSG = 'Cannot read write-modded pickle file'
    CANNOT_WRITE_MSG = 'Cannot write to read-modded pickle file'
