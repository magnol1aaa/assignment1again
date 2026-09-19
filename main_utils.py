""" 
This module contains the core parts of the main script to keep it readable.
In particular it contains the utility functions and classes such as:

- Opening and handling the json files: open_json(), save_to_json().
- Verifying and converting user input: get_input().
- The class that defines the structure of the user data: UsageDetails.
"""
import json
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


def check_database(data, database):
    """Check if a file exists, and if theres JSON data inside.

    Args:
        file_name (string): Name of the file to check.

    Returns:
        list: List contains success/error message, count of dicts in the file.
    """
    if isinstance(data, UsageDetails):
            database = sqlite3.connect(database)
            cursor = database.cursor()
            first_name = data.first_name
            last_name = data.last_name
            email_address = data.email_address
            
            query = """
            SELECT id 
            FROM user_info 
            WHERE first_name = ? 
            AND last_name = ? 
            AND email_address = ?
            """
            #print(first_name, last_name, email_address)
            
            cursor.execute(query, (first_name, last_name, email_address))
            results = cursor.fetchone()
            database.close()
            return results

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
    

def save_data(data, database, exists):
    database = sqlite3.connect(database)
    cursor = database.cursor()
    to_save = []
    if not exists:
        if isinstance(data, UsageDetails):
            for item in vars(data):
                list.append(to_save, item[0])
            print(to_save)