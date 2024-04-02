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
register_mutually_exclusive = register_parser.add_mutually_exclusive_group(required=True)
register_mutually_exclusive.add_argument('-r', '--regular', action='store_true', help='The regular user')
register_mutually_exclusive.add_argument('-a', '--admin', action='store_true', help='The admin user')
# register parameters
register_parser.add_argument('--another-user', action='store_true', help='Use to add a new user '
                                                                         '\033[91m(Only Admin Users)\033[0m')
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

# ----------------------------------------( view my info )---------------------------------------
view_my_profile_info_parser = subparsers.add_parser('view-my-info', help='Shows your profile information.')
view_my_profile_info_parser.set_defaults(func=cli_func.view_my_info)

# ----------------------------------------( view all users )------------------------------------
view_all_users_parser = subparsers.add_parser('view-all-users',
                                              help='Show all existing users \033[91m(Only Admin Users)\033[0m')
view_all_users_parser.set_defaults(func=cli_func.view_all_users)

# ---------------------------------------------( edit user )-----------------------------------------
edit_my_info_parser = subparsers.add_parser('edit-user', help="Use this command to edit your (or another user's)"
                                                              " profile info.")
edit_my_info_parser.add_argument('-i', '--user-id', help="Enter another user's ID. \033[91m(Only Admin Users)\033[0m")
edit_my_info_parser.add_argument('-n', '--name', default="", help='Enter your name')
edit_my_info_parser.add_argument('-u', '--username', default="", help='Enter your username')
edit_my_info_parser.add_argument('-p', '--password', default="", help='Enter your password')
edit_my_info_parser.add_argument('-c', '--confirm_password', default="", help='Re-enter your password')
edit_my_info_parser.set_defaults(func=cli_func.edit_user)

# ---------------------------------------------( search user)-----------------------------------------
search_user_parser = subparsers.add_parser('search-user', help="Search users by 'id', 'name', and 'username'"
                                                               "\033[91m(Only Admin Users)\033[0m")
search_user_parser.add_argument('-i', '--user-id', default='', help='Provide a user id (UUID)')
search_user_parser.add_argument('-n', '--name', default="", help='Enter your name')
search_user_parser.add_argument('-u', '--username', default="", help='Enter your username')
search_user_parser.set_defaults(func=cli_func.search_user)

# ---------------------------------------------( delete user)-----------------------------------------
delete_user_parser = subparsers.add_parser('delete-user', help="Delete a user by id \033[91m(Only Admin Users)\033[0m")
delete_user_parser.add_argument('-i', '--user-id', default='', help='Provide a user id (UUID)')
delete_user_parser.set_defaults(func=cli_func.delete_user)

# ================================================( contact management )=================================

# ---------------------------------------------( view all contacts )-----------------------------------------
view_all_contacts_parser = subparsers.add_parser('view-contacts', help='List all contacts')
view_all_contacts_parser.add_argument('-i', '--user-id',
                                      help="Enter another user's ID. \033[91m(Only Admin Users)\033[0m")
view_all_contacts_parser.set_defaults(func=cli_func.view_all_con)

# ---------------------------------------------( add contact)-----------------------------------------
add_contact_parser = subparsers.add_parser('add-contact',
                                           help="Add a contact to your (or other user's contacts) list")
add_contact_parser.add_argument('-i', '--user-id', help="Add a contact to a user's list with this user_id")
add_contact_parser.add_argument('-f', '--first-name', required=True, help="Contact's first name")
add_contact_parser.add_argument('-l', '--last-name', required=True, help="Contact's last name")
add_contact_parser.add_argument('-e', '--email', required=True, help="Contact's email address")
add_contact_parser.add_argument('-p', '--phones', action='append', nargs=2, default=list(),
                                metavar=('LABEL', 'PHONE_NUMBER'),
                                help="Contact's phone number. (each phone number needs a 'label')")
add_contact_parser.add_argument('-a', '--addresses', action='append', default=list(), nargs=2,
                                metavar=('LABEL', 'ADDRESS'),
                                help="Contact's address. (each address needs a 'label')")
add_contact_parser.set_defaults(func=cli_func.add_con)

# ---------------------------------------------( search contact)-----------------------------------------
search_contact_parser = subparsers.add_parser('search-contact',
                                              help="Search through your (or another user's) contacts list. "
                                                   "Provide user ID or other fields. If 'other fields' are provided, "
                                                   "they are combined using 'and'.")
search_contact_parser.add_argument('-i', '--user-id', default='',
                                   help="Add a contact to a user's list with this user_id")
search_contact_parser.add_argument('--contact-id', default='', help="Contact's ID (required)")
search_contact_parser.add_argument('-f', '--first-name', default='', help="Contact's first name")
search_contact_parser.add_argument('-l', '--last-name', default='', help="Contact's last name")
search_contact_parser.add_argument('-e', '--email', default='', help="Contact's email address")
search_contact_parser.add_argument('-p', '--phone-number', default='', help="Contact's phone numbers")
search_contact_parser.set_defaults(func=cli_func.search_con)

# ---------------------------------------------( edit contact)-----------------------------------------
edit_contact_parser = subparsers.add_parser('edit-contact',
                                            help="Edit a contact of your (or another user's) contacts list.")
edit_contact_parser.add_argument('-i', '--user-id', default='',
                                 help="Add a contact to a user's list with this user_id")
edit_contact_parser.add_argument('--contact-id', required=True, help="Contact's ID (required)")
edit_contact_parser.add_argument('-f', '--first-name', default='', help="Contact's first name")
edit_contact_parser.add_argument('-l', '--last-name', default='', help="Contact's last name")
edit_contact_parser.add_argument('-e', '--email', default='', help="Contact's email address")
edit_contact_parser.add_argument('-p', '--phones', action='append', nargs=2, default=list(),
                                 metavar=('LABEL', 'PHONE_NUMBER'),
                                 help="Contact's phone number. (each phone number needs a 'label')")
edit_contact_parser.add_argument('-a', '--addresses', action='append', default=list(), nargs=2,
                                 metavar=('LABEL', 'ADDRESS'),
                                 help="Contact's address. (each address needs a 'label')")
edit_contact_parser.set_defaults(func=cli_func.edit_con)

# ---------------------------------------------( delete contact )-----------------------------------------
delete_contact_parser = subparsers.add_parser('delete-contact',
                                              help="Edit a contact of your (or another user's) contacts list.")
delete_contact_parser.add_argument('-i', '--user-id', default='',
                                   help="Add a contact to a user's list with this user_id")
delete_contact_mutually_exclusive = delete_contact_parser.add_mutually_exclusive_group(required=True)
delete_contact_mutually_exclusive.add_argument('--contact-id', help="Contact's ID (required) ")
delete_contact_mutually_exclusive.add_argument('-a', '--all', action='store_true', help="Delete all contacts")
delete_contact_mutually_exclusive.set_defaults(func=cli_func.delete_con)

# ================================================( parsing args )=================================

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
