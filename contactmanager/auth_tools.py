import pathlib
import time
from collections import namedtuple
import constants as cs
from pickle_handler import PickleHandler

login_record = namedtuple("login_record", ["user_id", "user_type", "login_timestamp"])
empty_login_record = login_record(user_id="", user_type="", login_timestamp=0.0)
last_login_pickle_file_path = pathlib.Path(cs.Paths.LAST_LOGIN_PICKLE_FILE_PATH)


def save_last_login_record(last_login_record=empty_login_record):
    last_login_pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
    with PickleHandler(file_path=str(last_login_pickle_file_path), mode='r') as f:
        f.write(last_login_record)


def load_last_login_record() -> login_record:
    if not last_login_pickle_file_path.exists():
        save_last_login_record()
    else:
        with PickleHandler(file_path=str(last_login_pickle_file_path), mode='w') as f:
            return f.read()


def clear_last_login_record():
    save_last_login_record()


def get_last_logged_in_user_id():
    now = time.time()
    last_login_record = load_last_login_record()
    if (last_login_record.login_timestamp + cs.Constants.LOGIN_DURATION_SEC) < now:
        clear_last_login_record()
        raise TimeoutError(cs.Messages.LOGIN_TIMEOUT_MSG)
    return last_login_record.user_id


def provide_user_id(func):
    def wrapper(*args, **kwargs):
        pass

    return wrapper


def who_has_access(user_types_list):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with PickleHandler(cs.Paths.LAST_LOGIN_PICKLE_FILE_PATH, 'r') as f:
                last_login_record = f.read()
                user = last_login_record['user']
                if user is not None:
                    for user_type in user_types_list:
                        if isinstance(user, user_type):
                            return func(*args, **kwargs)
                    raise PermissionError(cs.Messages.NOT_AUTHORIZED_MSG)
            raise TimeoutError(cs.Messages.LOGIN_TIMEOUT_MSG)

        return wrapper

    return decorator
