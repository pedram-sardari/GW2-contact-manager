from user import User
from pickle_handler import PickleHandler


def main():
    # user1 = User("jack", "jack_sparrow", "1234", "1234")
    # user1 = User("jack", "jack_sparrow_", "1234", "1234")
    # print(user1._User__password)

    User.register("jack", "jack_sparrow", "1234", "1234")
    User.register("Sara", "sara_sparrow", "1234", "1234")
    # with PickleHandler(str(User.users_pickle_file_path), 'r') as pickle_file:

# 03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4
# f5d99d85-63da-4a4d-8a7a-613016c19594

if __name__ == "__main__":
    main()
