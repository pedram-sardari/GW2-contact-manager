import datetime
import uuid
import pathlib
import os
import pickle

import validators
import constants as cs
from contactmanager.pickle_handler import PickleHandler


class User:
    users_list = []
    users_pickle_file_path = pathlib.Path(cs.Paths.USERS_FILE_PATH)
    last_login_pickle_file_path = pathlib.Path(cs.Paths.LAST_LOGIN_PICKLE_FILE_PATH)
    _last_login_data = {"user": None, "date": None}

    def __init__(self, name, username, password, confirm_password):
        self._user_id = str(uuid.uuid4())
        self._name = validators.validate_name(name)
        self._username = User.validate_username(username)
        self.__password = validators.validate_password(password, confirm_password)
        self._contacts_file_path = pathlib.Path(
            os.path.join(cs.Paths.CONTACTS_DIRECTORY_PATH, f"{str(uuid.uuid4())}.pickle"))
        self.__initialize_contacts_pickle_file()

    def __initialize_contacts_pickle_file(self):
        # self.contacts_file_path.mkdir(parents=True, exist_ok=True) # TODO: Why throwing a Error?
        with self._contacts_file_path.open('wb') as f:
            pickle.dump(list(), f)

    @classmethod
    def __initialize_users_pickle_file(cls):
        with PickleHandler(str(cls.users_pickle_file_path), mode='w') as f:
            f.write(cls.users_list)

    @classmethod
    def __initialize_last_login_pickle_file(cls):  # TODO: Where is it gonna be used?
        with PickleHandler(str(cls.last_login_pickle_file_path), mode='w') as f:
            f.write(cls._last_login_data)

    @property
    def user_id(self):
        return self._user_id

    @property
    def contacts_file_path(self):
        return self._contacts_file_path

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

    @staticmethod
    def validate_username(username):
        validators.validate_username(username)
        if username in [user.username for user in User.users_list]:
            raise ValueError(cs.Messages.USER_ALREADY_EXISTS_MSG.format(username))
        return username

    @classmethod
    def __load_users_list(cls):
        with PickleHandler(file_path=str(cls.users_pickle_file_path), mode='r') as f:
            cls.users_list = f.read()

    @classmethod
    def __save_users_list(cls):
        with PickleHandler(file_path=str(cls.users_pickle_file_path), mode='w') as f:
            f.write(cls.users_list)

    @classmethod
    def __save_last_login_data(cls):
        with PickleHandler(file_path=str(cls.last_login_pickle_file_path), mode='w') as f:
            f.write(cls._last_login_data)

    @classmethod
    def __load_last_login_data(cls):
        with PickleHandler(file_path=str(cls.last_login_pickle_file_path), mode='r') as f:
            cls._last_login_data = f.read()

    @classmethod
    def register(cls, name, username, password, confirm_password):
        if not cls.users_pickle_file_path.exists():
            cls.__initialize_users_pickle_file()
        else:
            cls.__load_users_list()
        # print(cls.users_list[1].__dict__)
        new_user = cls(name=name, username=username, password=password, confirm_password=confirm_password)
        cls.users_list.append(new_user)
        cls.__save_users_list()

    @classmethod
    def login(cls, username, password):
        cls.__load_users_list()
        for user in cls.users_list:
            if user.username == username and user.__password == password:
                cls._last_login_data["user"] = user
                cls._last_login_data["date"] = datetime.datetime.today()
                cls.__save_last_login_data()
                return user
            else:
                raise ValueError(cs.Messages.INVALID_USERNAME_OR_PASSWORD_MSG)

    @classmethod
    def logout(cls):
        cls._last_login_data["user"] = None
        cls._last_login_data["date"] = None
        cls.__save_last_login_data()

    @classmethod
    def get_last_login_data(cls):
        with PickleHandler(str(cls.last_login_pickle_file_path), 'r') as f:
            return f.read()

    @classmethod
    def edit_user(cls, name=None, username=None, password=None, confirm_password=None):
        cls.__load_last_login_data()
        if user := User._last_login_data["user"] is not None:
            User.__load_users_list()    # username validator needs users_list
            if name:
                user.name = name    # validation by setter
            if username:
                user.username = username    # validation by setter
            if password and confirm_password:
                user.__password = validators.validate_password(password, confirm_password)

            # find the logged-in user in users_list



