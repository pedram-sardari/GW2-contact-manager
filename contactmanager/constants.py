class Paths:
    # User
    CONTACTS_DIRECTORY_PATH = './db/contacts'
    USERS_FILE_PATH = './db/users.pickle'
    LAST_LOGIN_PICKLE_FILE_PATH = './db/last_login_data.pickle'


class Constants:
    LOGIN_DURATION_SEC = 1000000 * 60


class Messages:
    # User
    USER_ALREADY_EXISTS_MSG = "\nUsername '{}' already exists."
    INVALID_USERNAME_OR_PASSWORD_MSG = ("\nInvalid username or password."
                                        " If you haven't registered, please register first.")
    INVALID_USER_ID_MSG = "\nUser with id {} not found"
    LOGIN_TIMEOUT_MSG = "\nThere's no logged-in user (or Login Timeout Expired), please login again later."
    LOGIN_MSG = "\n\033[94mWelcome, dear '\033[96m{}\033[94m'. Please use -h for help.\033[0m"
    LOGOUT_MSG = "\n\033[94mThank you for using this application '\033[93m{}\033[94m'. We hope see you soon.\033[0m"
    REGISTER_MSG = "\n\033[94mThank you for registering '\033[96m{}\033[94m'!\033[0m"
    DELETE_USER_MSG = "\n\033[94mUser with id '\033[96m{}\033[94m' deleted!\033[0m"
    SUCCESSFUL_USER_INFO_UPDATE_MSG = "\n\033[92mUser information updated successfully.\033[0m"
    PASS_AND_CONFIRM_PASS_REQUIRED_MSG = "\nBoth password and confirm_password is required"
    Error_FORMAT_MSG = "\n\033[31m{}\033[0m"
    NO_SEARCH_RESULT_MSG = "\nThere are no search result with the given info."
    REGISTER_DURING_LOGIN_SESSION_MSG = ("\nUse '--another-user' flag to "
                                         "register a new user (Only for Admin users).")

    # PickleHandler
    INVALID_MODE_MSG = '\nInvalid mode, must be one of these {}'
    CANNOT_READ_MSG = '\nCannot read write-modded pickle file'
    CANNOT_WRITE_MSG = '\nCannot write to read-modded pickle file'
    FILE_NOT_FOUND_MSG = "\nError 700"  # "File '{}' does not exist."

    # Contact
    CONTACT_ALREADY_EXIST_MSG = '\nThe same contact already exists'
    INVALID_PHONE_NUMBER_MSG = "\nPhone number '{}' is not valid"

    # auth_tools
    NOT_AUTHORIZED_MSG = "\nYou are not authorized to do this operation."
