import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from contactmanager.user import User
import constants as cs
import cli_functions as cli_func


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
register_group = register_parser.add_mutually_exclusive_group(required=True)
register_group.add_argument('-r', '--regular', action='store_true', help='The regular user')
register_group.add_argument('-a', '--admin', action='store_true', help='The admin user')
# register parameters
register_parser.add_argument('--another-user', action='store_true', help='Use to add a new user '
                                                                         '(Only for Admin users)')
register_parser.add_argument('-n', '--name', required=True, help='Enter your name (without any space)')
register_parser.add_argument('-u', '--username', required=True, help='Enter your username')
register_parser.add_argument('-p', '--password', required=True, help='Enter your password')
register_parser.add_argument('-c', '--confirm_password', required=True, help='Re-enter your password')
register_parser.set_defaults(func=cli_func.register)

# ---------------------------------------------( login )-----------------------------------------
login_parser = subparsers.add_parser('login', help='Use this command to login in our system.')
login_parser.add_argument('-u', '--username', required=True, help='Enter your username')
login_parser.add_argument('-p', '--password', required=True, help='Enter your password')
login_parser.set_defaults(func=cli_func.login)

# ---------------------------------------------( logout )-----------------------------------------
logout_parser = subparsers.add_parser('logout', help='Use this command to logout.')
logout_parser.set_defaults(func=cli_func.logout)

# ----------------------------------------( view my profile info )------------------------------------
view_my_profile_info_parser = subparsers.add_parser('view-my-info', help='Shows your profile information.')
view_my_profile_info_parser.set_defaults(func=cli_func.view_my_info)

# ----------------------------------------( view all users )------------------------------------
view_all_users_parser = subparsers.add_parser('view-all-users', help='Show all existing users (Only for Admin users)')
view_all_users_parser.set_defaults(func=cli_func.view_all_users)

# ---------------------------------------------( edit my info )-----------------------------------------
edit_my_info_parser = subparsers.add_parser('edit-user', help="Use this command to edit your (or another user's)"
                                                              " profile info.")
edit_my_info_parser.add_argument('-i', '--user_id', help="Enter another user's ID. (Only for Admin users)")
edit_my_info_parser.add_argument('-n', '--name', default="", help='Enter your name')
edit_my_info_parser.add_argument('-u', '--username', default="", help='Enter your username')
edit_my_info_parser.add_argument('-p', '--password', default="", help='Enter your password')
edit_my_info_parser.add_argument('-c', '--confirm_password', default="", help='Re-enter your password')
edit_my_info_parser.set_defaults(func=cli_func.edit_user)

# ---------------------------------------------( search user)-----------------------------------------
search_user_parser = subparsers.add_parser('search-user', help="Search users by 'id', 'name', and 'username'"
                                                               "(Only for Admin users)")
search_user_parser.add_argument('-i', '--user_id', default='', help='Provide a user id (UUID)')
search_user_parser.add_argument('-n', '--name', default="", help='Enter your name')
search_user_parser.add_argument('-u', '--username', default="", help='Enter your username')
search_user_parser.set_defaults(func=cli_func.search_user)
# ---------------------------------------------( delete user)-----------------------------------------
delete_user_parser = subparsers.add_parser('delete-user', help="Delete a user by id (Only for Admin users)")
delete_user_parser.add_argument('-i', '--user_id', default='', help='Provide a user id (UUID)')
delete_user_parser.set_defaults(func=cli_func.delete_user)
# ================================================( contact management )=================================

User.load_users_list()
User.load_last_login_data()
# call func
args = global_parser.parse_args()
try:
    print(args)
    args.func(**args.__dict__)
except Exception as error:
    print(cs.Messages.Error_FORMAT_MSG.format(error))
User.save_users_list()
User.save_last_login_data()
