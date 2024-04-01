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
    LOGIN_MSG = "\033[94mWelcome, dear '\033[96m{}\033[94m'. Please use -h for help.\033[0m"
    LOGOUT_MSG = "\033[94mThank you for using this application '\033[93m{}\033[94m'. We hope see you soon.\033[0m"
    REGISTER_MSG = "\033[94mThank you for registering '\033[96m{}\033[94m'!\033[0m"
    SUCCESSFUL_USER_INFO_UPDATE_MSG = "\033[92mUser information updated successfully.\033[0m"
    PASS_AND_CONFIRM_PASS_REQUIRED_MSG = "Both password and confirm_password is required"
    Error_FORMAT_MSG = "\033[31m{}\033[0m"
    NO_SEARCH_RESULT_MSG = "There are no search result with the given info."

    # PickleHandler
    INVALID_MODE_MSG = 'Invalid mode, must be one of these {}'
    CANNOT_READ_MSG = 'Cannot read write-modded pickle file'
    CANNOT_WRITE_MSG = 'Cannot write to read-modded pickle file'
    FILE_NOT_FOUND_MSG = "Error 700"  # "File '{}' does not exist."

    # Contact
    CONTACT_ALREADY_EXIST_MSG = 'The same contact already exists'
    INVALID_PHONE_NUMBER_MSG = "Phone number '{}' is not valid"

    # auth_tools
    NOT_AUTHORIZED_MSG = "You are not authorized to do this operation."
