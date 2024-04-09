from contactmanager.user import User
import constants as cs
import cli

User.load_users_list()
User.load_last_login_data()
# call func
args = cli.global_parser.parse_args()
try:
    print(args)
    args.func(**args.__dict__)
except Exception as error:
    print(cs.Messages.Error_FORMAT_MSG.format(error))
User.save_users_list()
User.save_last_login_data()
