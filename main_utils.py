""" 
This module contains the core parts of the main script to keep it readable.
In particular it contains the utility functions and classes such as:

- Opening and handling the json files: open_json(), save_to_json().
- Verifying and converting user input: get_input().
- The class that defines the structure of the user data: UsageDetails.
"""
import json


class UsageDetails:
    """Class that allows for easy structuring of userdata"""
    def __init__(self, call_time, data_used, roaming_bool):
        self.call_time = call_time
        self.data_used = data_used
        self.roaming_bool = roaming_bool
        
    def __str__(self):
        return(
            f"Call Time: {self.call_time} "
            f"Data Used: {self.data_used} "
            f"Roaming Needed: {self.roaming_bool}"
        )
    
def save_to_json(data, file_name, overwrite=None):
    """
    This function saves input data to file_name path, it checks whether
    the input is a dictionary or if its an instance of Usage Details.  
    If it is an instance of Usage Details it converts it to a dictionary.  
    """
    if isinstance(data, dict):
        data_json = json.dumps(data)
        try:
            file = open(file_name)
        except FileNotFoundError:
            file = open(file_name, 'w')
        
            
    elif isinstance(data, UsageDetails):
        save_to_json(vars(data), file_name, overwrite)

        
def get_input(message, convert=None):
    """
    This function is used to read, verify and convert the user input.
    You pass the message to the function through the first parameter and then
    provide what type you wish to convert the input to.  Then it attempts a
    type conversion and if it fails that means the user input was incorrect.  
    Which then leads to it re-requesting the input and performing conversion again.
    """
    approve = ['y', 'yes'] 
    deny = ['n', 'no'] 
    
    user_input = input(message)
    if convert == int:
        try:
            return int(user_input)
        except:
            print(f"{user_input} is not a number.") 
            get_input(message, convert)
    elif convert == bool:
        if user_input.lower() in approve:
            return True
        elif user_input.lower() in deny:
            return False
        else:
            print("Please enter Yes/No or Y/N.")
            get_input(message, convert)
        
        
            
            
            
        
    