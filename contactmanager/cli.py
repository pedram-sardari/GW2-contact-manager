import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import argparse
import constants as cs
from user import AdminUser, RegularUser, User


def register(**kwargs):
    kwargs.pop('func')
    admin = kwargs.pop('admin')
    regular = kwargs.pop('regular')
    try:
        new_user = None
        if admin:
            new_user = AdminUser(**kwargs)
        elif regular:
            new_user = RegularUser(**kwargs)
        if new_user:
            print(User.register(new_user))
    except Exception as error:
        print(cs.Messages.Error_FORMAT_MSG.format(error))


def login(**kwargs):
    kwargs.pop('func')
    try:
        msg = User.login(**kwargs)
        print(msg)
    except Exception as error:
        print(cs.Messages.Error_FORMAT_MSG.format(error))


def logout(**kwargs):
    try:
        msg = User.logout()
        print(msg)
    except Exception as error:
        print(cs.Messages.Error_FORMAT_MSG.format(error))


def view_my_profile_info(**kwargs):
    try:
        User.view_my_profile_info()
    except Exception as error:
        print(cs.Messages.Error_FORMAT_MSG.format(error))


def edit_my_profile_info(**kwargs):
    kwargs.pop('func')
    print(kwargs)
    try:
        msg = User.edit_my_profile_info(**kwargs)
        print(msg)
    except Exception as error:
        print(cs.Messages.Error_FORMAT_MSG.format(error))


global_parser = argparse.ArgumentParser(
    prog='ContactManager',
    description='You can register in our system and then create and manage your contacts list'
)
# ================================================(user management)=================================
subparsers = global_parser.add_subparsers(title='subcommands', required=True,
                                          help='User and Contact Management command')
# ---------------------------------------------( register )-----------------------------------------
register_parser = subparsers.add_parser('register', help='Use this command to register in our system.')
# user_type
user_type = register_parser.add_mutually_exclusive_group(required=True)
user_type.add_argument('-r', '--regular', action='store_true', help='The regular user')
user_type.add_argument('-a', '--admin', action='store_true', help='The admin user')
# register parameters
register_parser.add_argument('-n', '--name', required=True, help='Enter your name (without any space)')
register_parser.add_argument('-u', '--username', required=True, help='Enter your username')
register_parser.add_argument('-p', '--password', required=True, help='Enter your password')
register_parser.add_argument('-c', '--confirm_password', required=True, help='Re-enter your password')
register_parser.set_defaults(func=register)

# ---------------------------------------------( login )-----------------------------------------
login_parser = subparsers.add_parser('login', help='Use this command to login in our system.')
login_parser.add_argument('-u', '--username', required=True, help='Enter your username')
login_parser.add_argument('-p', '--password', required=True, help='Enter your password')
login_parser.set_defaults(func=login)

# ---------------------------------------------( logout )-----------------------------------------
logout_parser = subparsers.add_parser('logout', help='Use this command to logout.')
logout_parser.set_defaults(func=logout)

# ---------------------------------------------( view my profile info )-----------------------------------------
view_my_profile_info_parser = subparsers.add_parser('view_my_profile_info', help='Shows your profile information.')
view_my_profile_info_parser.set_defaults(func=view_my_profile_info)
# ---------------------------------------------( edit my info )-----------------------------------------
edit_my_info_parser = subparsers.add_parser('edit_my_profile_info', help='Use this command to edit your profile info.')
edit_my_info_parser.add_argument('-n', '--name', default=None, help='Enter your name')
edit_my_info_parser.add_argument('-u', '--username', default=None, help='Enter your username')
edit_my_info_parser.add_argument('-p', '--password', default=None, help='Enter your password')
edit_my_info_parser.add_argument('-c', '--confirm_password', default=None, help='Re-enter your password')
edit_my_info_parser.set_defaults(func=edit_my_profile_info)

# ================================================( contact management )=================================


# call func
args = global_parser.parse_args()
args.func(**args.__dict__)
