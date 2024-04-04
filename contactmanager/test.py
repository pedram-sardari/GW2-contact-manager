import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from contactmanager.contact import Contact
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

    User.load_users_list()
    print(User.users_list)

    # -------------------------------------------------------( login )-------------------------------------------------
    # User.login("jack_sparrow", "1234a1234a")
    # User.login("paulsmith", "FZP@?%876")
    # User.login("dhoward", "834!!$Uxs")
    # User.login("pey_1s", "1234a1234a@")
    # User.login("sara_ninja", "1234a1234a")
    # User.login("maro_u", "1818")
    # login_data = User.get_last_logged_in_user()
    # print(login_data)
    # User.logout()
    # User.login("maro_u", "4321")

    # ------------------------------------------------------( search )------------------------------------------------
    # AdminUser.view_search_result(AdminUser.search_user(user_id="b792a475-c62a-4013-93e5-340a4e6884e2", name="Lau", username=""))
    # AdminUser.view_search_result(AdminUser.search_user(name="", username=""))
    # ------------------------------------------------------( view )------------------------------------------------
    # user = User.get_last_logged_in_user()
    # user.view_my_profile_info()
    # AdminUser.view_all_users()

    # -------------------------------------------------------( edit )-------------------------------------------------
    # user = User.find_last_logged_in_user_in_users_list()
    # print("9***************", id(User.users_list))
    # User.edit_my_profile_info("Jack",) #"Peter_spider",)
    # user.edit_my_profile_info(name="Jack", username="")  # "Peter_spider",)

    # ------------------------------------------------------( delete )------------------------------------------------
    # @auth_tools.who_has_access(authorized_user_types_list=[RegularUser, ])
    def delete_all_users():
        AdminUser.delete_all_users()
        # AdminUser.delete_user(user_id='a66d3c95-765b-4a2b-8da1-f18ca773badc')

    # delete_all_users()


def contact():
    print("================================================( Contact )============================================")
    # -------------------------------------------------------( add )---------------------------------------------------
    # con1 = Contact("Arma", 'alibabaei', 'arma@gmail.com', [["addr1", "street1, alley1"]], [["Home", "8821318"]])
    # con1 = Contact("Arma", 'alibabaei', 'arma@gmail.com', [["addr1", "street2, alley1"]],
    #                [["Home", "09122343132"],["Home", "8821318"]])
    # con1 = Contact("samira", 'babakhodadad', 'pedi@gmail.com', [["addr1", "street1, alley1"]], [["Home", "8821318"]])
    # user = User.get_last_logged_in_user()
    # Contact.set_contacts_list(user_id="b67fb395-2917-49d4-b1ee-ee2e12021c08")
    # con1.add_contact(con1)
    # ------------------------------------------------------( edit )------------------------------------------------
    # matched_contacts = Contact.search_contact(contact_id="e58e88c7-f9ad-4766-8bc8-62ec790e11a6", first_name="",
    #                                           last_name="", email="", phone_number="")
    # print(matched_contacts)
    # for contact in matched_contacts:
    #     print("before:", contact, sep="\n")
    #     print("test:********", id(contact))
    #     contact.edit_contact(first_name="mahmodd", last_name="shafie", email="pedisdi@gmail.com",
    #                          phones=[["work", ""], ["mobile", ""], ["Home", "232"]])
    #     print("after:", contact, sep="\n")
    #
    # ------------------------------------------------------( search )------------------------------------------------
    # search_result= Contact.search_contact(contact_id="e58e88c7-f9ad-4766-8bc8-62ec790e11a6")
    # search_result = Contact.search_contact(first_name='', phone_number='138')
    # print("matched_contacts:", search_result)

    # ------------------------------------------------------( delete )------------------------------------------------
    # Contact.delete_contact(contact_id="eb2d8ee4-3216-472f-b10c-e85b9e566c0c", first_name="", phone_number="")
    # Contact.delete_all_contacts()
    # -------------------------------------------------------( view )-------------------------------------------------
    # Contact.view_all_contacts()


if __name__ == "__main__":
    User.load_users_list()
    User.load_last_login_data()
    # Contact.set_contacts_list()
    user()
    contact()
    User.save_last_login_data()
    User.save_users_list()
