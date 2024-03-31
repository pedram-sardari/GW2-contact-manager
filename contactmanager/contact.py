import pathlib
import re
import uuid

import auth_tools
import constants as cs
import validators
from contactmanager.pickle_handler import PickleHandler
from contactmanager.user import User, AdminUser


class Contact:
    contacts_list = []
    contacts_pickle_file_path = pathlib.Path('null')

    def __init__(self, first_name, last_name, email, addresses: list, phone_numbers: list):
        self._contact_id = uuid.uuid4()
        self._first_name = validators.validate_name(first_name)
        self._last_name = validators.validate_name(last_name)
        self._email = validators.validate_email(email)
        self._addresses = self.validate_addresses(addresses)  # addresses = [["addr1", "street1, alley1"], ...]]
        self._phones = self.validate_phones(phone_numbers)  # phones = [["Home", "8821318"], ...]

    @property
    def contact_id(self):
        return self._contact_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self._first_name = validators.validate_name(new_first_name)

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = validators.validate_name(new_last_name)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = validators.validate_email(new_email)

    @property
    def phones(self):
        return self._phones

    @phones.setter
    def phones(self, new_phones):
        for new_name, new_phone in Contact.validate_phones(new_phones):
            for index, item in enumerate(self.phones):
                name, phone = item
                if name == new_name and phone != new_phone:
                    self.phones[index] = new_phone
                    break
            else:
                self.phones.append([new_name, new_phone])

    @property
    def addresses(self):
        return self._addresses

    @addresses.setter
    def addresses(self, new_addresses):
        for new_name, new_address in Contact.validate_addresses(new_addresses):
            for index, item in enumerate(self.addresses):
                name, address = item
                if name == new_name and address != new_address:
                    self.phones[index] = new_address
                break
            else:
                self.phones.append([new_name, new_address])

    @staticmethod
    def validate_addresses(addresses_list: list):
        for name, address in addresses_list:
            validators.Address.validate_address(address)
            validators.validate_name(name)
        return addresses_list

    @staticmethod
    def validate_phones(phones_list: list):
        # print(phones_list)
        for name, phone in phones_list:
            try:
                validators.Phones.validate_cellphone_number(phone)
            except ValueError:
                pass
            try:
                validators.Phones.validate_home_number(phone)
            except ValueError:
                raise ValueError(cs.Messages.INVALID_PHONE_NUMBER_MSG.format(phone))
            validators.validate_name(name)
        return phones_list

    # @auth_tools.who_has_access(authorized_user_types_list=[AdminUser])
    @classmethod
    @auth_tools.who_can_provide_params(authorized_user_types_list=[AdminUser], restricted_params_list=["user_id"])
    def set_contacts_pickle_file_path(cls, *, user_id=None):
        if user_id:
            search_result = AdminUser.search_user(user_id=user_id)
            user = search_result[0]
            print(user)
        else:
            user = User.get_last_logged_in_user()
        cls.contacts_pickle_file_path = user.contacts_pickle_file_path

    @classmethod
    def __load_contacts_list(cls):
        if cls.contacts_pickle_file_path.name == "null":
            cls.set_contacts_pickle_file_path()
        if cls.contacts_pickle_file_path.exists():
            print(cls.contacts_pickle_file_path)
            with PickleHandler(str(cls.contacts_pickle_file_path), 'r') as f:
                cls.contacts_list = f.read()

    @classmethod
    def __save_contacts_list(cls):
        if cls.contacts_pickle_file_path.name == "null":
            cls.set_contacts_pickle_file_path()
        with PickleHandler(str(cls.contacts_pickle_file_path), 'w') as f:
            f.write(cls.contacts_list)

    @classmethod
    def add_contact(cls, new_contact):
        if isinstance(new_contact, cls):
            cls.__load_contacts_list()
            cls.check_contact_existence(new_contact)
            cls.contacts_list.append(new_contact)
            cls.__save_contacts_list()

    @staticmethod
    def check_contact_existence(new_contact):
        for contact in Contact.contacts_list:
            if contact == new_contact:
                raise ValueError(cs.Messages.CONTACT_EXIST_ALREADY)

    def __eq__(self, other):
        cond1 = self.first_name == other.first_name
        cond2 = self.last_name == other.last_name
        cond3 = self.email == other.email
        cond4 = all([(address in self.addresses) for address in other.addresses])
        cond5 = all([(phone in self.phones) for phone in other.phones])
        if cond1 and cond2 and cond3 and cond4 and cond5:
            return True
        return False

    @staticmethod
    def search_contact(contact_id=None, first_name=None, last_name=None, email=None, phone_number=None) -> list:
        Contact.__load_contacts_list()
        matched_contacts = []
        pattern = r".*{}.*"
        for contact in Contact.contacts_list:
            cond1 = cond2 = cond3 = cond4 = cond5 = True
            if contact_id:
                cond1 = True if re.search(pattern.format(contact_id), str(contact.contact_id)) else False
            if first_name:
                cond2 = True if re.search(pattern.format(first_name), contact.first_name) else False
            if last_name:
                cond3 = True if re.search(pattern.format(last_name), contact.last_name) else False
            if email:
                cond4 = True if re.search(pattern.format(email), contact.email) else False
            if phone_number:
                for name, contact_phone_number in contact.phones:
                    if re.search(pattern.format(phone_number), contact_phone_number):
                        break
                else:
                    cond5 = False

            if cond1 and cond2 and cond3 and cond4 and cond5:
                matched_contacts.append(contact)

        return matched_contacts

    def edit_contact(self, first_name=None, last_name=None, email=None, phones=None, addresses=None):
        try:
            if first_name:
                self.first_name = first_name
            if last_name:
                self.last_name = last_name
            if email:
                self.email = email
            if phones:
                self.phones = phones
            if addresses:
                self.addresses = addresses
        except Exception:
            raise
        else:
            Contact.__save_contacts_list()

    @classmethod
    def view_all_contacts(cls):
        cls.__load_contacts_list()
        for index, contact in enumerate(cls.contacts_list, 1):
            print(f"\033[93m{'-' * 40}( {index} ){'-' * 40}\033[0m")
            print(contact)

    @classmethod
    def delete_contact(cls, contact_id=None, first_name=None, last_name=None, email=None, phone_number=None):
        matched_contacts = cls.search_contact(contact_id, first_name, last_name, email, phone_number)
        for matched_contact in matched_contacts:
            cls.contacts_list.remove(matched_contact)
        cls.__save_contacts_list()
        return matched_contacts

    @classmethod
    def delete_all_contacts(cls):
        cls.__load_contacts_list()
        cls.contacts_list.clear()
        cls.__save_contacts_list()

    def __str__(self):
        string = ""
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                # print(f"{key}: {value}")
                for name, item in value:
                    string += f"\033[94m{name}: \033[95m{item}\033[0m\n"
            else:
                string += f"\033[94m{key.strip('_').replace('_', ' ')}: \033[95m{value}\033[0m\n"
        return string

    def __repr__(self):
        return str(self)
