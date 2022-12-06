from utils import *
from other_agents import *
from expert_system import *

# variables
OFFSPRING_SIZE = 200
K= 5
POPULATION_SIZE = 50
TOURNAMENT_SIZE = 5

OPPONENT = [optimal_startegy, random_agent, dumb] #opponents 

#Rule 1

def one_row_left(state, data, genome): #Rule 1 - if only one row left: leave x sticks
    
    
    active_row = data["active_rows_index"][0]
    elem_last_row = state.rows[active_row] #active_rows_index returns a list -> need to get the first one
   
    if elem_last_row < genome['Rule1']: #if the rule want to leave more sticks than exists in row
        ply = Nimply(active_row, 1)
        
    else:
        
        elem_to_remove = max(elem_last_row - genome["Rule1"], 1) #if take more elem than exists -> take all
        ply = Nimply(active_row, elem_to_remove)

    return ply

def rule_one_multiple_left(state, data, genome, rule): #Rule 2 and 4 
    
  active_rows_index = data["active_rows_index"]
  single_elem_rows = data["rows_with_one_element"]
  multiple_elem_rows = data["rows_multiple_elem"]


  if genome[rule][0] == 0:  # take from row with one elem
    
    elem = 1 # want to take the last elem in row
    single_elem_row = single_elem_rows[0][0] # looks like [(row,elem),(row,elem)] if two rows with single elem
    ply = Nimply(single_elem_row, 1) #takes from the first row that has 1 elem

  else: #take from the row with more than one element

    if len(multiple_elem_rows) == 0: #if single elem in all rows
      row = single_elem_rows[0][0]
      elem = 1
        
    else: 
      row = multiple_elem_rows[0][0] # [(row,elem)] -> since only one row with multiple elem
    
    if (genome[rule][1] > state.rows[row]): # if it wants to leave more elem than exists in row
      elem = 1
                        
    else: 
        
      elem = max(state.rows[row] - genome[rule][1], 1)
    
    ply = Nimply(row, elem)
      
  return ply


def rule_several_multiple_left(state, data, genome, rule): #Rule 3 and 5

  if (genome[rule][0] == 0): # choose from row with fewest elemt
    row = data['shortest_row']
    
  else: #choose from row with biggest elem
    row = data['longest_row']
      
  elem = max(state.rows[row] - genome[rule][1], 1)
  ply = Nimply(row, elem)

  return ply

def even_rows_left(state, data, genome): #rules for when we have an even number of non-zero rows
    
  rows_multiple_elem = data["rows_multiple_elem"]

  if len(rows_multiple_elem) == 1: # Rule 2 - only one row with multiple elems
    
    ply = rule_one_multiple_left(state, data, genome,'Rule2')
  
  else: # Rule 3 - more than one row with multiple elems 
           
    ply = rule_several_multiple_left(state, data, genome,'Rule3')

  return ply


def odd_number_of_rows_left(state, data, genome):  #rules for when we have an odd number of non-zero rows
    
    rows_multiple_elem = data["rows_multiple_elem"]

    if len(rows_multiple_elem) == 1: # Rule 4 - only one row with multiple elems
        ply = rule_one_multiple_left(state, data, genome,'Rule4')
  
    else: # Rule 5 - more than one row with multiple elems             
        ply = rule_several_multiple_left(state, data, genome,'Rule5')

    return ply

def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        
        data = cook_status(state)

        active_rows_number = data["active_rows_number"]

        #only one active row left - we choose Rule 1
        if active_rows_number == 1:
            ply = one_row_left(state=state,data=data, genome=genome) 
        
        #even number of rows left - we choose Rule 2 or 3
        elif active_rows_number %2 == 0: # even numbers

            ply = even_rows_left(state=state, data=data, genome=genome)

        #odd number of rows left - we choose Rule 4 or 5
        else: 
            ply = odd_number_of_rows_left(state=state, data=data, genome=genome)

        return ply

    return evolvable

