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
    
    if isinstance(data, UsageDetails):
        email_address = data.email_address
        first_name = data.first_name
        last_name = data.last_name
    elif type(data) == tuple:
        print('istuple')
        print(data)
        #(first_name, last_name, email_address)
        email_address = data[2]
        first_name = data[0]
        last_name = data[1]
        
    database = sqlite3.connect(database_name)
    cursor = database.cursor()

    id = get_id(data, database_name)
    is_user = (True if id != -1 else False)
    
    matches_names = user_name_match(data,)
    print(f"FROM USER EXISTS BEFORE IS USER AND MATCH NAMES {id} {is_user} {matches_names}")
    if is_user and matches_names[0] == id:
        database = sqlite3.connect(database_name)
        cursor = database.cursor()
        cursor.execute("SELECT id FROM user_data WHERE id = ?", [id])
        does_exist = cursor.fetchone()
        print(f"From is user: {does_exist}")
        print(does_exist)
        if does_exist:
            if does_exist == id:
                print("user matches and has data already")
                return "User has data"
        else:
            return "User has no data"
    if is_user and not matches_names:
        return "Wrong name"
    if not is_user and not matches_names:
        cursor.execute("""INSERT INTO user_info
                (first_name,last_name, email_address)
                VALUES (?, ?, ?);
                """, 
                [first_name, last_name, 
                email_address])
        database.commit()
        return "User created"
        

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
    
    
def save_data(data, database_name, exists):
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    to_save = []
    if not exists:
        if isinstance(data, UsageDetails):
            variables = vars(data)
            for key, value in variables.items():
                to_save.append(value)
            user_id = get_id(data, database_name)
            cursor.execute("""INSERT INTO user_data
                           (id, call_minutes, data_gigabytes, 
                           needs_roaming) VALUES
                           (?, ?, ?, ?)
                           """, 
                           (user_id, data.call_time, 
                            data.data_used,
                            data.roaming_bool
                            )
                           )
            cursor.execute("SELECT * FROM user_info WHERE email_address = ?", [data.email_address])
            print(cursor.fetchone())
            cursor.execute("SELECT * FROM user_data WHERE id = ?", [user_id])
            print(cursor.fetchone())
            database.commit()
            database.close()
    elif exists:
        cursor.execute
        cursor.execute("""UPDATE user_info SET call_minutes = ?, 
                       data_gigabytes = ?, needs_roaming = ? WHERE
                       id = ?""", [data.call_time, data.data_used, data.roaming_bool, user_id] )
    else:
        print("Not an instance of the Usage Details class.")
        
        
def get_id(data, database_name) -> int:
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    
    if isinstance(data, UsageDetails):
        email_address = data.email_address        
    elif isinstance(data, tuple):
        email_address = data[2]        
    else:
        print("Incompatible data type.")
        
    cursor.execute("SELECT id FROM user_info WHERE email_address = ?", [email_address])
    id = cursor.fetchone()
    print("Getting ID")
    print(id)
    if id:
        return id[0]
    else:
        return -1

def user_name_match(data, database_name, id):
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    if isinstance(data, UsageDetails):
        first_name = data.first_name
        last_name = data.last_name
        email_address = data.email_address
    elif isinstance(data, tuple):
        email_address = data[2]
        first_name = data[0]
        last_name = data[1]
    else:
        print("Not useful data type from user_name_match")
        return
    cursor.execute("""SELECT id FROM user_info WHERE
                    first_name = ? AND last_name = ? AND
                    email_address = ?""", [first_name, last_name, email_address])
    results = cursor.fetchone()
    if results != None:
        print(f"from user_name_match: {results[0]}")
    
    
            