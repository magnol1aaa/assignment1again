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

    matches_names = user_name_match(data, id)
    if is_user and matches_names == 1:
        does_exist = execute_query(
            "SELECT id FROM user_data WHERE id = ?", [id], True, False
        )
        if does_exist:
            return "User has data"
        else:
            return "User has no data"
    elif is_user and matches_names == -1:
        return "Wrong name"
    elif not is_user and matches_names == -1:
        if create:
            execute_query(
                """INSERT INTO user_info
                (first_name,last_name, email_address)
                VALUES (?, ?, ?);
                """,
                [first_name, last_name, email_address],
                False,
                True,
            )
            return "New user"
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
    execute_query(user_info_query, None, False, True)
    execute_query(user_data_query, None, False, True)


def save_data(data, exists):
    if not exists:
        user_id = get_id(data)
        query = """
        INSERT INTO user_data
        (id, call_minutes, data_gigabytes,
        needs_roaming) VALUES (?, ?, ?, ?)
        """
        query_data = [
            user_id,
            data.call_time,
            data.data_used,
            data.roaming_bool,
        ]
        execute_query(query, query_data, False, True)
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
        execute_query(query, query_data, False, True)
    else:
        print("unknown parameters.")


def get_id(data) -> int:

    email_address = data.email_address
    query = "SELECT id FROM user_info WHERE email_address = ?"
    query_data = [email_address]
    id = execute_query(query, query_data, True, False)

    if id:
        return id[0]
    else:
        return -1


def user_name_match(data, id) -> int:
    first_name = data.first_name
    last_name = data.last_name
    email_address = data.email_address

    query = """
    SELECT id FROM user_info WHERE first_name = ? AND 
    last_name = ? AND email_address = ?
    """
    query_data = [first_name, last_name, email_address]

    results = execute_query(query, query_data, True, False)
    if results is not None:
        if results[0] == id:
            return 1
        else:
            return -1
    else:
        return -1


def execute_query(query, data, need_return, commit):
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    if not data:
        cursor.execute(query)
    elif data:
        cursor.execute(query, data)
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
            return result[0]
    elif not need_return:
        if commit:
            database.commit()
            database.close()
            return
    print("No path followed.")
    database.close()
    return


def input_user_info() -> UsageDetails:
    first_name = input_name("What is your first name? " "Enter first name: ")

    last_name = input_name("What is your last name? " "Enter last name: ")

    email_address = input_email(
        "What is your email address? " "Enter email address:"
    )
    user = UsageDetails(first_name, last_name, email_address, 0, 0, False)
    return user


def get_user_data(data):
    id = get_id(data)
    query = """
    SELECT * from user_data WHERE id = ?
    """
    query_data = [id]
    return execute_query(query, query_data, True, False)


def get_plan_stats() -> dict:
    with open(plan_file_name) as f:
        data = json.load(f)
        return data


def calculate_costs(data, plans) -> list:
    # id | call min | data use | roaming
    # monthly cost = Base Cost + (Extra Minutes x Cost Per Minute) + (Extra Data x Cost per GB)
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
