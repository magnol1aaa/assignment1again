text_spacer = "-----------------------------------"
def display_menu(option=None):
    print("")
    print(text_spacer)
    print("Main Menu")
    print(text_spacer)
    print("1. Enter usage details")
    print("2. Display current usage details")
    print("3. Display plan costs")
    print("4. Reccomend best plan")
    print("5. Exit")
    print("")
    print(f"{option} is not a valid option. Please pick an option from 1 to 5." if option else text_spacer)
    print("Pick an option from 1 to 5.")
    resp = get_response(True, [1, 5])
    if resp[0] == False:
        display_menu(resp[1])
    else:
        option_process(resp[1])

def option_process(option):
    match option:
        case 1:
            print("option 1")
        case 2:
            print("option 2")
        case 3:
            print("option 3")
        case 4:
            print("option 4")
        case 5:
            print("option 5")

def get_response(is_int=None, in_range=[]):
    to_return = input("Enter here:")
    input_int = 0
    if is_int:
        try:
            input_int = int(to_return)
            if in_range:
                if input_int >= in_range[0] and input_int <= in_range[1]:
                    return [True, input_int]
                else:
                    return [False, input_int]
        except ValueError:
            return [False, to_return]

def enter_usage():
    minutes = input("How many call minutes do you typically use a month?")
    data = input("How many gigabytes of data do you typically use a month?")
    roaming = input("Do you need a plan that offers international roaming?")

    current_user_details = [minutes, data, roaming]
    



display_menu()