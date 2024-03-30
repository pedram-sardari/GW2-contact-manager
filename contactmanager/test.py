import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# from contactmanager.contact import Contact
from contactmanager.user import User, AdminUser, RegularUser
import auth_tools
import sample_data.fake_record_genarator as frg


def user():
    print("===================================================( User )==============================================")

    # ----------------------------------------------------( registration )---------------------------------------------
    # user_info = {"name": "jack", "username": "jack_sparrow", "password": "1234a1234a", "confirm_password": "1234a1234a"}
    # user_info = {"name": "sara", "username": "sara_ninja", "password": "1234a1234a", "confirm_password": "1234a1234a"}
    # user_info = {"name": "samad", "username": "samad_dj", "password": "1234a1234a", "confirm_password": "1234a1234a"}

    def register(**kwargs):
        new_user = None
        user_type = kwargs.pop('user_type')
        print(kwargs)
        if user_type == AdminUser.__name__:
            new_user = AdminUser(**kwargs)
        elif user_type == RegularUser.__name__:
            new_user = RegularUser(**kwargs)
        if new_user:
            User.register(new_user)
        else:
            raise TypeError("invalid user type")

    for user_info in frg.read_fake_csv():
        try:
            pass
            # register(**user_info)
        except Exception as error:
            print(error)

    User._load_users_list()
    # print(User.users_list)

    # -------------------------------------------------------( login )-------------------------------------------------
    # User.login("jack_sparrow", "1234a1234a")
    # User.login("sara_ninja", "1234a1234a")
    # User.login("maro_u", "1818")
    # login_data = User.get_last_logged_in_user()
    # print(login_data)
    # User.logout()
    # User.login("maro_u", "4321")

    # ------------------------------------------------------( search )------------------------------------------------
    # print(AdminUser.search_user(name="Lau", username="ed"))
    # AdminUser.view_search_result(AdminUser.search_user(name="", username=""))
    # ------------------------------------------------------( view )------------------------------------------------
    # user = User.get_last_logged_in_user()
    # user.view_my_profile_info()
    AdminUser.view_all_users()

    # -------------------------------------------------------( edit )-------------------------------------------------
    # User.edit_my_profile_info("Jack",) #"Peter_spider",)
    # User.edit_logged_in_user("maro", "maro_u", "4321", "4321")
    # User.edit_logged_in_user(password="1818", confirm_password="1818")

    # ------------------------------------------------------( delete )------------------------------------------------
    @auth_tools.who_has_access(user_types_list=[AdminUser, RegularUser])
    def delete_all_users():
        # AdminUser.delete_all_users()
        AdminUser.delete_user(user_id='a66d3c95-765b-4a2b-8da1-f18ca773badc')

    # delete_all_users()


def contact():
    print("================================================( Contact )============================================")
    # -------------------------------------------------------( add )---------------------------------------------------
    # con1 = Contact("Arma", 'alibabaei', 'arma@gmail.com', [["addr1", "street1, alley1"]], [["Home", "8821318"]])
    # con1 = Contact("Arma", 'alibabaei', 'arma@gmail.com', [["addr1", "street2, alley1"]],
    #                [["Home", "09122343132"],["Home", "8821318"]])
    # con1 = Contact("pedi", 'babakhodadad', 'pedi@gmail.com', [["addr1", "street1, alley1"]], [["Home", "8821318"]])
    # con1.add_contact(con1)
    # ------------------------------------------------------( edit )------------------------------------------------
    # matched_contacts = Contact.search_contact(contact_id="350416e1-71f2-463e-ab0a-9472524c18e3", first_name="",
    #                                           last_name="", email="", phone_number="")
    # print(matched_contacts)
    # for contact in matched_contacts:
    #     print("before:", contact, sep="\n")
    #     contact.edit_contact(first_name="mahmodd", last_name="shafie", email="pedisdi@gmail.com",
    #                          phones=[["work", "02188493144"], ["mobile", "09123421321"], ["Home", "0000000000"]])
    #     print("after:", contact, sep="\n")

    # ------------------------------------------------------( search )------------------------------------------------
    # matched_contacts = Contact.search_contact(contact_id="b004d5ba-7a5d-4860-b807-f468a5b8d57e", first_name="",
    #                                           last_name="", email="", phone_number="")
    # print("matched_contacts:", matched_contacts)

    # ------------------------------------------------------( delete )------------------------------------------------
    # Contact.delete_contact(first_name="mahmodd", phone_number="")
    # Contact.delete_all_contacts()
    # -------------------------------------------------------( view )-------------------------------------------------
    # Contact.view_all_contacts()


if __name__ == "__main__":
    user()
    contact()
