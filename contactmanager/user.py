import hashlib
import os
import pathlib
import re
import time
import uuid
import typing

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
        self._initialize_contacts_pickle_file()

    def _initialize_contacts_pickle_file(self):
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

    @staticmethod
    def validate_username(username):
        if User.users_pickle_file_path.exists():
            User._load_users_list()
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
        if not cls.users_list:
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
    def register(cls, new_user):  # TODO: EXCEPTION HANDLING
        cls.users_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not cls.users_pickle_file_path.exists():
            cls._save_users_list()
        else:
            cls._load_users_list()
        cls.users_list.append(new_user)
        cls._save_users_list()
        return cs.Messages.REGISTER_MSG.format(new_user.name.title())

    @classmethod
    def login(cls, username, password):
        cls._load_users_list()
        for user in cls.users_list:
            if user.username == username and user.__password == cls.convert_password_to_hash(password):
                cls.last_login_data["user"] = user
                cls.last_login_data["timestamp"] = time.time()
                cls._save_last_login_data()
                return cs.Messages.LOGIN_MSG.format(user.name.title())
        cls._clear_last_login_data()
        raise ValueError(cs.Messages.INVALID_USERNAME_OR_PASSWORD_MSG)

    @classmethod
    def logout(cls):
        user = cls.get_last_logged_in_user()
        cls._clear_last_login_data()
        return cs.Messages.LOGOUT_MSG.format(user.name.title())

    @classmethod
    def _clear_last_login_data(cls):
        cls.last_login_data["user"] = None
        cls.last_login_data["timestamp"] = 0.0
        cls._save_last_login_data()

    @classmethod
    def is_any_logged_in_user(cls):
        now = time.time()
        cls._load_last_login_data()
        user = cls.last_login_data["user"]
        if user is None or (cls.last_login_data["timestamp"] + cs.Constants.LOGIN_DURATION_SEC) < now:
            cls._clear_last_login_data()
            raise TimeoutError(cs.Messages.LOGIN_TIMEOUT_MSG)

    @classmethod
    def get_last_logged_in_user(cls) -> None | typing.Self:
        cls.is_any_logged_in_user()
        return cls.last_login_data["user"]

    @classmethod
    def find_last_logged_in_user_in_users_list(cls) -> typing.Self:
        cls._load_users_list()
        last_logged_in_user = cls.get_last_logged_in_user()
        for user in cls.users_list:
            if user == last_logged_in_user:
                cls.last_login_data['user'] = user
                return user

    def edit_my_profile_info(self, name=None, username=None, password=None, confirm_password=None):
        try:
            if password and confirm_password:
                self.__password = validators.User.validate_password(password, confirm_password)
            elif (password and not confirm_password) or (not password and confirm_password):
                raise ValueError(cs.Messages.PASS_AND_CONFIRM_PASS_REQUIRED_MSG)
            if name:
                self.name = name  # validation by setter
            if username:
                self.username = username  # validation by setter
        except Exception:
            raise
        else:
            User._save_last_login_data()
            User._save_users_list()
            return cs.Messages.SUCCESSFUL_USER_INFO_UPDATE_MSG

    def view_my_profile_info(self):
        print(self)

    def delete_corresponding_contact_pickle_file(self):
        if self.contacts_pickle_file_path.exists():
            self.contacts_pickle_file_path.unlink()

    def __str__(self):
        self_str = ""
        ignore_attributes = ['_User__password', '_contacts_pickle_file_path']
        print()
        for attribute, value in self.__dict__.items():
            if attribute not in ignore_attributes:
                self_str += f"\033[92m{attribute.strip('_').replace('_', ' ')}: \033[93m{value}\033[0m\n"
        return self_str

    def __repr__(self):
        return str(self)


class AdminUser(User):
    @staticmethod
    def search_user(user_id="", name="", username="") -> list:
        User.is_any_logged_in_user()
        User._load_users_list()
        matched_users = []
        pattern = r".*{}.*"
        for user in User.users_list:
            user_id_match_res = name_search_res = username_search_res = True

            if user_id:
                user_id = validators.validate_uuid(user_id)
                user_id_match_res = re.match(pattern.format(user_id), user.user_id)
            else:
                if name:
                    name_search_res = re.search(pattern.format(name), user.name)
                if username:
                    username_search_res = re.search(pattern.format(username), user.username)
            if user_id_match_res and name_search_res and username_search_res:
                matched_users.append(user)

        if matched_users:
            return matched_users
        raise ValueError(cs.Messages.NO_SEARCH_RESULT_MSG)

    @classmethod
    def delete_user(cls, *, user_id):
        cls._load_users_list()
        for user in cls.users_list:
            if user.user_id == user_id:
                cls.users_list.remove(user)
                cls._save_users_list()
                user.delete_corresponding_contact_pickle_file()
                last_logged_in_user = cls.get_last_logged_in_user()
                if user == last_logged_in_user:
                    cls._clear_last_login_data()
                return cs.Messages.DELETE_USER_MSG.format(user_id)
        raise ValueError(cs.Messages.INVALID_USER_ID_MSG.format(user_id))

    @classmethod
    def delete_all_users(cls):
        cls.is_any_logged_in_user()
        cls._load_users_list()
        for user in cls.users_list:
            user.delete_corresponding_contact_pickle_file()
        cls.users_list.clear()
        cls._save_users_list()
        cls._clear_last_login_data()

    @staticmethod
    def view_search_result(search_result_list: list):
        if isinstance(search_result_list, list):
            for i, user in enumerate(search_result_list, 1):
                print(f"\033[94m{'-' * 40}( {i} ){'-' * 40}\033[0m")
                print(user)

    @staticmethod
    def view_all_users():
        AdminUser.view_search_result(AdminUser.search_user())

    @classmethod
    def register(cls, new_user):
        cls.is_any_logged_in_user()
        return super().register(new_user)

    @classmethod
    def edit_another_user_profile_info(cls, *, user_id, name=None, username=None, password=None, confirm_password=None):
        search_result = cls.search_user(user_id)
        if search_result:
            user = search_result[0]
            return user.edit_my_profile_info(name=name, username=username, password=password,
                                             confirm_password=confirm_password)


class RegularUser(User):
    @classmethod
    def register(cls, new_user):
        try:
            cls.is_any_logged_in_user()
        except TimeoutError:
            return super().register(new_user)
        else:
            raise TypeError(cs.Messages.REGISTER_DURING_LOGIN_SESSION_MSG)
