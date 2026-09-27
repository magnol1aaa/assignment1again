# Imports

from main_utils import (
    user_exists,
    input_int,
    input_bool,
    save_data,
    init_database,
    input_user_info,
    get_user_data,
    get_plan_stats,
    calculate_costs,
    fun_statistics
)

# Vars
welcome_message = "Welcome to the Mobile Data Plan Advisor."
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

# Print welcome string
print(welcome_message)

# Functions
def option_one():
    """Option one: Display usage details"""

    print("Enter usage details: ")

    
    user_data = input_user_info()
    data_update = False
    # Check if user exists
    user_status = user_exists(user_data, False)
    match user_status:
        case "Wrong name":
            # If they input an existing email but not the matching names
            print("A user already exists with this email.")
            print("Please enter the correct names or use a different email.")
            input("Press any key to return...")
            menu_function()

        case "No user":
            create_account = input_bool(
                "Would you like to create an account? Y(es) / N(o)"
            )
            if create_account:
                # User exists func also handles creation.
                # The boolean flag defines whether an account is made or not -
                # If an account is not found.
                user_status = user_exists(user_data, True)
                if user_status == "New user":
                    print("Account created.")
                else:
                    print("Failed to create an account.")
                    input("Press any key to return...")
                    menu_function()
            else:
                input("Press any key to return...")
                menu_function()

        case "User has data":
            # If user exists and has data
            overwrite = input_bool(
                "You already have data saved, overwrite it? " "Y(es) / N(o): "
            )
            if overwrite:
                # Flag that data must be updated, not inserted.
                data_update = True
            else:
                input("Press any key to return...")
                menu_function()

        case "User has no data":
            # If they have no data we just pass and continue with data entry
            pass
    
    # Retrieve plan data
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

    # Update the user_data class with the info
    user_data.call_time = call_time
    user_data.data_used = data_use
    user_data.roaming_bool = roaming_bool

    save_bool = input_bool(
        "Would you like to save these details? " "Y(es) / N(o): "
    )

    if not save_bool:
        menu_function()
    # If the update flag is True, it updates the data instead of inserting.
    if data_update:
        save_data(user_data, True)
        print("Your data has been saved.")
        input("\nPress any key to return...")
        menu_function()
    elif not data_update:
        save_data(user_data, False)
        menu_function()


def option_two():
    """Option two: Display user data"""

    print("Display user data")

    # Get user info and check if user exists
    user_info = input_user_info()
    user_status = user_exists(user_info, False)

    match user_status:
        case "User has data":
            # Print their usage details.
            print("Here are your usage details:\n")
            user_data = get_user_data(user_info)
            roaming = "Yes" if user_data[3] == 1 else "No"
            print(f"Call Minutes: {user_data[1]}")
            print(f"Gigabytes Used: {user_data[2]}")
            print(f"Roaming Required: {roaming}\n")
            print(fun_statistics(user_data))
            input("\nPress any key to return...")
            menu_function()

        case "User has no data":
            print("You have no data saved, enter some in option 1.")
            input("Press any key to return...")
            menu_function()
        case _:
            # This case occurs if the data does not match.
            print("This information does not match an account.")
            input("Press any key to return...")
            menu_function()


def option_three():
    print("Display plan costs:")
    
    user_info = input_user_info()
    user_status = user_exists(user_info, False)
    
    match user_status:
        case "User has no data":
            print("You have no data saved, enter some in option 1.")
            input("Press any key to return...")
            menu_function()
        case "User has data":
            print("\nAvailable plan data:")
            # get_user_data retrieves user data from their info.
            user_data = get_user_data(user_info)
            
            # retrieves the available plans from the json file.
            plan = get_plan_stats()
            
            # calculate costs based on data retrieved from user_data.
            plan_costs = calculate_costs(user_data, plan)
            
            # print each calculated plan cost
            for item in plan_costs:
                name = item["plan_name"]
                cost = item["monthly_cost"]
                print(f"{name}'s monthly cost: {cost}")
            input("\nPress any key to return...")
            menu_function()
        case _:
            print("This information does not match an account.")
            input("Press any key to return...")
            menu_function()


def option_four():
    """Option four: Reccomend best plan"""

    print("Reccomend best plan:")

    user_info = input_user_info()
    user_status = user_exists(user_info, False)
    
    match user_status:
        case "User has no data":
            print("you have no data, create some now.")
            input("Press any key to return...")
            menu_function()

        case "User has data":
            # Get user data, available plans and their costs.
            user_data = get_user_data(user_info)
            plans = get_plan_stats()
            plan_costs = calculate_costs(user_data, plans)
            
            valid_plans = []
            lowest_plan = {}
            
            # Iterate through plans and append applicable plans for the user.
            for item in plan_costs:
                # This checks if the plan supports roaming.
                # Then checks if the user needs roaming.
                if item["roaming"] and user_data[3] == 1:
                    valid_plans.append(item)
                elif user_data[3] == 0:
                    valid_plans.append(item)
                else:
                    pass
                
            # Iterate through applicable plans and find the cheapest one.           
            for item in valid_plans:
                if not lowest_plan:
                    lowest_plan = item
                elif item["monthly_cost"] < lowest_plan["monthly_cost"]:
                    lowest_plan = item
            
            lowest_name = lowest_plan["plan_name"]
            lowest_cost = lowest_plan["monthly_cost"]
            print(f"\nCheapest Plan: {lowest_name}")
            print(f"Monthly Cost: {lowest_cost}")
            
            input("\nPress any key to return...")
            menu_function()

        case _:
            print("This information does not match an account.")
            input("Press any key to return...")
            menu_function()


def option_five():
    print("Goodbye.")


def menu_function(option=None):
    """Displays main menu, calls itself with if user chooses incorrect option.

    Args:
        option (str, optional): Used to display incorrect menu option.
    """

    option_funcs = [
        option_one,
        option_two,
        option_three,
        option_four,
        option_five,
    ]

    print(menu_string)

    if option:
        print(f"{option} is not a valid option.")
        print("Please pick an option from 1 to 5.")

    input = input_int("Enter an option from 1-5:")

    if input > 0 and input <= len(option_funcs):
        option_funcs[input - 1]()  # Call function from list
    elif input == 0:
        # Due to the if option logic above, int 0 would return false.
        menu_function("0")
    else:
        menu_function(input)


menu_function()
