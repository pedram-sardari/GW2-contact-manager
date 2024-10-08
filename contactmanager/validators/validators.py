import re
import datetime
import hashlib

from . import constants as cs


def validate_email(email):
    if isinstance(email, str) and re.match(cs.Patterns.EMAIL_PATTERN, email):
        return email
    raise ValueError(cs.Messages.INVALID_EMAIL_MSG)


def validate_date(date_string: str):
    """
    date_string = "dd-mm-yyyy"
    """
    if isinstance(date_string, str) and re.match(cs.Patterns.DATE_PATTERN, date_string):
        day, month, year = date_string.split('-')
        try:
            datetime.datetime(day=int(day), month=int(month), year=int(year))
        except ValueError:
            pass
        else:
            return date_string

    raise ValueError(cs.Messages.INVALID_DATE_MSG)


def validate_price(price: float | int):
    """

    :param price:
    :raise:
    """
    if isinstance(price, (float, int)) and price > 0:
        return price
    raise ValueError(cs.Messages.INVALID_PRICE_MSG)


def validate_name(name: str):
    if isinstance(name, str) and re.match(cs.Patterns.NAME_PATTERN, name):
        return name
    raise ValueError(cs.Messages.INVALID_NAME_MSG)


def validate_label(label: str):  # TODO: Implementation
    return label


def validate_categories(categories):
    if isinstance(categories, set):
        for category in categories:
            if not isinstance(category, str):
                raise ValueError("Categories must be strings.")  # TODO
    else:
        raise ValueError("Categories must be provided as set of strings")  # TODO
    return categories


def validate_index(lst: list, index: int):
    if isinstance(lst, list) and isinstance(index, int) and len(lst) > index > 0:
        return True
    return False


def validate_uuid(uuid: str):
    if isinstance(uuid, str) and re.match(cs.Patterns.UUID_PATTERN, uuid):
        return uuid
    raise ValueError(cs.Messages.INVALID_UUID.format(uuid))


class User:
    @staticmethod
    def validate_password(password: str, confirm_password: str):  # TODO: Implementation
        cond1 = isinstance(password, str)
        cond2 = True if re.match(cs.Patterns.PASSWORD_8_PATTERN, password) else False
        if cond1 and cond2:
            if password == confirm_password:
                sha256 = hashlib.sha256()
                sha256.update(password.encode())
                return sha256.hexdigest()
            raise ValueError(cs.Messages.PASSWORD_NOT_MATCHED_MSG)
        raise ValueError(cs.Messages.INVALID_PASSWORD_MSG.format(cs.Constants.PASSWORD_MIN_LENGTH))

    @staticmethod
    def validate_username(username: str):  # TODO: Implementation
        return username


class Address:
    @staticmethod
    def validate_city(city: str):
        return city

    @staticmethod
    def validate_address(address: str):  # TODO: Implementation
        return address


class Phones:
    @staticmethod
    def validate_cellphone_number(phone_number: str):
        if isinstance(phone_number, str) and re.match(cs.Patterns.CELLPHONE_NUMBER_PATTERN, phone_number):
            return phone_number
        raise ValueError(cs.Messages.INVALID_CELLPHONE_NUMBER_MSG)

    @staticmethod
    def validate_home_number(phone_number: str):  # TODO: Implementation
        return phone_number


if __name__ == '__main__':
    try:
        print("---------------------------------")
        # print(validate_email("yew(ksad@gmail.com"))
        # print(validate_email("yew2ksad@g*mail.com"))
        print(validate_email("yew2ksad@gmail.com"))
        print("---------------------------------")
        # print(validate_date("32-2-2002"))
        # print(validate_date("3-23-2002"))
        # print(validate_date("3-2-20002"))
        # print(validate_date("32-2--2002"))
        # print(validate_date("32-a-2002"))
        # print(validate_date("32*2*2002"))
        print(validate_date("3-2-2002"))
        print("---------------------------------")
        # print(validate_price(-72))
        print(validate_price(72))
        print("---------------------------------")
        # print(NumberValidator.validate_cellphone_number("+12345678911"))
        # print(NumberValidator.validate_cellphone_number("19193636442"))
        # print(NumberValidator.validate_cellphone_number("091903636442"))
        print(Phones.validate_cellphone_number("+98913636442"))
        print(Phones.validate_cellphone_number("09193636442"))
        print("---------------------------------")
        # print(validate_name("hasan2"))
        print(validate_name("Hasan"))
        print(validate_name("hasan"))
    except ValueError as error:
        print(error)
