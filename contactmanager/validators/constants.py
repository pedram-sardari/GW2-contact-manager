class Constants:
    PASSWORD_MIN_LENGTH = 8


class Patterns:
    EMAIL_PATTERN = r"[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    DATE_PATTERN = r"^\d{1,2}-\d{1,2}-\d{1,4}$"
    NAME_PATTERN = r"^[A-Za-z][a-z1-9]*$"
    CELLPHONE_NUMBER_PATTERN = r"^(\+98|09)\d-?\d{3}-?\d{5}$"
    UUID_PATTERN = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
    PASSWORD_8_PATTERN = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class Messages:
    INVALID_EMAIL_MSG = "Invalid email!"
    INVALID_DATE_MSG = "Invalid date!"
    INVALID_NAME_MSG = "Invalid name!"
    INVALID_CELLPHONE_NUMBER_MSG = "Invalid cellphone number!"
    INVALID_PRICE_MSG = "Invalid price!"
    INVALID_UUID = "Invalid UUID '{}'"
    # User
    INVALID_PASSWORD_MSG = ("Invalid password. Password should be alphanumeric and at least {} "
                            "characters long and contain special characters!")
    PASSWORD_NOT_MATCHED_MSG = "Password and Confirm Password do not match."
