class Patterns:
    EMAIL_PATTERN = r"[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    DATE_PATTERN = r"^\d{1,2}-\d{1,2}-\d{1,4}$"
    NAME_PATTERN = r"^[A-Za-z][a-z]*$"
    CELLPHONE_NUMBER_PATTERN = r"^(\+98|09)\d-?\d{3}-?\d{5}$"


class Messages:
    INVALID_EMAIL_MSG = "Invalid email!"
    INVALID_DATE_MSG = "Invalid date!"
    INVALID_NAME_MSG = "Invalid name!"
    INVALID_CELLPHONE_NUMBER_MSG = "Invalid cellphone number!"
    INVALID_PRICE_MSG = "Invalid price!"
