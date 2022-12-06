from utils import *

def optimal_startegy(state: Nim) -> Nimply: #function from the professor
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]

def random_agent(state): #An agent returning a random move
    data = cook_status(state)
    return data["pure_random"]

def dumb(state): #A dumb agent that always picks one element from the longest row
    data = cook_status(state)
    row = data["longest_row"]
    return Nimply(row, 1)

def random_smart_agent(state: Nim): # A random agent that is smarter than pure agent
    data = cook_status(state)
    if (data["active_rows_number"] == 1): #if we have only one line left, we take all the elements
        row = data["active_rows_index"][0]
        elem = state.rows[row]
        ply = Nimply(row, elem)
    else:
        ply = data["pure_random"]
    return ply

def hard_coded_agent(state: Nim): #Agent using fixed rules
    
    data = cook_status(state=state)

    active_rows_number = data["active_rows_number"]
    active_rows_index = data["active_rows_index"]
    rows_with_multiple_elem = data["rows_multiple_elem"]
    longest_row = data["longest_row"]

    if active_rows_number == 1:
        row = active_rows_index[0]
        elem = state.rows[row]
        
    elif active_rows_number % 2 == 0:
        if len(rows_with_multiple_elem) == 1: 
            row = rows_with_multiple_elem[0][0]
            elem = rows_with_multiple_elem[0][1] - 1 # take all elem exept one
            logging.debug(f"Even rows one mul, elem: {elem}") 
        else:
            row = longest_row
            logging.debug(f"longest row index: {longest_row}, elem: {state.rows[longest_row]}")
            elem = max(state.rows[longest_row] - 1, 1) # take all elem exept one
            logging.debug(f"Even rows, several mul, elem: {elem}") 
    else:
        if len(rows_with_multiple_elem) == 1:
            row = rows_with_multiple_elem[0][0]
            elem = rows_with_multiple_elem[0][1] # take all elem
            logging.debug(f"Odd rows, one mul, elem: {elem}") 
        else:
            row = longest_row
            elem = state.rows[longest_row]
            logging.debug(f"Even rows, several mul, elem: {elem}") 

    ply = Nimply(row, elem)
    return ply