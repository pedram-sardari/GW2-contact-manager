import pytest
import sys
# sys.path.append(r"C:\Users\pedis\OneDrive\Desktop\python_110\weeks\week12\GW2\pickle\GW2-contact-manager\contactmanager")
from contactmanager.user import User

# @pytest.fixture(scope="module")
@pytest.fixture()
def user():
    return User('reza', 'reza_palang', '1234a1234@', '1234a1234@')


def test_register(user):
    assert user.name == 'reze'
