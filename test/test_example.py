import pytest

def test_equal_or_not_equal():
    assert 4 == 4, "This is a test assertion that should always pass"
    assert 2 + 2 != 5, "This is a simple math test that should always pass"
    

def test_is_instance():
    assert isinstance("Hello, World!", str), "This is a test to check if the variable is a string"
    assert isinstance(42, int), "This is a test to check if the variable is an integer"
    
def test_in():
    assert "apple" in ["apple", "banana", "cherry"], "This is a test to check if 'apple' is in the list"
    assert 3 not in [1, 2, 4], "This is a test to check if 3 is not in the list"
    
def test_boolean():
    assert True, "This is a test to check if the boolean value is True"
    assert not False, "This is a test to check if the boolean value is not False"

def test_none():
    assert None is None, "This is a test to check if None is None"
    assert not (None is not None), "This is a test to check if None is not something else"

def test_comparison():
    assert 5 > 3, "This is a test to check if 5 is greater than 3"
    assert 2 <= 2, "This is a test to check if 2 is less than or equal to 2"
    assert 10 >= 5, "This is a test to check if 10 is greater than or equal to 5"
    assert 7 < 8, "This is a test to check if 7 is less than 8"

def test_identity():
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]
    
    assert a is b, "This is a test to check if 'a' and 'b' are the same object"
    assert a is not c, "This is a test to check if 'a' and 'c' are not the same object"
    assert c == [1, 2, 3], "This is a test to check if 'c' has the same content as the list [1, 2, 3]"

def test_membership():
    my_list = [1, 2, 3, 4, 5]
    assert 3 in my_list, "This is a test to check if 3 is a member of the list"
    assert 6 not in my_list, "This is a test to check if 6 is not a member of the list"
    
    my_dict = {'a': 1, 'b': 2}
    assert 'a' in my_dict, "This is a test to check if 'a' is a key in the dictionary"
    assert 'c' not in my_dict, "This is a test to check if 'c' is not a key in the dictionary"

def test_type():
    assert type(42) is int, "This is a test to check if the type of 42 is int"
    assert type("Hello") is str, "This is a test to check if the type of 'Hello' is str"
    assert type([1, 2, 3]) is list, "This is a test to check if the type of [1, 2, 3] is list"
    assert type({'key': 'value'}) is dict, "This is a test to check if the type of {'key': 'value'} is dict"

def test_list():
    my_list = [1, 2, 3]
    any_lust = [False, False, False]
    assert len(my_list) == 3, "This is a test to check if the length of the list is 3"
    assert my_list[0] == 1, "This is a test to check if the first element of the list is 1"
    assert my_list[-1] == 3, "This is a test to check if the last element of the list is 3"
    assert all(my_list), "This is a test to check if all elements in the list are truthy"
    assert not any(any_lust), "This is a test to check if any element in the list is truthy"
    

def test_truthiness():
    assert bool(1), "This is a test to check if 1 is truthy"
    assert not bool(0), "This is a test to check if 0 is falsy"
    assert bool("non-empty string"), "This is a test to check if a non-empty string is truthy"
    assert not bool(""), "This is a test to check if an empty string is falsy"
    
class Student:
    def __init__(self, name: str, age: int, major: str, grade: str, year: int = 2025):
        self.name = name
        self.age = age
        self.major = major
        self.grade = grade
        self.year = year

@pytest.fixture
def default_student():
    return Student(name="John Doe", age=20, major="Computer Science", grade="A")

def test_student_initialization(default_student):
    s = default_student
    # Check if the student object is initialized correctly
    assert s.name == "John Doe", "This is a test to check if the student's name is initialized correctly"
    assert s.age == 20, "This is a test to check if the student's age is initialized correctly"
    assert s.major == "Computer Science", "This is a test to check if the student's major is initialized correctly"
    assert s.grade == "A", "This is a test to check if the student's grade is initialized correctly"
    assert s.year == 2025, "This is a test to check if the student's year is initialized correctly"
    




