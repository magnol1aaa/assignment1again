# Imports
import sqlite3
from main_utils import(
    UsageDetails, check_database, 
    input_int, input_bool, 
    save_data, input_name,
    input_email)

# Vars
menu_string = """
---------
Mobile Data Plan Advisor
Cooper Gerraty 30487791
----------
1. Enter usage details
2. Display current usage
3. Display plan costs
4. Reccomend best plan
5. Exit
----------
"""
# Initialize Database
database_name = "plandata"
database = sqlite3.connect("plandata")
cursor = database.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_info "
               "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "first_name TEXT NOT NULL, "
               "last_name TEXT NOT NULL, "
               "email_address VARCHAR NOT NULL UNIQUE)"
                )

cursor.execute("CREATE TABLE IF NOT EXISTS user_data "
               "(call_minutes INTEGER NOT NULL, "
               "data_gigabytes INTEGER NOT NULL, "
               "needs_roaming INTEGER NOT NULL)"
               )

database.close()


def option_one():
    """User inputs usage details, saves to file if requested."""

    first_name = input_name(
            "What is your first name? " 
            "Enter a number:"
            )

    last_name = input_name(
            "What is your last name? " 
            "Enter a number:"
            )

    email_address = input_email(
            "What is your email address? " 
            "Enter a number:"
            )
    
    call_time = input_int(
            "How many call minutes do you typically use a month? " 
            "Enter a number:"
            )

    data_time = input_int(
        "How many gigabytes of data do you typically use a month? "
        "Enter a number:"
        )
    
    roaming_bool = input_bool(
        "Do you need a plan that offers international roaming? " 
        "Y(es) / N(o):"
        )
    
    data = UsageDetails(first_name, last_name, 
                        email_address, call_time, 
                        data_time, roaming_bool)
    
    save_bool = input_bool(
        "Would you like to save these details?"
        "Y(es) / N(o):"
        )
    
    if not save_bool: menu_function()
    
    data_exists = check_database(data, database_name)
    if data_exists:
        do_replacement = None
        while not do_replacement:
            do_replacement = input_bool(
                "There is pre-existing data, overwrite it?"
                "Y(es) / N(o)"
            )
        if do_replacement:
            save_data(data, database_name, False)
    if not data_exists:
        save_data(data, database_name, False)
            

def option_two():
    print("Option Two")


def option_three():
    print("Option Three")


def option_four():
    print("Option Four")


def option_five():
    print("Option Five")


def menu_function(option=None):
    
    option_funcs = [
        option_one, option_two,
        option_three, option_four,
        option_five
        ]
    
    print(menu_string)
    print(f"{option} is not a valid option. " 
          "Please pick an option from 1 to 5." 
          if option else ""
          )
    
    input = input_int("Enter an option from 1-5:")
    if input > 0 and input <= len(option_funcs):
        option_funcs[input - 1]() # Call function from list
    else:
        if input == 0:
            # Due to the if option logic above, int 0 would return false.
            menu_function('0') 

menu_function()