import auth_tools
from contactmanager.contact import Contact
from contactmanager.user import AdminUser, RegularUser, User


def _create_new_user(**kwargs):
    kwargs.pop('func')
    admin = kwargs.pop('admin')
    regular = kwargs.pop('regular')
    new_user = None
    if admin:
        new_user = AdminUser(**kwargs)
    elif regular:
        new_user = RegularUser(**kwargs)
    return new_user


def register(**kwargs):
    another_user = kwargs.pop('another_user')
    new_user = _create_new_user(**kwargs)
    if another_user:
        msg = _register_another_user(new_user)
    else:
        msg = RegularUser.register(new_user)
    print(msg)


@auth_tools.who_has_access(authorized_user_types_list=[AdminUser])
def _register_another_user(new_user):
    return AdminUser.register(new_user)


def login(**kwargs):
    kwargs.pop('func')
    msg = User.login(**kwargs)
    print(msg)


def logout(**kwargs):
    msg = User.logout()
    print(msg)


def view_my_info(**kwargs):
    user = User.get_last_logged_in_user()
    user.view_my_profile_info()


def edit_user(**kwargs):
    kwargs.pop('func')
    user_id = kwargs.pop('user_id')
    if user_id:
        msg = _edit_another_user_info(user_id=user_id, **kwargs)
    else:
        msg = _edit_my_info(**kwargs)
    print(msg)


def _edit_my_info(**kwargs):
    user = User.get_last_logged_in_user()
    return user.edit_my_profile_info(**kwargs)


@auth_tools.who_has_access(authorized_user_types_list=[AdminUser])
def _edit_another_user_info(**kwargs):
    return AdminUser.edit_another_user_profile_info(**kwargs)


@auth_tools.who_has_access(authorized_user_types_list=[AdminUser])
def search_user(**kwargs):
    kwargs.pop('func')
    search_result = AdminUser.search_user(**kwargs)
    AdminUser.view_search_result(search_result)


@auth_tools.who_has_access(authorized_user_types_list=[AdminUser])
def view_all_users(**kwargs):
    kwargs.pop('func')
    AdminUser.view_all_users()


@auth_tools.who_has_access(authorized_user_types_list=[AdminUser])
def delete_user(**kwargs):
    kwargs.pop('func')
    msg = AdminUser.delete_user(**kwargs)
    print(msg)


@auth_tools.who_can_provide_params(authorized_user_types_list=[AdminUser], restricted_params_list=['user_id'])
def _set_contacts_list(**kwargs):
    kwargs.pop('func')
    user_id = kwargs.pop('user_id')
    Contact.set_contacts_list(user_id=user_id)
    return kwargs


def view_all_con(**kwargs):
    _set_contacts_list(**kwargs)
    Contact.view_all_contacts()


def add_con(**kwargs):
    kwargs = _set_contacts_list(**kwargs)
    new_contact = Contact(**kwargs)
    msg = Contact.add_contact(new_contact)
    print(msg)


def search_con(**kwargs):
    kwargs = _set_contacts_list(**kwargs)
    search_result = Contact.search_contact(**kwargs)
    Contact.view_search_result(search_result)


def edit_con(**kwargs):
    kwargs = _set_contacts_list(**kwargs)
    contact_id = kwargs.pop('contact_id')
    search_result = Contact.search_contact(contact_id=contact_id)
    contact = search_result[0]
    print(f"\033[91m{'-' * 40}( Before ){'-' * 40}\033[0m")
    print(contact)
    contact.edit_contact(**kwargs)
    print(f"\033[92m{'-' * 40}( After ){'-' * 40}\033[0m")
    print(contact)


def delete_con(**kwargs):
    kwargs = _set_contacts_list(**kwargs)
    if kwargs.pop('all'):
        msg = Contact.delete_all_contacts()
    else:
        contact_id = kwargs.pop('contact_id')
        msg = Contact.delete_contact(contact_id=contact_id)
    print(msg)


