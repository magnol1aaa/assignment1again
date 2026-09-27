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

# Configuration
database_name = "plandata"
plan_file_name = "plan_stats.json"


class UsageDetails:
    """Class that allows for easy structuring of userdata"""

    def __init__(
        self,
        first_name,
        last_name,
        email_address,
        call_time,
        data_used,
        roaming_bool,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.call_time = call_time
        self.data_used = data_used
        self.roaming_bool = roaming_bool

    def __str__(self):
        return (
            f"Full Name: {self.first_name} {self.last_name}"
            f"User Email: {self.email_address}"
            f"Call Time: {self.call_time} "
            f"Data Used: {self.data_used} "
            f"Roaming Needed: {self.roaming_bool}"
        )


def user_exists(data, create) -> str:
    """Check if a file exists, and if theres JSON data inside.

    Args:
        file_name (string): Name of the file to check.

    Returns:
        list: List contains success/error message, count of dicts in the file.
    """

    email_address = data.email_address
    first_name = data.first_name
    last_name = data.last_name

    id = get_id(data)
    is_user = True if id != -1 else False

    # Check if names match the email provided.
    matches_names = user_name_match(data, id)
    
    # If they are a user and their names match the email.
    if is_user and matches_names == 1:
        query = "SELECT id FROM user_data WHERE id = ?"
        query_data = [id]
        does_exist = execute_query(query, True, query_data, False)
        
        if does_exist:
            return "User has data"
        else:
            return "User has no data"
    # If they are a user but they entered non-matching names.
    elif is_user and matches_names == -1:
        return "Wrong name"
    # If they aren't a user.
    elif not is_user:
        # Checks if the function was called to create an account.
        if create:
            query = """
            INSERT INTO user_info
            (first_name,last_name, email_address)
            VALUES (?, ?, ?);
            """
            query_data = [first_name, last_name, email_address]
            execute_query(query, False, query_data, True)
            return "New user"
        # If an account doesn't need to be made, return no user.
        else:
            return "No user"
    else:
        return "Error"


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


def input_email(message) -> str:
    """Ensure user inputs email address, if incorrect it repeats.

    Args:
        message (string): Message to display for input.

    Returns:
        str: Returns email address.
    """
    input_valid = None
    while not input_valid:
        email = input(message).lower()
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
    approve = ["y", "yes"]
    deny = ["n", "no"]

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
    """Gets user input and ensures it only contains letters.

    Args:
        message (string): Message to display for input.

    Returns:
        str: Returns the users input as a string.
    """
    input_valid = None
    while not input_valid:
        user_input = input(message).lower()
        if user_input.isalpha():
            input_valid = True
        else:
            print(
                f"{user_input} is not a valid name, "
                "remove any numbers or special characters."
            )
    return user_input


def init_database():
    """Creates the database tables if they do not exist."""
    
    user_info_query = """
    CREATE TABLE IF NOT EXISTS user_info 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL, 
    email_address VARCHAR NOT NULL UNIQUE)
    """
    
    user_data_query = """
    CREATE TABLE IF NOT EXISTS user_data 
    (id INTEGER REFERENCES user_info(id), 
    call_minutes INTEGER NOT NULL, 
    data_gigabytes INTEGER NOT NULL, 
    needs_roaming INTEGER NOT NULL)
    """
    
    execute_query(user_info_query, False, [], True)
    execute_query(user_data_query, False, [], True)


def save_data(data, exists):
    """This function is responsible for saving data to the sqlite database.

    Args:
        data (class): Takes an instance of UsageDetails, which has user info.
        exists (bool): This tells the function if data already exists or not.

    """
    
    if not exists:
        user_id = get_id(data)
        # Query to execute.
        query = """
        INSERT INTO user_data
        (id, call_minutes, data_gigabytes,
        needs_roaming) VALUES (?, ?, ?, ?)
        """
        
        # Defining data to pass to the query.
        query_data = [
            user_id,
            data.call_time,
            data.data_used,
            data.roaming_bool,
        ]
        # Execute the query, False means no return details needed.
        # True means that we need the changes committed to the database.
        execute_query(query, False, query_data, True)
        
    elif exists:
        user_id = get_id(data)

        query = """
        UPDATE user_data SET call_minutes = ?, 
        data_gigabytes = ?, needs_roaming = ? WHERE
        id = ?
        """

        query_data = [
            data.call_time,
            data.data_used,
            data.roaming_bool,
            user_id,
        ]
        execute_query(query, False, query_data, True)
        
    else:
        print("Unknown parameters, check save function args.")


def get_id(data) -> int:
    """This function returns the provided email addresses user ID.

    Args:
        data (class): Takes an instance of UsageDetails, containing user info.

    Returns:
        int: Returns user ID, or -1 if the ID cannot be found.
    """
    
    email_address = data.email_address
    
    query = "SELECT id FROM user_info WHERE email_address = ?"
    query_data = [email_address]
    # Executes the query, True means it requires a return value.
    # False means that it doesn't need to commit database changes.
    id = execute_query(query, True, query_data, False)

    if id:
        return id[0]
    else:
        return -1


def user_name_match(data, id) -> int:
    """This function checks whether the users name matches the provided email.

    Args:
        data (class): Takes an instance of UsageDetails, containing user info.
        id (int): Takes the user ID for comparison.

    Returns:
        int: Returns user id if the names match, or -1 if they do not.
    """
    
    first_name = data.first_name
    last_name = data.last_name
    email_address = data.email_address

    query = """
    SELECT id FROM user_info WHERE first_name = ? AND 
    last_name = ? AND email_address = ?
    """
    
    query_data = [first_name, last_name, email_address]

    results = execute_query(query, True, query_data, False)
    if results is not None:
        if results[0] == id:
            return 1
        else:
            return -1
    else:
        return -1


def execute_query(query, need_return=False, data=[], commit=False):
    """Executes supplied queries and returns or commits changes if required.

    Args:
        query (string): The string containing the query.
        need_return (bool): Whether data must be returned, default false.
        data (dict): The data of the query, can be empty.
        commit (bool): If data changes need to be committed, default false.

    Returns:
        result: If need_return is true it returns the results.
    """
    # Connect to the database
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    
    if not data:
        cursor.execute(query)
    elif data:
        cursor.execute(query, data)
    
    # If user needs return or not, and whether to commit.
    if need_return:
        result = cursor.fetchall()
        if not result:
            if commit:
                database.rollback()
                database.close()
            return
        if result:
            if commit:
                database.commit()
                database.close()
            if len(result) <= 1:
                return result[0]
            else:
                return result
    elif not need_return:
        if commit:
            database.commit()
            database.close()
            return 


def input_user_info() -> UsageDetails:
    """Gets user name and email address, returns as UsageDetails instance.

    Returns:
        UsageDetails: Class containing only the users name and email.
    """
    first_name = input_name("What is your first name? Enter first name: ")

    last_name = input_name("What is your last name? Enter last name: ")

    email_address = input_email(
        "What is your email address? " "Enter email address: "
    )
    # Plan info is left empty, they're not saved until user enters usage data.
    user = UsageDetails(first_name, last_name, email_address, 0, 0, False)
    return user


def get_user_data(data):
    """Gets user data from their ID.
    Args:
        data (class): Requires user's UsageDetails instance to get their ID.
    Returns:
        tuple: Returns users data as as tuple.
    """
    id = get_id(data)
    
    query = """
    SELECT * from user_data WHERE id = ?
    """
    query_data = [id]

    to_return = execute_query(query, True, query_data, False)
    return to_return


def get_plan_stats() -> list:
    """Retrieves the details from the json file containing all the plans.

    Returns:
        list: List containing every available plan.
    """
    with open(plan_file_name) as f:
        data = json.load(f)
        return data


def calculate_costs(data, plans) -> list:
    """Returns the cost for each supplied plan based on user data.

    Args:
        data (list, tuple): Receives a tuple of data returned from a query.
        plans (list, tuple): Receives a tuple of plans from a function.

    Returns:
        list: List of valid plans and their costs.
    """
    call_time = data[1]
    data_used = data[2]
    plan_costs = []

    for plan in plans:
        if data_used > plan["included_data_gb"]:
            extra_data = data_used - plan["included_data_gb"]
        else:
            extra_data = 0
        if plan["included_minutes"] == "Unlimited":
            extra_minutes = 0
        else:
            if call_time > plan["included_minutes"]:
                extra_minutes = plan["included_minutes"] - call_time
            else:
                extra_minutes = 0

        monthly_cost = (
            plan["base_cost_aud"]
            + (extra_minutes * plan["cost_per_excess_minute_aud"])
            + (extra_data * plan["cost_per_excess_gb_aud"])
        )
        plan_costs.append(
            {
                "plan_name": plan["plan_name"],
                "monthly_cost": round(monthly_cost, 2),
                "roaming": plan["roaming"],
            }
        )
        
    return plan_costs


def fun_statistics(data) -> str:
    query = """
    SELECT call_minutes, data_gigabytes, needs_roaming FROM user_data
    """
    all_data = execute_query(query, True)
    
    if len(all_data) <= 1:
        return "You're the only user, stats will show when there's more users."
    
    call_usage = 0
    data_usage = 0
    plan_count = 0
    roaming_percent = 0
    roaming_needs = []
    
    for item in all_data:
        call_usage += int(item[0])
        data_usage += (item[1])
        roaming_needs.append(item[2])
        plan_count += 1
    
    # User usages:
    user_call = data[1]
    user_data = data[2]
    
    # Calculate mean usages.
    call_usage = call_usage / plan_count
    data_usage = data_usage / plan_count
    
    # Store if above or below average.
    above_call = False
    above_data = False
    
    # Calculate how many people need roaming.
    roaming_percent = round((roaming_needs.count(True) / plan_count) * 100)
    
    # Compare user data to mean usage and generate a rounded percentage.
    if user_call <= call_usage:
        compare_call = round((user_call / call_usage) * 100)
    else:
        compare_call = round(((user_call - call_usage) / call_usage) * 100)
        above_call = True
    if user_data <= data_usage:
        compare_data = round((user_data / data_usage) * 100)
    else:
        compare_data = round(((user_data - data_usage) / data_usage) * 100)
        above_data = True
    
    # Decide what strings are appropriate to return for each option.
    if above_call:
        call_string = f"You use {compare_call}% more minutes than average!"
    else:
        call_string = f"You use {compare_call}% less minutes than average!"
    if above_data:
        data_string = f"You use {compare_data}% more data than average!"
    else:
        data_string = f"You use {compare_data}% less data than average!"
    bool_string = f"{roaming_percent}% of users use roaming!"
    
    return f"{call_string}\n{data_string}\n{bool_string}"