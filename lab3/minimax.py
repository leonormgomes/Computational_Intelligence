#https://realpython.com/python-minimax-nim/

from utils import *

def possible_new_states(nim_rows): #define all possible states 

  possible = []

  for row in range(len(nim_rows)) :

    for j in range(nim_rows[row]):
      new_state = deepcopy(nim_rows)

      new_state[row] = nim_rows[row] - j - 1
      possible.append(new_state)
  
  return possible


def evaluate(nim_rows, player): #evaluate if the game is finished
  if (sum(nim_rows) == 0):
    return -1 if player == 0 else 1 
  else: return None

def minimax(nim_rows, player): #minimax algorithm

  score = evaluate(nim_rows, player) 

  if score != None: #checks if the game is finished
    return score #once finished, returns the score

  if (player == 0): #player 0 is max

    scores = [minimax(new_state, player = 1) for new_state in possible_new_states(nim_rows)] 
    return max(scores) 

  else: #player 1 is min

    scores = [minimax(new_state, player = 0) for new_state in possible_new_states(nim_rows)] 
    return min(scores)


def best_move(nim_rows, player): #gets the best move considering the current state

  if player == 0:
    new_player = 1

    return max(
      (minimax(new_state, new_player), new_state)
        for new_state in possible_new_states(nim_rows)
    )
  else:
    new_player = 0

  return min(
        (minimax(new_state, new_player), new_state)
        for new_state in possible_new_states(nim_rows)
    )


def minimax_pruning(state, is_maximizing, alpha=-1, beta=1): #minimax algorithm with pruning - not working
    
    if (score := evaluate(state, is_maximizing)) is not None:
        return score

    scores = []
    
    for new_state in possible_new_states(state):
        scores.append(
            score := minimax_pruning(new_state, not is_maximizing, alpha, beta)
        )
        if is_maximizing:
            alpha = max(alpha, score) #if we find a good solution for player 0, alpha = 1
        else:
            beta = min(beta, score) #if we find a good solution for player 1, beta = -1
            
        if beta <= alpha: #when beta is -1 or alpha is 1, we no longer go through the tree
            break
            
    return (max if is_maximizing else min)(scores)

def best_move_pruning(state, player): #returns the best move using minimax pruning - not working
    if player == 0:
        return max(
            (minimax_pruning(new_state, is_maximizing=False), new_state)
            for new_state in possible_new_states(state)
        )
    else:
        return min(
            (minimax_pruning(new_state, is_maximizing=True), new_state)
            for new_state in possible_new_states(state)
        )

def nimply_move(current_state, new_state): #returns a nimply move based on the best move from minimax
    
    diff = 0
    row = len(current_state) #invalid row
    
    for i in range(len(current_state)):
        
        if current_state[i] != new_state[i]:
            diff = current_state[i] - new_state[i]
            row = i
            
    return Nimply(row, diff)


def minimax_agent(nim):
  _, new_state = best_move(nim._rows, 0)
  return nimply_move(nim.rows, new_state)


