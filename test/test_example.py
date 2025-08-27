
# ~ assert condition, message
# ~ condition → evaluated as True or False
# ~ message → only shown if the assertion fails


"""def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False """

"""def test_list():
    num_list = [1,2,3,4,5,6]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)  # &✅ passes, all numbers are truthy (no 0 or False)
    assert not any(any_list) # &✅ passes, any_list only has False values"""

"""import pytest


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture  # ~ don’t have to write the same setup again and again.
def default_employee():
    return Student('John', 'Doe', 'Computer Science', 3)

def test_major(default_employee):
    assert default_employee.major == "Computer Science"

def test_person_initialization():
    p =Student('John', 'Doe', 'Computer Science', 3)
    assert p.first_name == 'John', 'First name should be Dwiti'
    assert p.last_name == 'Doe', 'Last name should be Doe'
    assert p.major == 'Computer Science'
    assert p.years == 3 """

