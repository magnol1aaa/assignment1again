# Imports
from main_utils import UsageDetails, open_json,  get_input

# Vars
menu_string = """
Main Menu
----------
1. Enter usage details
2. Display current usage
3. Display plan costs
4. Reccomend best plan
5. Exit
----------
"""
option_list = []
usage_storage = None
        
def menu_function(option=None):
    print(menu_string)
    print(f"{option} is not a valid option. Please pick an option from 1 to 5." if option else "")
    input_string = input("Enter an option from 1-5:")
    try:
        input_int = int(input_string)
        if input_int > 0 and input_int <= 5:
            print("do option")
        else:
            raise ValueError
    except ValueError:
        menu_function(input_string)

def option_one():
    call_time = get_input("How many call minutes do you typically use a month? Enter a number:", int)
    data_time = get_input("How many gigabytes of data do you typically use a month? Enter a number:", int)
    roaming_bool = get_input("Do you need a plan that offers international roaming? Y(es) / N(o):", bool)
    user_data = UsageDetails(call_time, data_time, roaming_bool)
    if 
menu_function()