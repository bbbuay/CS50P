import re
import uuid
from enum import Enum

from rich.console import Console
from rich.table import Table
import sys
from termcolor import colored
from dataclasses import dataclass

def main(): 
    header()
    command_number = get_user_command()
    is_continue = True

    while is_continue:
        function_name = get_command_name(command_number)
        function_name()
        command_number = next_command()

COMMAND_NAMES = ["Create New Person", "Show All Person", "Show All Cards", 
                 "Create MRT Card", "Top Up Money", "Process Payment", "MRT Calculator"]
COMMAND_NUMBERS = [str(i) for i in range(1,len(COMMAND_NAMES)+1)]

@dataclass
class MRTStation:
    name: str
    code: str
    number: int

# key: display station number, value is station name
MRT_STATIONS = {
    38: "Lak Song",
    37: "Bang Khae",
    36: "Phasi Charoen",
    35: "Phetkasem 48",
    34: "Bang Wa",
    33: "Bang Phai",
    1: "Tha Phra",
    2: "Fai Chai",
    3: "Charun Sanitwong Railway Station",
    4: "Bang Khun Non",
    5: "Bang Yi Khan",
    6: "Sirindhorn",
    7: "Bang Phlat",
    8: "Bang O",
    9: "Bang Pho",
    10: "Tao Poon",
    11: "Bang Sue",
    12: "Kamphaeng Phet",
    13: "Chatuchak Park",
    14: "Phahon Yothin",
    15: "Lat Phrao",
    16: "Ratchadaphisek",
    17: "Sutthisan",
    18: "Huai Khwang",
    19: "Thailand Cultural Centre",
    20: "Phra Ram 9",
    21: "Phetchaburi",
    22: "Sukhumvit",
    23: "Queen Sirikit National Convention Centre",
    24: "Klong Toei",
    25: "Lumphini",
    26: "Silom",
    27: "Sam Yan",
    28: "Hua Lamphong",
    29: "Wat Mangkon",
    30: "Sam Yot",
    31: "Sanam Chai", 
    32: "Itsarahap",
}

# key is station number, value is fare
MRT_RATE = {
    0: 17,
    1: 17, 
    2: 19,
    3: 21,
    4: 24,
    5: 26,
    6: 29,
    7: 31,
    8: 33,
    9: 36,
    10: 38,
    11: 41,
    12: 43,
}

# create dict where key is mrt station code and value is mrt station obj 
MRT_STATIONS_OBJ = {}
station_codes = []
for number, name in MRT_STATIONS.items():
    code = name.replace(" ", "-").lower()
    obj =  MRTStation(name, code, number)
    MRT_STATIONS_OBJ[code] = obj

    # append station code 
    station_codes.append(code)

class Person:

    instances = []

    def __init__(self, first_name: str, last_name: str, age: int):
        self._national_id = self._generate_national_id()
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        Person.instances.append(self)

    def __str__(self):
        return f"{self.national_id}: {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    # Getter for national_id
    @property
    def national_id(self):
        return self._national_id

    def _generate_national_id(self):
        return (str(uuid.uuid4().int))[:13]


    # Getter for first_name
    @property
    def first_name(self):
        return self._first_name

    # Setter for first_name
    @first_name.setter
    def first_name(self, first_name):
        name_pattern = r"^[a-zA-Z]+$"
        if not re.search(name_pattern, first_name.strip()):
            raise ValueError("Invalid first name.")
        self._first_name = first_name

    # Getter for last_name
    @property
    def last_name(self):
        return self._last_name

    # Setter for last_name
    @last_name.setter
    def last_name(self, last_name):
        name_pattern = r"^[a-zA-Z]+$"
        if not re.search(name_pattern, last_name.strip()):
            raise ValueError("Invalid last name.")
        self._last_name = last_name

    # Getter for age
    @property
    def age(self):
        return self._age

    # Setter for age
    @age.setter
    def age(self, age):
        if age <= 0 or age > 122:
            raise ValueError(f"Invalid Age for {age} year. Age suppose to be between 1 to 122.")
        self._age = age
    

class MRTCardType(Enum):
    STUDENT = 'student'
    ADULT = 'adult'
    SENIOR = 'senior'

