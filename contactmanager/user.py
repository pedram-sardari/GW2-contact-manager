import hashlib
import os
import pathlib
import time
import uuid

import constants as cs
import validators
from pickle_handler import PickleHandler


class User:
    users_list = []
    users_pickle_file_path = pathlib.Path(cs.Paths.USERS_FILE_PATH)
    last_login_pickle_file_path = pathlib.Path(cs.Paths.LAST_LOGIN_PICKLE_FILE_PATH)
    last_login_data = {"user": None, "timestamp": 0.0}

    def __init__(self, name, username, password, confirm_password):
        self._user_id = str(uuid.uuid4())
        self.user_type = self.__class__.__name__
        self._name = validators.validate_name(name)
        self._username = User.validate_username(username)
        self.__password = validators.User.validate_password(password, confirm_password)
        contacts_path = os.path.join(cs.Paths.CONTACTS_DIRECTORY_PATH, f"{str(self.user_id)}.pickle")
        self._contacts_pickle_file_path = pathlib.Path(contacts_path)
        self.__initialize_contacts_pickle_file()

    def __initialize_contacts_pickle_file(self):
        self.contacts_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
        with PickleHandler(str(self.contacts_pickle_file_path), 'w') as f:
            f.write(data=list())

    @staticmethod
    def convert_password_to_hash(password: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(password.encode())
        return sha256.hexdigest()

    @property
    def user_id(self):
        return self._user_id

    @property
    def contacts_pickle_file_path(self):
        return self._contacts_pickle_file_path

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = User.validate_username(username)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = validators.validate_name(name)

    @classmethod
    def validate_username(cls, username):
        cls._load_users_list()
        validators.User.validate_username(username)
        if username in [user.username for user in User.users_list]:
            raise ValueError(cs.Messages.USER_ALREADY_EXISTS_MSG.format(username))
        return username

    def __eq__(self, other):
        cond1 = self.user_id == other.user_id
        cond2 = self.user_type == other.user_type
        cond3 = self.name == other.name
        cond4 = self.username == other.username
        cond5 = self.__password == other.__password
        cond6 = str(self.contacts_pickle_file_path) == str(other.contacts_pickle_file_path)
        if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
            return True
        return False

    @classmethod
    def _load_users_list(cls):
        with PickleHandler(file_path=str(cls.users_pickle_file_path), mode='r') as f:
            cls.users_list = f.read()

    @classmethod
    def _save_users_list(cls):
        with PickleHandler(file_path=str(cls.users_pickle_file_path), mode='w') as f:
            f.write(cls.users_list)

    @classmethod
    def _save_last_login_data(cls):
        cls.last_login_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
        with PickleHandler(file_path=str(cls.last_login_pickle_file_path), mode='w') as f:
            f.write(cls.last_login_data)

    @classmethod
    def _load_last_login_data(cls):
        if not cls.last_login_pickle_file_path.exists():
            cls._save_last_login_data()
        else:
            with PickleHandler(file_path=str(cls.last_login_pickle_file_path), mode='r') as f:
                cls.last_login_data = f.read()

    @classmethod
    def register(cls, new_user):
        cls.users_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not cls.users_pickle_file_path.exists():
            cls._save_users_list()
        else:
            cls._load_users_list()
        cls.users_list.append(new_user)
        cls._save_users_list()

    @classmethod
    def login(cls, username, password):
        cls._load_users_list()
        for user in cls.users_list:
            if user.username == username and user.__password == cls.convert_password_to_hash(password):
                cls.last_login_data["user"] = user
                cls.last_login_data["timestamp"] = time.time()
                cls._save_last_login_data()
                return user
        cls._clear_last_login_data()
        raise ValueError(cs.Messages.INVALID_USERNAME_OR_PASSWORD_MSG)

    @classmethod
    def logout(cls):
        cls._clear_last_login_data()

    @classmethod
    def _clear_last_login_data(cls):
        cls.last_login_data["user"] = None
        cls.last_login_data["timestamp"] = 0.0
        cls._save_last_login_data()

    @classmethod
    def get_last_logged_in_user(cls):
        now = time.time()
        cls._load_last_login_data()
        if (cls.last_login_data["timestamp"] + cs.Constants.LOGIN_DURATION_SEC) < now:
            cls._clear_last_login_data()
            raise TimeoutError(cs.Messages.LOGIN_TIMEOUT_MSG)
        return cls.last_login_data["user"]

    @classmethod
    def find_last_logged_in_user_in_users_list(cls):
        cls._load_users_list()
        last_logged_in_user = cls.get_last_logged_in_user()
        for user in cls.users_list:
            if user == last_logged_in_user:
                cls.last_login_data['user'] = user
                return user

    @classmethod
    def edit_my_profile_info(cls, name=None, username=None, password=None, confirm_password=None):
        user = cls.find_last_logged_in_user_in_users_list()
        try:
            if name:
                user.name = name  # validation by setter
            if username:
                user.username = username  # validation by setter
                cls._clear_last_login_data()
            if password and confirm_password:
                user.__password = validators.User.validate_password(password, confirm_password)
                cls._clear_last_login_data()
        except Exception:
            raise
        else:
            cls._save_last_login_data()
            cls._save_users_list()

    def view_my_profile_info(self):
        print(self)

    def __str__(self):
        return (f"\nUser ID: {self.user_id}\n"
                f"Name: {self.name}\n"
                f"User Type: {self.user_type}\n"
                f"Username: {self.username}\n"
                f"Password: {self._User__password}\n"
                f"Contacts_pickle_file_path: {self.contacts_pickle_file_path}\n"
                f"{id(self)}"
                f"--------------------------------------------------------------------------------")

    def __repr__(self):
        return str(self)
