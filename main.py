# Imports

from main_utils import (
    UsageDetails,
    user_exists,
    input_int,
    input_bool,
    save_data,
    init_database,
    input_user_info,
    get_user_data,
)

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
init_database()


def option_one():
    """User inputs usage details, saves to file if requested."""

    user_data = input_user_info()
    data_update = False
    user_status = user_exists(user_data, False)
    match user_status:
        case "Wrong name":
            print("A user already exists with this email.")
            print("Please enter the correct names or use a different email.")
        case "No user":
            create_account = input_bool(
                "Would you like to create an account? Y(es) / N(o)"
                )
            if create_account:
                user_status = user_exists(user_data, True)
                if user_status == "New user":
                    print("Account created.")
                else:
                    print("Failed to create an account.")
                    input("Press any key to return...")
                    menu_function()
                    
        case "User has data":
            print("You already have data.")
            overwrite = input_bool(
                "There is pre-existing data, overwrite it? " "Y(es) / N(o): "
            )
            if overwrite:
                print("Continuing.")
                data_update = True
            else:
                menu_function()

        case "User has no data":
            pass
    
    call_time = input_int(
        "How many call minutes do you typically use a month? "
        "Enter a number: "
    )

    data_use = input_int(
        "How many gigabytes of data do you typically use a month? "
        "Enter a number: "
    )

    roaming_bool = input_bool(
        "Do you need a plan that offers international roaming? "
        "Y(es) / N(o): "
    )

    user_data.call_time = call_time
    user_data.data_used = data_use
    user_data.roaming_bool = roaming_bool

    save_bool = input_bool(
        "Would you like to save these details? " "Y(es) / N(o): "
    )

    if not save_bool:
        menu_function()

    if data_update:
        save_data(user_data, True)
        print("Your data has been saved.")
        input("Press any key to return...")
        menu_function()
    elif not data_update:
        save_data(user_data, False)
        menu_function()


def option_two():
    user_info = input_user_info()
    user_status = user_exists(user_info, False)
    match user_status:
        case "User has data":
            print("Here are your usage details:\n")
            user_data = get_user_data(user_info)
            roaming = ("Yes" if user_data[3] == 1 else "No")
            print(f"Call Minutes: {user_data[1]}")
            print(f"Gigabytes Used: {user_data[2]}")
            print(f"Roaming Required: {roaming}")
            input("\nPress any key to return...")
            menu_function()
            
        case "User has no data":
            print("you have no data, create some now.")
            input("Press any key to return...")
            menu_function()
        case _:
            print("This information does not match an account.")
            input("Press any key to return...")
            menu_function()


def option_three():
    print("Option Three")


def option_four():
    print("Option Four")


def option_five():
    print("Option Five")


def menu_function(option=None):

    option_funcs = [
        option_one,
        option_two,
        option_three,
        option_four,
        option_five,
    ]

    print(menu_string)
    print(
        f"{option} is not a valid option. "
        "Please pick an option from 1 to 5."
        if option
        else ""
    )

    input = input_int("Enter an option from 1-5:")
    if input > 0 and input <= len(option_funcs):
        option_funcs[input - 1]()  # Call function from list
    elif input == 0:
        # Due to the if option logic above, int 0 would return false.
        menu_function("0")
    else:
        menu_function(input)


menu_function()