class MRTCard:

    instances = []

    def __init__(self, owner: Person, money: int = 50):
        self.card_number = (str(uuid.uuid4().int))[:8]
        self.owner = owner
        self.money = money
        self.card_type = self.calculate_card_type(owner.age)
        MRTCard.instances.append(self)

    def __str__(self):
        return f"MRT card {self.card_number}."

    def calculate_card_type(self, age: int) -> MRTCardType:
        if age <= 23:
            return MRTCardType.STUDENT
        elif age < 60:
            return MRTCardType.ADULT
        else:
            return MRTCardType.SENIOR


# command table 

def header() -> None:
    print(colored("Hello World ! Welcome to MRT Assitance !", attrs=["bold", "underline"]))

def get_user_command() -> str:
    command_table()
    print("Press", colored("'q'", "red", attrs=["bold", "blink"]) ,"for exit the program")
    command_number = input("Enter the command number you want to do: ").strip().lower()

    if command_number == 'q':
        print(colored("Exit the program", "red", attrs=["bold"]))
        sys.exit()

    if command_number not in COMMAND_NUMBERS:
        print(colored(f"There is no command number: {command_number}", "red", attrs=["bold"]))
        command_number = next_command()
    
    return command_number

def next_command() -> str:
    print("\nDo you want to continue use this more ?")
    print("If you want to see command table, Press", colored("'t'", "green", attrs=["bold"]))
    print("Press", colored("'q'", "red", attrs=["bold", "blink"]) ,"for exit the program")
    user_input = input("Enter the command number: ").strip().lower()

    if user_input == "t":
        command_table()
        user_input = next_command()

    if user_input == "q":
        print(colored("Exit the program", "red", attrs=["bold"]))
        sys.exit()

    if user_input not in COMMAND_NUMBERS:
        print(colored(f"There is no command number: {user_input}", "red", attrs=["bold"]))
        user_input = next_command()
    
    return user_input
        
def command_table() -> None:
    table = Table(title="Table of Avilable Commands")

    columns = ["Number", "Command Title"]
    rows = []
    for number, command in zip(COMMAND_NUMBERS, COMMAND_NAMES):
        rows.append([number, command])

    for column in columns:
        table.add_column(column)

    for row in rows:
        table.add_row(*row)

    console = Console()
    console.print(table)

def command_mrt_station_and_number_table() -> None:
    table = Table(title="Table of Avilable Commands")

    columns = ["Station Number", "MRT Station Name"]
    rows = []
    for number, mrt_station_name in MRT_STATIONS.items():
        rows.append([str(number), mrt_station_name])

    for column in columns:
        table.add_column(column)

    for row in rows:
        table.add_row(*row)

    console = Console()
    console.print(table)


# all commands 
def create_person_person_command() -> str | Person:
    try:
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        age = int(input("Enter Age: ").strip())
        person = create_new_person(first_name, last_name, age)
    except Exception as error:
        print(colored(error, color="red", attrs=["bold"]))
        return ""

    else:
        print(colored("Successfully created new person.", color="green", attrs=["bold"]))
        return person
    
def show_all_persons_command() -> None:
    
    persons = Person.instances

    if len(persons) == 0:
        print(colored("There is no person in the system yet.", "red", attrs=["bold"]))

    else:
        table = Table(title="All People")
        columns = ["Number", "National ID", "Full Name", "Age(years)"]

        rows = []

        for person, number in zip(persons, range(len(persons))):
            rows.append([str(number+1), person.national_id, person.full_name, str(person.age)])

        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*row)

        console = Console()
        console.print(table)

def show_all_cards_command() -> None:
    mrt_cards = MRTCard.instances

    if len(mrt_cards) == 0:
        print(colored("There is no mrt card in the system yet.", "red", attrs=["bold"]))

    else:
        table = Table(title="All Cards")
        columns = ["Number", "Card number", "Owner", "Age", "Card type", "Money(baht)"]

        rows = []
        for card, number in zip(mrt_cards, range(len(mrt_cards))):
            rows.append([str(number+1), card.card_number, card.owner.full_name, str(card.owner.age), card.card_type.value, str(card.money)])


        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*row)

        console = Console()
        console.print(table)

