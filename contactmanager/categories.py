import re

import validators
import constants as cs


class Category:

    def __init__(self, categories):
        self.categories = validators.validate_categories(categories)

    def add_category(self, new_categories):
        self.categories = self.categories.union(new_categories)

    def delete_category(self, categories_to_delete):
        self.categories -= validators.validate_categories(categories_to_delete)

    def edit_category(self, new_categories: dict):
        new_set = set()
        for category in self.categories:
            updated_category = new_categories.get(category, category)
            print(updated_category)
            new_set.add(updated_category)
        self.categories = new_set

    def search_category(self, category):
        pattern = r".*{}.*"
        for cat in self.categories:
            if re.search(pattern.format(category), cat):
                return True
        return False

    def __str__(self):
        string = ""
        for key, value in self.__dict__.items():
            string += f"\033[94m{key.strip('_').replace('_', ' ')}: \033[95m{value}\033[0m\n"
        return string

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    category1 = Category({"1", "2", "3"})
    print(category1)
    category1.edit_category({"1": "10", "2": "20"})
    print(category1)
