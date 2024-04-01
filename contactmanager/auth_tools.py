from user import User
import constants as cs
from pickle_handler import PickleHandler


def who_has_access(*, authorized_user_types_list):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = User.get_last_logged_in_user()
            for user_type in authorized_user_types_list:
                if isinstance(user, user_type):
                    return func(*args, **kwargs)
            raise PermissionError(cs.Messages.NOT_AUTHORIZED_MSG)

        return wrapper

    return decorator


def who_can_provide_params(*, authorized_user_types_list, restricted_params_list: list):
    """
    Params in decorated function should be passed by keyword
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            user = User.get_last_logged_in_user()
            # Check is there any restricted params in kwrags
            for param in restricted_params_list:
                # if param is in kwargs, run the func
                if kwargs.get(param):
                    # if the current user in restricted_params_list
                    for user_type in authorized_user_types_list:
                        if isinstance(user, user_type):
                            return func(*args, **kwargs)
                    raise PermissionError(cs.Messages.NOT_AUTHORIZED_MSG)
            # if param is not in kwargs, run the func
            return func(*args, **kwargs)

        return wrapper

    return decorator
