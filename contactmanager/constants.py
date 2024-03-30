class Paths:
    # User
    CONTACTS_DIRECTORY_PATH = './db/contacts'
    USERS_FILE_PATH = './db/users.pickle'
    LAST_LOGIN_PICKLE_FILE_PATH = './db/last_login_data.pickle'


class Constants:
    LOGIN_DURATION_SEC = 1000000 * 60


class Messages:
    # User
    USER_ALREADY_EXISTS_MSG = "Username '{}' already exists."
    INVALID_USERNAME_OR_PASSWORD_MSG = "Invalid username or password. If you haven't registered, please register first."
    INVALID_USER_ID_MSG = "User with id {} not found"
    LOGIN_TIMEOUT_MSG = "There's no logged-in user (or Login Timeout Expired), please login again later."

    # PickleHandler
    INVALID_MODE_MSG = 'Invalid mode, must be one of these {}'
    CANNOT_READ_MSG = 'Cannot read write-modded pickle file'
    CANNOT_WRITE_MSG = 'Cannot write to read-modded pickle file'
    FILE_NOT_FOUND_MSG = "Error 700"  # "File '{}' does not exist."

    # Contact
    CONTACT_EXIST_ALREADY = 'The same contact already exists'
    INVALID_PHONE_NUMBER_MSG = "Phone number '{}' is not valid"

    # auth_tools
    NOT_AUTHORIZED_MSG = "You are not authorized to do this operation."
