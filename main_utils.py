""" 
This module contains the core parts of the main script to keep it readable.
In particular it contains the utility functions and classes such as:

- Opening and handling the json files: open_json(), save_to_json().
- Verifying and converting user input: get_input().
- The class that defines the structure of the user data: UsageDetails.
"""
import sqlite3
import re

class UsageDetails:
    """Class that allows for easy structuring of userdata"""
    def __init__(self, first_name, last_name, 
                 email_address, call_time, 
                 data_used, roaming_bool
                 ):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.call_time = call_time
        self.data_used = data_used
        self.roaming_bool = roaming_bool
        
    def __str__(self):
        return(
            f"Full Name: {self.first_name} {self.last_name}"
            f"User Email: {self.email_address}"
            f"Call Time: {self.call_time} "
            f"Data Used: {self.data_used} "
            f"Roaming Needed: {self.roaming_bool}"
        )


def user_exists(data, database_name) -> str:
    """Check if a file exists, and if theres JSON data inside.

    Args:
        file_name (string): Name of the file to check.

    Returns:
        list: List contains success/error message, count of dicts in the file.
    """

    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    cursor.execute("SELECT id FROM user_info WHERE email_address = ?", [data[2]])
    is_user = cursor.fetchone()
    id = is_user[0]
    cursor.execute("""SELECT id FROM user_info WHERE first_name = ? AND last_name = ? AND email_address = ?""", data)
    matches_names = cursor.fetchone()
    if is_user and matches_names:
        print("Match voth")
    if is_user and not matches_names:
        return "Wrong name"
    if not is_user and not matches_names:
        return "No user"
    
    print(matches_names)
    print(is_user)
    if id:
        database = sqlite3.connect(database_name)
        cursor = database.cursor()
        cursor.execute("SELECT id FROM user_data WHERE id = ?", [id])
        does_exist = cursor.fetchone()
        print(does_exist)
        if does_exist[0] == id:
            print("user matches and has data already")
            return "User has data"
        

def input_int(message) -> int:
    """Converts input into an integer, repeats if input is incorrect.

    Args:
        message (string): Message to display for input.

    Returns:
        int: Returns users input as an integer.
    """
    
    input_valid = None
    while not input_valid:
        user_input = input(message)
        if user_input.isdigit():
            input_valid = True
            break
        else:
            print(f"{user_input} is not a number.") 
    return int(user_input)


def input_email(message):
    input_valid = None
    while not input_valid:
        email = input(message)
        if re.match("[^@]+@[^@]+\\.[^@]+", email):
            input_valid = True
            break
        else:
            print(f"{email} is not a valid email address.")
            
    return email

def input_bool(message) -> bool:
    """Converts yes/no input to a bool, repeats if input is incorrect.

    Args:
        message (string): Message to display for input.

    Returns:
        bool: The input returned as a bool.
    """
    approve = ['y', 'yes'] 
    deny = ['n', 'no'] 
    
    input_valid = None
    while not input_valid:
        user_input = input(message)
        if user_input.lower() in approve:
            input_valid = True
            input_type = True
        elif user_input.lower() in deny:
            input_valid = True
            input_type = False
        else:
            print(f"{user_input} isn't a valid option.")
    return input_type
    


def input_name(message) -> str:
    input_valid = None
    while not input_valid:
        user_input = input(message)
        if user_input.isalpha():
            input_valid = True
    return user_input
    
    
def init_database(database_name):
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user_info "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "first_name TEXT NOT NULL, "
                "last_name TEXT NOT NULL, "
                "email_address VARCHAR NOT NULL UNIQUE)"
                    )

    cursor.execute("CREATE TABLE IF NOT EXISTS user_data "
                "(id INTEGER REFERENCES user_info(id), "
                "call_minutes INTEGER NOT NULL, "
                "data_gigabytes INTEGER NOT NULL, "
                "needs_roaming INTEGER NOT NULL)"
                )
    database.commit()
    database.close()
    
    
def save_data(data, database, exists):
    database = sqlite3.connect(database)
    cursor = database.cursor()
    to_save = []
    if not exists:
        if isinstance(data, UsageDetails):
            variables = vars(data)
            for key, value in variables.items():
                to_save.append(value)
            cursor.execute("""INSERT INTO user_info
                           (first_name,last_name, email_address)
                           VALUES (?, ?, ?);
                           """, 
                           (data.first_name, data.last_name, 
                            data.email_address))
            cursor.execute("""SELECT id FROM user_info WHERE
                           email_address = ?""", [data.email_address])
            user_id = cursor.fetchone()
            print(user_id)
            cursor.execute("""INSERT INTO user_data
                           (id, call_minutes, data_gigabytes, 
                           needs_roaming) VALUES
                           (?, ?, ?, ?)
                           """, 
                           (user_id[0], data.call_time, 
                            data.data_used,
                            data.roaming_bool
                            )
                           )
            cursor.execute("SELECT * FROM user_info WHERE email_address = ?", [data.email_address])
            print(cursor.fetchone())
            cursor.execute("SELECT * FROM user_data WHERE id = ?", [user_id[0]])
            print(cursor.fetchone())
            database.commit()
            database.close()