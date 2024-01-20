import pytest 

from project import (
    get_person, 
    get_mrt_card, 
    is_number, 
    validate_station_number, 
    convert_to_station_number,
    create_new_person,
    create_mrt_card,
    top_up_mrt_card,
    calculate_station_number,
    calculate_fare_by_normal_rate,
    final_fare_after_discount_by_age,
    process_payment,
    Person,
    MRTCard,
)

@pytest.fixture
def person():
    return Person("myfirstname", "mylastname", 25) # adult

@pytest.fixture
def mrt_card():
    person = Person("myfirstname", "mylastname", 25) # adult
    return MRTCard(owner=person)

@pytest.fixture
def senior_mrt_card():
    person = Person("myfirstname", "mylastname", 65) # senior
    return MRTCard(owner=person)

@pytest.fixture
def student_mrt_card():
    person = Person("myfirstname", "mylastname", 18) # student
    return MRTCard(owner=person)


def test_get_person(person):
    assert get_person(person.national_id) == person
    assert get_person("not_existing_national_id") == None

def test_get_mrt_card(mrt_card):
    assert get_mrt_card(mrt_card.card_number) == mrt_card
    assert get_mrt_card("not_existing_card_number") == None

def test_is_number():
    assert is_number("12") == True
    assert is_number("word") == False
    assert is_number("word1234") == False
    assert is_number("123 ") == False

def test_validate_station_number():
    assert validate_station_number(1) == True 
    assert validate_station_number(38) == True 
    assert validate_station_number(12) == True 
    assert validate_station_number(-1) == False 
    assert validate_station_number(40) == False 

def test_convert_to_station_number():
    assert convert_to_station_number("Lak Song") == 38
    assert convert_to_station_number("Huai Khwang") == 18
    assert convert_to_station_number("Lat Phrao") == 15
    assert convert_to_station_number("12") == 12
    with pytest.raises(ValueError):
        convert_to_station_number("-1")
    with pytest.raises(ValueError):
        convert_to_station_number("40")
    with pytest.raises(ValueError):
        convert_to_station_number("not-existing-name")

def test_create_new_person():
    # normal case
    person = create_new_person("firstname", "lastname", 20)
    assert person.first_name == "firstname"
    assert person.last_name == "lastname"
    assert person.age == 20
    assert len(person.national_id) == 13

    # invalid case for first name
    with pytest.raises(ValueError) as err:
        # having space
        create_new_person("first name", "lastname", 20)
        assert str(err) == "Invalid first name."
    with pytest.raises(ValueError) as err:
        # having number
        create_new_person("firstname1234", "lastname", 20)
        assert str(err) == "Invalid first name."
    with pytest.raises(ValueError) as err:
        # wired char
        create_new_person("first-name", "lastname", 20)
        assert str(err) == "Invalid first name."

    # invalid case for last name
    with pytest.raises(ValueError) as err:
        # having space
        create_new_person("firstname", "last name", 20)
        assert str(err) == "Invalid last name."
    with pytest.raises(ValueError) as err:
        # having number
        create_new_person("firstname", "lastname1234", 20)
        assert str(err) == "Invalid last name."
    with pytest.raises(ValueError) as err:
        # wired char
        create_new_person("firstname", "last-name", 20)
        assert str(err) == "Invalid last name."

    # invalid case for age
    with pytest.raises(ValueError) as err:
        create_new_person("firstname", "lastname", -1)
    with pytest.raises(ValueError) as err:
        create_new_person("firstname", "lastname", 0)
    with pytest.raises(ValueError) as err:
        create_new_person("firstname", "lastname", 3000)

def test_open_mrt_card(person):
    mrt_card = create_mrt_card(person)
    assert mrt_card.owner == person
    assert mrt_card.money == 50
    assert len(mrt_card.card_number) == 8

def test_top_up_mrt_card(mrt_card):
    assert mrt_card.money == 50
    top_up_mrt_card(mrt_card, 500)
    assert mrt_card.money == 500 + 50

    # negative case
    with pytest.raises(Exception):
        top_up_mrt_card(mrt_card, -100)
    # less than 100 baht
    with pytest.raises(Exception):
        top_up_mrt_card(mrt_card, 50)

def test_calculate_station_number():
    assert calculate_station_number(33, 38) == 5
    assert calculate_station_number(33, 4) == 4
    assert calculate_station_number(4, 30) == 6
    assert calculate_station_number(10, 25) == 15
    assert calculate_station_number(28, 1) == 5

    # out of avilable station number
    with pytest.raises(ValueError):
        calculate_station_number(-5, 10)
    with pytest.raises(ValueError):
        calculate_station_number(0, 10)
    with pytest.raises(ValueError):
        calculate_station_number(1, 100)

def test_calculate_fare_by_normal_rate():
    assert calculate_fare_by_normal_rate(33, 38) == 26
    assert calculate_fare_by_normal_rate(33, 4) == 24
    assert calculate_fare_by_normal_rate(4, 30) == 29
    assert calculate_fare_by_normal_rate(10, 25) == 43
    assert calculate_fare_by_normal_rate(28, 1) == 26

def test_final_fare_after_discount_by_age(mrt_card, senior_mrt_card, student_mrt_card):
    fare = calculate_fare_by_normal_rate(33, 38) 
    assert final_fare_after_discount_by_age(senior_mrt_card, fare) == round(0.5 * fare)
    assert final_fare_after_discount_by_age(student_mrt_card, fare)  == round(0.9 * 26) 
    assert final_fare_after_discount_by_age(mrt_card, fare) == fare

def test_process_payment(mrt_card):
    assert mrt_card.money == 50
    process_payment(mrt_card, 20)
    assert mrt_card.money == 30 # 50 - 20 

    # case money in card < fare
    with pytest.raises(ValueError):
        process_payment(mrt_card, 40)
