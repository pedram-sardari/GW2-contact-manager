import csv
import random
import string
from faker import Faker

fake = Faker()


def generate_password():
    charset_length = random.randint(3, 5)  # Random length between 8 and 16
    password = ""
    valid_chars = [string.ascii_letters, string.digits, list("@$!%*?&")]
    random.shuffle(valid_chars)
    for character_set in valid_chars:
        password += ''.join(random.choice(character_set) for _ in range(charset_length))
    return password


def generate_fake_users_csv():
    # Generate 100 random records
    num_records = 100
    records = []
    for _ in range(num_records):
        usertype = random.choice(["AdminUser", "RegularUser"])
        name = fake.name().split()[0]
        username = fake.user_name()
        password = generate_password()
        confirm_password = password  # Assuming confirm_password is the same as password
        records.append([usertype, name, username, password, confirm_password])

    # Write records to a CSV file
    with open('users.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_type', 'name', 'username', 'password', 'confirm_password'])
        writer.writerows(records)

    print("csv file with random records generated successfully.")


def read_fake_csv(path='./sample_data/users.csv'):
    with open(path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        return [row for row in csv_reader]


if __name__ == '__main__':
    generate_fake_users_csv()
    print(read_fake_csv())
