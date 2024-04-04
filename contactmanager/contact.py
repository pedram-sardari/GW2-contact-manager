import re
import uuid
import logging

import constants as cs
import validators
from contactmanager.user import User, AdminUser
from categories import Category

# logging
logging.basicConfig(filename='contact_manager.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Contact:
    contacts_list = []

    def __init__(self, first_name, last_name, email, addresses: list, phones: list, categories: set):
        self._contact_id = uuid.uuid4()
        self._first_name = validators.validate_name(first_name)
        self._last_name = validators.validate_name(last_name)
        self._email = validators.validate_email(email)
        self._addresses = self.validate_addresses(addresses)  # addresses = [["addr1", "street1, alley1"], ...]]
        self._phones = self.validate_phones(phones)  # phones = [["Home", "8821318"], ...]
        self.categories = Category(categories)
        logging.info(f"Initialized contact: {self._first_name} {self._last_name}")

    @property
    def contact_id(self):
        return self._contact_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self._first_name = validators.validate_name(new_first_name)
        logging.info(f"Updated first name: {self._first_name}")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = validators.validate_name(new_last_name)
        logging.info(f"Updated last name: {self._last_name}")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = validators.validate_email(new_email)
        logging.info(f"Updated email: {self._email}")

    @property
    def phones(self):
        return self._phones

    @phones.setter
    def phones(self, new_phones):
        for new_label__phone in Contact.validate_phones(new_phones):
            new_label, new_phone = new_label__phone
            for i, current_label__phone in enumerate(self.phones):
                current_label, current_phone = current_label__phone
                if not new_phone:
                    if new_label == current_label and new_phone == "":
                        self.phones.pop(i)
                        break
                elif new_label == current_label and new_phone != current_phone:
                    self.phones[i] = new_label__phone
                    break
                elif new_label == current_label and new_phone == current_phone:
                    break
            else:
                if new_phone:
                    self.phones.append(new_label__phone)
        logging.info("Updated phones")

    @property
    def addresses(self):
        return self._addresses

    @addresses.setter
    def addresses(self, new_addresses):
        for new_label__address in Contact.validate_addresses(new_addresses):
            new_label, new_address = new_label__address
            for i, current_label__address in enumerate(self.addresses):
                current_label, current_address = current_label__address
                if not new_address:
                    if new_label == current_label and new_address == "":
                        self.addresses.pop(i)
                        break
                elif new_label == current_label and new_address != current_address:
                    self.addresses[i] = new_label__address
                    break
                elif new_label == current_label and new_address == current_address:
                    break
            else:
                if new_address:
                    self.addresses.append(new_label__address)
        logging.info("Updated addresses")

    @staticmethod
    def validate_addresses(addresses_list: list):
        for label, address in addresses_list:
            validators.Address.validate_address(address)
            validators.validate_name(label)
        return addresses_list

    @staticmethod
    def validate_phones(phones_list: list):
        for label, phone in phones_list:
            try:
                validators.Phones.validate_cellphone_number(phone)
            except ValueError:
                pass
            try:
                validators.Phones.validate_home_number(phone)
            except ValueError:
                raise ValueError(cs.Messages.INVALID_PHONE_NUMBER_MSG.format(phone))
            validators.validate_name(label)
        return phones_list

    @classmethod
    def set_contacts_list(cls, *, user_id=None):
        if user_id:
            search_result = AdminUser.search_user(user_id=user_id)
            user = search_result[0]
        else:
            user = User.get_last_logged_in_user()
        cls.contacts_list = user.contacts_list
        logging.info(f"Set contacts list for user: {user.username}")

    @classmethod
    def add_contact(cls, new_contact):
        if isinstance(new_contact, cls):
            cls.check_contact_existence(new_contact)
            cls.contacts_list.append(new_contact)
            logging.info(f"Added new contact: {new_contact.first_name} {new_contact.last_name}")
            return cs.Messages.CONTACT_ADDED_MSG.format(new_contact.first_name)
        else:
            logging.error("Invalid contact instance provided.")
            raise ValueError("Invalid contact instance provided.")

    @staticmethod
    def check_contact_existence(new_contact):
        for contact in Contact.contacts_list:
            if contact == new_contact:
                logging.error("Contact already exists.")
                raise ValueError(cs.Messages.CONTACT_ALREADY_EXIST_MSG)

    def __eq__(self, other):
        cond1 = self.first_name == other.first_name
        cond2 = self.last_name == other.last_name
        cond3 = self.email == other.email
        cond4 = all([(address in self.addresses) for address in other.addresses])
        cond5 = all([(phone in self.phones) for phone in other.phones])
        if cond1 and cond2 and cond3 and cond4 and cond5:
            logging.info("Contacts are equal.")
            return True
        else:
            logging.info("Contacts are not equal.")
            return False

    @staticmethod
    def search_contact(contact_id="", first_name="", last_name="", email="", phone_number="", category="") -> list:
        matched_contacts = []
        pattern = r".*{}.*"
        for contact in Contact.contacts_list:
            cond1 = cond2 = cond3 = cond4 = cond5 = con6 = True
            if contact_id:
                contact_id = validators.validate_uuid(contact_id)
                cond1 = True if re.search(pattern.format(contact_id), str(contact.contact_id)) else False
            else:
                if first_name:
                    cond2 = True if re.search(pattern.format(first_name), contact.first_name) else False
                if last_name:
                    cond3 = True if re.search(pattern.format(last_name), contact.last_name) else False
                if email:
                    cond4 = True if re.search(pattern.format(email), contact.email) else False
                if phone_number:
                    for label, contact_phone_number in contact.phones:
                        if re.search(pattern.format(phone_number), contact_phone_number):
                            break
                    else:
                        cond5 = False
                if category:
                    con6 = contact.categories.search_category(category)
            if cond1 and cond2 and cond3 and cond4 and cond5 and con6:
                matched_contacts.append(contact)

        if matched_contacts:
            return matched_contacts
        else:
            logging.error("No search results found.")
            raise ValueError(cs.Messages.NO_SEARCH_RESULT_MSG)

    def edit_contact(self, first_name=None, last_name=None, email=None, phones=None, addresses=None, categories=None):
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
        if categories:
            self.categories.edit_category(categories)
        logging.info("Contact edited successfully.")

    @staticmethod
    def view_search_result(search_result_list):
        if isinstance(search_result_list, list):
            for index, contact in enumerate(search_result_list, 1):
                print(f"\033[93m{'-' * 40}( {index} ){'-' * 40}\033[0m")
                print(contact)

    @staticmethod
    def view_all_contacts():
        Contact.view_search_result(Contact.search_contact())

    @classmethod
    def delete_contact(cls, contact_id="", first_name="", last_name="", email="", phone_number="", categories=""):
        matched_contacts = cls.search_contact(contact_id, first_name, last_name, email, phone_number, categories)
        for matched_contact in matched_contacts:
            cls.contacts_list.remove(matched_contact)
            logging.info(f"Deleted contact: {matched_contact.first_name} {matched_contact.last_name}")
        return cs.Messages.CONTACT_REMOVED_MSG.format(len(matched_contacts))

    @classmethod
    def delete_all_contacts(cls):
        count = len(cls.contacts_list)
        cls.contacts_list.clear()
        logging.info(f"All contacts deleted. Count: {count}")
        return cs.Messages.CONTACT_REMOVED_MSG.format(count)

    def __str__(self):
        string = "\n"
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                for name, item in value:
                    string += f"\033[94m{name}: \033[95m{item}\033[0m\n"
            else:
                string += f"\033[94m{key.strip('_').replace('_', ' ')}: \033[95m{value}\033[0m\n"
        return string

    def __repr__(self):
        return str(self)