def head2head(individual1, opponent, nim_size): #compute the fitness - makes two players compete against each other
    won = 0
    
    nim = Nim(nim_size) #creates the board

    players = (make_strategy(individual1), opponent) #gets the players
    player = 0
    
    while nim:
        
        ply = players[player](nim)
        nim.nimming(ply)
        player = 1 - player
        
    winner = 1 - player
    
    if winner == 0:
        return 1
    else:
        return 0


def calculate_fitness(population, nim_size): # calculate fitness for whole population
    NUM_MATCHES = 10
    
    for p1 in population:
        
        fitness = []

        for strat in OPPONENT: #plays against optimal player, random player and dumb player 
            wins = 0
            
            for _ in range(NUM_MATCHES):
                wins += head2head(p1, strat, nim_size)
                
            fitness.append(wins/NUM_MATCHES)
            
        p1['fitness'] = (fitness[0], fitness[1], fitness[2]) #fitness according to each type of player

def init_population(nim_size): #initiates population
    
    population = []
    max_leave = (nim_size-1)*2 # last row of the table will have nim_size*2-1 objects

    cond = POPULATION_SIZE
    
    while cond: #creates individuals
        individual = {'Rule1': random.randint(0,max_leave), 'Rule2': [random.randint(0,1), max_leave], 'Rule3': [random.randint(0, 1), random.randint(0, max_leave)],
        'Rule4': [random.randint(0,1), max_leave], 'Rule5': [random.randint(0,1), max_leave]}
        
        individual['fitness'] = ()
        population.append(individual)
        
        cond -= 1
        
    return population

def k_fittest_indv(population, k): #gets the k fittest individuals of a population
    return sorted(population, key=lambda indv: indv['fitness'], reverse=True)[:k]

# select k random individuals, return the one with best fitness
def tournament(population):    
    
    contestors = random.sample(population, TOURNAMENT_SIZE)
    best_contestor = sorted(contestors, key=lambda indv: indv['fitness'], reverse=True)[0] #sorts contestors by descending order of fitness
  
    return best_contestor
    

def crossover(parent1, parent2, mutation_prob): # take two parents and create one child w/ a mutation probability
    
    rules_parent1 = [key for key in parent1.keys() if 'Rule' in key] #gets rules in parent genome
    
    child = {}

    for rule in rules_parent1:
        which_parent = random.randint(0,1)
        
        if which_parent == 0: # take parameters from parent1
            child[rule] = parent1[rule]
            
        else: #take parameters from parent 2
            child[rule] = parent2[rule]
    
    child['fitness'] = ()
    rules = [key for key in child.keys() if 'Rule' in key]

    #mutation
    if random.random() < mutation_prob:
        
        rule = random.choice(rules) #chooses a random rule to mutate
        r1 = parent1[rule]
        r2 = parent2[rule]

        if rule == 'Rule1':
            mean = int((r1+r2)/2) #mutates to average of values of rule 1
            child[rule] = mean

        else:
            mean_val_one = int((r1[0]+r2[0])/2)
            mean_val_two = int((r1[1]+r2[1])/2)
            child[rule] = [mean_val_one, mean_val_two]
    
    return child

def create_offspring(population, mutation_prob): #gets new population of offspring
    offspring = []
    
    for i in range(OFFSPRING_SIZE):
        parent1 = tournament(population) #gets parent 1
        parent2 = tournament(population) #gets parent 2

        child = crossover(parent1, parent2, mutation_prob=mutation_prob) #crossover between parent 1 and 2 and creates one child
        
        offspring.append(child)
        
    return offspring

def get_next_generation(population): #sorts the population in descending order by fitness and returns the k ones with best fitness
    best_k_indv = sorted(population, key=lambda child: child['fitness'], reverse=True)[:POPULATION_SIZE]
    return best_k_indv


# GAME
nim_size = 5
GENERATIONS = 2

def evolution_agent(nim_size):
    population = init_population(nim_size) #creates population
    
    for _ in range(GENERATIONS):
    
        offspring = create_offspring(population, 0.2) #creates a new offspring
    
        calculate_fitness(offspring, nim_size) #calculates fitness of offspring
    
        population = get_next_generation(offspring) #gets new population from best offspring
        
    best_indv = population[0]
    logging.debug(f"best player {best_indv}")
    
    return best_indv

#print(evolution_agent(nim_size))