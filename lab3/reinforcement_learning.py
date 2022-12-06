#Q-learning

from utils import *
from other_agents import *

#Variables 
NUM_GAMES = 10 # number of games against each type of opponent
OPPONENTS = [dumb, hard_coded_agent, random_agent, random_smart_agent, optimal_startegy]
NIM_SIZE = 5

class QLearner:
    #learning rate and discount factor

    REWARD = 1
    PENALTY = -1
    previous_state = None
    previous_move = None

    def __init__(self, learning_rate, discount_rate, exploration_rate):
       q = {} # (state_rows: list, move: tuple (row, elem)) -> value: int
       self.q = q
        
       #in a deterministic environment, the optimal learning rate is 1
       #in practice, often a constant learning rate is used
       self.learning_rate = learning_rate
       #starting with a lower discont factor and increasing it towards its final value acelerates learning
       self.discount_rate = discount_rate
       #try to reduce the exploration rate while we are training the q-learner 
       self.exploration_rate = exploration_rate
    
    def clear_previous_vars(self):
      self.previous_state = None
      self.previous_move = None
    
    def change_exploration_rate(self, new_exploration_rate):
      self.exploration_rate = new_exploration_rate

    def change_discount_rate(self, new_discount_rate):
      self.discount_rate = new_discount_rate

    def change_learning_rate(self, new_learning_rate):
      self.learning_rate = new_learning_rate

    def add_state_moves(self, current_state): #function to add new state, moves combinations
      
      data = cook_status(current_state)
      possible_moves = data['possible_moves']

      for move in possible_moves:
        if (current_state.rows, move) not in self.q: #adds the combination state, move to the q
          self.q[(current_state.rows, move)] = np.random.uniform(0.0,0.01) #attribute a small random value 
    
    #gets the move to apply
    def policy(self, current_state):

      data = cook_status(current_state)
      possible_moves = data['possible_moves']

      if np.random.random() > self.exploration_rate:

        #we want to return the action with the biggest value
        q_val_list = [self.q[(current_state.rows, move)] for move in possible_moves] #list of the values of state and action
        max_val_index = np.argmax(q_val_list) #returns the index of the max element of the array 
        return possible_moves[max_val_index]  #returns the move with the biggest q_value

      else: #we explore
        return random.sample(possible_moves, 1)[0] #returns a random possible move - moves are in tuples
    
    def updateQ(self, current_state): #current_state: Nim

      if not current_state: #if the game is finished
        self.q[(self.previous_state, self.previous_move)] += \
                self.learning_rate * (self.PENALTY - self.q[(self.previous_state, self.previous_move)]) 
        current_move = self.previous_state = self.previous_move = None #clear in order to prepare for the next game

      else: #if the game is not finished 
        self.add_state_moves(current_state) #adds the new state, moves
        current_move = self.policy(current_state) #gets the move that we want to use

        if self.previous_move is not None: #if it is not the first move
          next_state = deepcopy(current_state) #current_state: Nim
          next_state.nimming(Nimply(current_move[0], current_move[1])) #get the next state applying the move (result of your move)

          reward = 0 if next_state else self.REWARD #gets the value of the reward, if it wins, reward = 1
          logging.debug(f" REWARD: {reward}")
          data = cook_status(current_state)
          possible_moves = data['possible_moves']

          maxQ = max([self.q[(current_state.rows, move)] for move in possible_moves]) #max qvalue from the possible moves of the current_state

          
          self.q[(self.previous_state, self.previous_move)] += \
                    self.learning_rate * (reward + (self.discount_rate * maxQ) - \
                    self.q[(self.previous_state, self.previous_move)]) 

        self.previous_state, self.previous_move = current_state.rows, current_move
        logging.debug(f"current_move - game not finished: {current_move}")
      return current_move

def play_q_learning(nim_size, q_learner, external_agent): #plays the game once
  nim = Nim(nim_size) #creates nim

  #q-learner is the first player
  #second player is the external agent - can be either dumb, random, optimizer

  game_on = True #bool that is true while the game is happening
  is_q_learner = True #we start with q-learner

  while game_on:

    if is_q_learner: #if the current player is our q_learner
        move_params = q_learner.updateQ(nim)
        logging.debug(f" Wanted move after player = q-learner: {move_params}, State before move: {nim}")
        
        if(move_params == None): #if q_learner loses
            logging.debug(f" Q-learner lost")
            return "q_learner lost"
        
        move_to_apply = Nimply(move_params[0], move_params[1])
        logging.debug(f"move to apply: {move_to_apply}")
        nim.nimming(move_to_apply)
        
        logging.debug(f" <<NIM>> after q-learner move: {nim}")
        
        if(sum(nim.rows) == 0): #if q_learner wins
            logging.debug(f"Q-learner won")
            q_learner.clear_previous_vars()
            
            return "q_learner won"
        
        is_q_learner = False
    
    else: #if the current player is the external agent
        move_to_apply = external_agent(nim) 
        logging.debug(f" Agent move to apply: {move_to_apply}")
        nim.nimming(move_to_apply)
        is_q_learner = True


logging.getLogger().setLevel(logging.INFO)

def q_learner_strategy(nim_size) -> QLearner: #function to train the q_learner
  #q_learner will play against dumb, random, optimizer
  num_games = 200
  current_explorration_rate = 0.6
  q_learner_agent = QLearner(learning_rate=0.9, discount_rate=0.4, exploration_rate=current_explorration_rate) #change this later

  for opponent in OPPONENTS:
    for game in range(num_games):
        play_q_learning(nim_size, q_learner_agent, opponent)
        logging.debug(f" GAME FINISHED")
    current_explorration_rate -= 0.10 #Exploration vs Exploitation
 
    if (current_explorration_rate < 0.1):
      current_explorration_rate = 0.1
    
    q_learner_agent.change_exploration_rate(current_explorration_rate)
    num_games += 2*(game+1)
  return q_learner_agent

#IMPROVEMENT POINT: practice against each opponent until 100% winning rate (except in optimal strategy)

def play_nim_qlearner(q_learner: QLearner, opponent: Callable):

    result = play_q_learning(NIM_SIZE, q_learner, opponent)
    print(result)

strat = q_learner_strategy(NIM_SIZE)

#for _ in range(100):
    #play_nim(strat, optimal_startegy)