def create_mrt_card_command() -> None:
    try:
        person_id = input("Nation ID of card's owner: ").strip()
        person = get_person(person_id)
        if person is None:
            print(colored(f"There is no person with national id: {person_id}", "red", attrs=["bold"]))
            return ""
        
        card = create_mrt_card(person)

    except Exception as err:
        print(colored(err, "red", attrs=["bold"]))
    else:
        print(colored(f"Successfully created MRT card: {card.card_number}.", color="green", attrs=["bold"]))

def top_up_mrt_card_command() -> str | None:
    try:
        card_number  = input("Card Number: ").strip()
        money = input("Money(baht): ").strip()

        if not is_number(money):
            print(colored("The money value should be integer.", "red", attrs=["bold"]))
            return ""

        money = int(money)
        mrt_card = get_mrt_card(card_number)

        if mrt_card is None:
            print(colored(f"There is no card: {card_number}", "red", attrs=["bold"]))
            return ""
        
        top_up_mrt_card(mrt_card, money)

    except Exception as err:
        print(colored(err, "red", attrs=["bold"]))
        return ""
    
    else:
        print(colored(f"Successfully added money to card {mrt_card.card_number}.", color="green", attrs=["bold"]))
        print(colored(f"Current money in the card is {mrt_card.money} baht.", color="green", attrs=["bold"]))

def process_payment_command() -> str | None:
    command_mrt_station_and_number_table()
    card_number  = input("Card Number: ").strip()
    start_station = input("Start Station Name/Number: ").strip()
    destination_station = input("Destination Station Name/Number: ").strip()

    try:
        start_number = convert_to_station_number(start_station)
        dest_number = convert_to_station_number(destination_station)
        mrt_card = get_mrt_card(card_number)
        fare = calculate_fare_by_normal_rate(start_number, dest_number)
        fare = final_fare_after_discount_by_age(mrt_card, fare)

        if mrt_card is None:
            raise ValueError(f"There is no card with card number: {card_number}")
        
        # if not validate_station_number(start_number):
        #     raise ValueError(f"There is no station number: {start_number}") 
        
        # if not validate_station_number(dest_number):
        #     raise ValueError(f"There is no station number: {dest_number}") 

        process_payment(mrt_card, fare)

    except Exception as err:
        print(colored(f"{err}", "red", attrs=["bold"]))
        return ""
    
    else:
        print(colored(f"Sucessfully paid {fare} baht", "green", attrs=["bold"]))
        print(colored(f"Current Money left: {mrt_card.money} baht", "blue", attrs=["bold"]))

def mrt_calculator_command() -> None:
    print(colored("\nCheck Fare Rate", "blue", attrs=["bold"]))
    command_mrt_station_and_number_table()
    start_station = input("Start Station Name/Number: ").strip()
    destination_station = input("Destination Station Name/Number: ").strip()

    try:
        start_number = convert_to_station_number(start_station)
        dest_number = convert_to_station_number(destination_station)
        fare = calculate_fare_by_normal_rate(start_number, dest_number)

    except Exception as err:
        print(colored(err, "red", attrs=["bold"]))

    else:
        print(colored(f"Fare: {MRT_STATIONS[start_number]} to {MRT_STATIONS[dest_number]} is {fare} baht.", "green", attrs=["bold"]))


# all helper function
def get_person(person_id: str) -> Person | None:
    for person in Person.instances:
        if person.national_id == person_id:
            return person
    return None 

def get_mrt_card(card_number: str) -> MRTCard | None:
    for card in MRTCard.instances:
        if card.card_number == card_number:
            return card
    return None

def is_number(user_input: str) -> bool:
    if re.search("^(\d)+$", user_input):
        return True
    return False

def validate_station_number(station_number: int) -> bool:
    if 1 <= station_number <= 38:
        return True
    return False

def convert_to_station_number(station: str) -> int:
    start_code = station.lower().replace(" ", "-")

    if start_code in station_codes:
        station_number = MRT_STATIONS_OBJ[start_code].number
    elif is_number(station):
        station_number = int(station)
    else:
        raise ValueError(f"There is no station number/name: {station}")
    
    if validate_station_number(station_number):
        return station_number
    raise ValueError(f"There is no station number/name: {station}")


