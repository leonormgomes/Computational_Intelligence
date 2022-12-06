from utils import *
from other_agents import *
from genetic_algorithm import *
from reinforcement_learning import *
from minimax import * 

NIM_SIZE = 5

def play_nim(agent1: Callable, opponent: Callable, nim_size = 5):
    nim = Nim(nim_size)
    logging.debug(f"status: Initial board  -> {nim}")
    
    strategy = (agent1, opponent)
    player = 0

    while nim:
        ply = strategy[player](nim)
        nim.nimming(ply)
        logging.debug(f"status: After player {player} -> {nim}")
        player = 1 - player
    winner = 1 - player
    logging.info(f"status: Player {winner} won!")


#Expert Agent plays
play_nim(nim_sum, dumb)
print("played nim_sum with dumb")

play_nim(nim_sum, random_agent)
print("played nim_sum with random")

play_nim(nim_sum, optimal_startegy)
print("played nim_sum with optimal strategy")


#Evolution Algorithm plays
evolution_strat = make_strategy(evolution_agent(NIM_SIZE))
play_nim(evolution_strat, dumb)
print("played evolution with dumb")

play_nim(evolution_strat, random_agent)
print("played evolution with random")

play_nim(evolution_strat, optimal_startegy)
print("played evolution with optimal_strategy")


#Minimax Algorithm plays - using nim size of 3 bc it is a slower agent
play_nim(minimax_agent, dumb, 3)
print("played minimax with dumb")

play_nim(minimax_agent, random_agent, 3)
print("played nim with random")

play_nim(minimax_agent, optimal_startegy, 3)
print("played minimax with optimal_strategy")


#Q-Learning Algorithm Plays
q_learner = q_learner_strategy(NIM_SIZE)
play_nim_qlearner(q_learner, dumb)
print("played q_learner with dumb")

play_nim_qlearner(q_learner, random_agent)
print("played q_learner with random")

play_nim_qlearner(q_learner, optimal_startegy)
print("played q_learner with optimal_strategy")




