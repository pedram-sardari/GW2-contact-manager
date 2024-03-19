class Contact:
    contact_list = []

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.addresses = {}  # addresses = {"addr1": "street1, alley1", "addr2": "st2, al2", ...}
        self.phones = {}  # phones = {"Home": "8821318", "Mobile": "9128731", ...}

    def add_contact(self, new_contact):
        if new_contact not in self.contact_list:
            self.contact_list.append(new_contact)

    def delete_contact(self, contact):
        if contact in self.contact_list:
            self.contact_list.remove(contact)

    def add_addresses(self, address, street, alley):
        self.addresses = {'address': [address, street, alley]}

    def add_phone(self, home_number, work_number):
        self.phones = {('Home', 'Work'): [home_number, work_number]}

    def __repr__(self):
        return f"first_name: {self.first_name}\nlast_name: {self.last_name}\nemail: {self.email}\nAddresses: {self.addresses}\nPhones: {self.phones}"


if __name__ == '__main__':
    con1 = Contact("Arma", 'alibabaei', 'arma@gmail.com')
    con2 = Contact("arsalan", 'babaei', 'arsalan@gmail.com')
    con1.add_contact(con1)
    con2.add_contact(con2)
    # print(Contact.contact_list)
    con1.add_addresses('tehran', 'street1', 'al2')
    con1.add_phone('02165254748', '09193636442')
    con2.add_addresses('shiraz', 'street2', 'al2')
    con2.add_phone('021765433', '099912232')
    # con2.add_addresses('shiraz', '09193636442', '021652555562')
    # con2.delete_contact(con2)
    print(con1.addresses)
    print(con1.phones)
    # print(con2.addresses)
    print(len(Contact.contact_list))
    print(Contact.contact_list)
