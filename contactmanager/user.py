import hashlib
import logging
import pathlib
import re
import time
import uuid

import constants as cs
import validators
from pickle_handler import PickleHandler

# logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class User:
    users_list = []
    users_pickle_file_path = pathlib.Path(cs.Paths.USERS_FILE_PATH)
    last_login_pickle_file_path = pathlib.Path(cs.Paths.LAST_LOGIN_PICKLE_FILE_PATH)
    last_login_data = {"user_id": None, "timestamp": 0.0}

    def __init__(self, name, username, password, confirm_password):
        self._user_id = str(uuid.uuid4())
        self.user_type = self.__class__.__name__
        self._name = validators.validate_name(name)
        self._username = User.validate_username(username)
        self.__password = validators.User.validate_password(password, confirm_password)
        self._contacts_list = []

    @staticmethod
    def convert_password_to_hash(password: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(password.encode())
        return sha256.hexdigest()

    @property
    def user_id(self):
        return self._user_id

    @property
    def contacts_list(self):
        return self._contacts_list

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
        cond6 = True # TODO: CHECK CONTACTS LIST
        if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
            return True
        return False

    @staticmethod
    def load_users_list():
        if not User.users_list and User.users_pickle_file_path.exists():
            with PickleHandler(file_path=str(User.users_pickle_file_path), mode='r') as f:
                User.users_list = f.read()

    @staticmethod
    def save_users_list():
        with PickleHandler(file_path=str(User.users_pickle_file_path), mode='w') as f:
            f.write(User.users_list)

    @staticmethod
    def save_last_login_data():
        User.last_login_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
        with PickleHandler(file_path=str(User.last_login_pickle_file_path), mode='w') as f:
            f.write(User.last_login_data)

    @staticmethod
    def load_last_login_data():
        if User.last_login_pickle_file_path.exists():
            with PickleHandler(file_path=str(User.last_login_pickle_file_path), mode='r') as f:
                User.last_login_data = f.read()

    @classmethod
    def register(cls, new_user):  # TODO: EXCEPTION HANDLING
        cls.users_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
        cls.users_list.append(new_user)
        logging.info(f"User registered: {new_user.name}")
        return cs.Messages.REGISTER_MSG.format(new_user.name.title())

    @staticmethod
    def login(username, password):
        for user in User.users_list:
            if user.username == username and user.__password == User.convert_password_to_hash(password):
                User.last_login_data["user_id"] = user.user_id
                User.last_login_data["timestamp"] = time.time()
                logging.info(f"User logged in: {username}")
                return cs.Messages.LOGIN_MSG.format(user.name.title())
        User.clear_last_login_data()
        logging.warning(f"Failed login attempt for username: {username}")
        raise ValueError(cs.Messages.INVALID_USERNAME_OR_PASSWORD_MSG)

    @staticmethod
    def logout():
        user = User.get_last_logged_in_user()
        User.clear_last_login_data()
        logging.info(f"User logged out: {user.name}")
        return cs.Messages.LOGOUT_MSG.format(user.name.title())

    @staticmethod
    def clear_last_login_data():
        User.last_login_data["user_id"] = None
        User.last_login_data["timestamp"] = 0.0

    @staticmethod
    def is_any_logged_in_user() -> None | str:
        now = time.time()
        user_id = User.last_login_data["user_id"]
        if user_id is None or (User.last_login_data["timestamp"] + cs.Constants.LOGIN_DURATION_SEC) < now:
            User.clear_last_login_data()
            raise TimeoutError(cs.Messages.LOGIN_TIMEOUT_MSG)
        return user_id

    @staticmethod
    def get_last_logged_in_user():
        last_logged_in_user_id = User.is_any_logged_in_user()
        for user in User.users_list:
            if user.user_id == last_logged_in_user_id:
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
            logging.info(f"User profile updated: {self.name}")
            return cs.Messages.SUCCESSFUL_USER_INFO_UPDATE_MSG

    def view_my_profile_info(self):
        print(self)


    def __str__(self):
        self_str = "\n"
        ignore_attributes = ['_User__password', '_contacts_list']
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

    @staticmethod
    def delete_user(*, user_id):
        for user in User.users_list:
            if user.user_id == user_id:
                User.users_list.remove(user)
                last_logged_in_user_id = User.is_any_logged_in_user()
                if user.user_id == last_logged_in_user_id:
                    User.clear_last_login_data()
                logging.info(f"User deleted successfully: User ID={user_id}")
                return cs.Messages.DELETE_USER_MSG.format(user_id)
        logging.warning(f"Invalid user ID: {user_id}")
        raise ValueError(cs.Messages.INVALID_USER_ID_MSG.format(user_id))

    @staticmethod
    def delete_all_users():
        User.is_any_logged_in_user()
        User.users_list.clear()
        User.clear_last_login_data()
        logging.info("All users deleted successfully")

    @staticmethod
    def view_search_result(search_result_list: list):
        if isinstance(search_result_list, list):
            for i, user in enumerate(search_result_list, 1):
                print(f"\033[94m{'-' * 40}( {i} ){'-' * 40}\033[0m")
                print(user)
        logging.info("Viewed search results")

    @staticmethod
    def view_all_users():
        AdminUser.view_search_result(AdminUser.search_user())

    @classmethod
    def register(cls, new_user):
        User.is_any_logged_in_user()
        logging.info(f"Registered new user: {new_user.name}")
        return super().register(new_user)

    @classmethod
    def edit_another_user_profile_info(cls, *, user_id, name=None, username=None, password=None, confirm_password=None):
        search_result = cls.search_user(user_id)
        if search_result:
            user = search_result[0]
            logging.info("Edited another user's profile information")
            return user.edit_my_profile_info(name=name, username=username, password=password,
                                             confirm_password=confirm_password)


class RegularUser(User):
    @classmethod
    def register(cls, new_user):
        try:
            User.is_any_logged_in_user()
        except TimeoutError:
            return super().register(new_user)
        else:
            raise TypeError(cs.Messages.REGISTER_DURING_LOGIN_SESSION_MSG)