# all main functions 
def create_new_person(first_name: str, last_name: str, age: int) -> Person:
    try:
        person = Person(first_name, last_name, age)
        return person

    except Exception as err:
        raise(err)

def create_mrt_card(person: Person) -> MRTCard:
    return MRTCard(owner=person)

def top_up_mrt_card(mrt_card: MRTCard, money: int) -> MRTCard:
    if money < 0:
        raise Exception("The input money suppose to be positive.")
    
    if money < 100:
        raise Exception("Minimum money value for adding to the card is 100 baht.")

    mrt_card.money = mrt_card.money + money
    return mrt_card

def calculate_station_number(start_station_number: int, destination_station_number: int) -> int:
    if not validate_station_number(start_station_number):
        raise ValueError(f"There is no station number: {start_station_number}.")

    if not validate_station_number(destination_station_number):
        raise ValueError(f"There is no station number: {destination_station_number}.")
    
    # case 1 : both are out of loop 
    if (33 <= start_station_number <= 38) and (33 <= destination_station_number <= 38):
        return abs(destination_station_number - start_station_number)
    
    # case 2 : both are in loop
    if (1 <= start_station_number <= 32) and (1 <= destination_station_number <= 32):
        min_station_number = min(start_station_number, destination_station_number)
        max_station_number = max(start_station_number, destination_station_number)
        possible_station_num_1 = max_station_number - min_station_number
        possible_station_num_2 = min_station_number + (32 - max_station_number)
        
        if possible_station_num_1 > possible_station_num_2:
            return possible_station_num_2
        return possible_station_num_1
    
    # case 3: 1 is out loop and 1 is in loop
    if ((1 <= start_station_number <= 32) and (33 <= destination_station_number <= 38)) or ((33 <= start_station_number <= 38) and (1 <= destination_station_number <= 32)):
        # calculate number of station out loop 
        min_station_number = min(start_station_number, destination_station_number)
        max_station_number = max(start_station_number, destination_station_number)
        out_station_number = max_station_number  - 33

        # calculate number of station in loop 
        poss_station_num_1 = min_station_number 
        poss_station_num_2 = 32 - min_station_number + 2

        if poss_station_num_1 > poss_station_num_2:
            return out_station_number + poss_station_num_2
        return out_station_number + poss_station_num_1
 
def calculate_fare_by_normal_rate(start_station_number: int, destination_station_number: int) -> int:
    # calculate station number 
    num_station = calculate_station_number(start_station_number, destination_station_number)

    max_station_number = max(MRT_RATE.keys())

    # if the number of station is greater than max number of station to calculate fare
    # return max fare
    if num_station > max_station_number:
        return MRT_RATE[max_station_number]
    
    return MRT_RATE[num_station]

def final_fare_after_discount_by_age(mrt_card: MRTCard, fare: int) -> int:
    match mrt_card.card_type:
        # get 10% discount
        case MRTCardType.STUDENT:
            return round(0.9*fare)
        # no discount
        case MRTCardType.ADULT:
            return fare
        # get 50% discount
        case MRTCardType.SENIOR:
            return round(0.5*fare)
        case _:
            raise ValueError(f"There is no mrt card type: {mrt_card.card_type}")

def process_payment(mrt_card: MRTCard, fare: int) -> MRTCard:

    if mrt_card.money < fare:
        raise ValueError(f"You don't have enough money({mrt_card.money} baht) to pay for fare({fare} baht).")
    mrt_card.money = mrt_card.money - fare
    return mrt_card

COMMANDS = {
    "1": create_person_person_command,
    "2": show_all_persons_command, 
    "3": show_all_cards_command,
    "4": create_mrt_card_command,
    "5": top_up_mrt_card_command,
    "6": process_payment_command,
    "7": mrt_calculator_command,
}

def get_command_name(command_number: str) -> str:
    command_number_list = list(COMMANDS.keys())
    if command_number not in command_number_list:
        raise ValueError(f"There is no this command number: {command_number}")
    
    return COMMANDS[command_number]
    
if __name__ == "__main__":
    main()