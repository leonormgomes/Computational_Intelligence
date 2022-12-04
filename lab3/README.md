## Colaborators and co-authors
I colaborated and wrote the code together with Angelica Ferlin, Mathias Schmekel, Karl Wennerström and Erik Bengtsson.

## Other sources
https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab3_nim.ipynb

### 3.1
https://en.wikipedia.org/wiki/Nim

### 3.2

**Rules**

Structure of an individual:

indv = {'Rule1': a, 'Rule2': [b, c], 'Rule3': [d, e], 'Rule4': [f, g], 'Rule5': [h, i], 'fitness': k}

Parameters:

 - a, c, e, g and i = how many elems should be left in a row after the agent has played (if the parameter > elem in row -> take one elem),
 - b, d, f, h = indicates which row to pick from, depending on rule.

The rules whose parameters are evolved:

- *Rule1*: If only one active row left on the board, leave a number of parameters.
- *Rule2*: If even amount of active rows are left on the board and only one of the rows has more than 1 elem:
  - if b = 0 -> take from row with only one elem
  - if b = 1 ->  leave c amounts of elem in row w/ > than one elem.
- *Rule3*: If even amount of active rows are left on the board and more than 2 rows have multiple elems:
  - if d = 0 -> leave e elem in the shortest row
  - if d = 1 -> leave e elem in the longest row
- *Rule4*: If odd amount of active rows are left on the board and only one of the rows has more than 1 elem:
  - if f = 0 -> take from row with only one elem
  - if f = 1 -> leave g amounts of elem in row  w/ > than one elem.
- *Rule5*: If odd amount of active rows are left on the board and more than 1 row have multiple elems:
  - if h = 0 ->  leave i elem in the shortest row
  - if h = 1 -> leave i elem in the longest row 

**Strategy**
1. Create inital population (with POPULATION_SIZE) where each player has the same set of rules but different parameters.
2. Generate offspring where OFFSPRING_SIZE>>POPULATION_SIZE:
    - k individuals compete against each other and the fittest becomes a parent. This is done twice for two parents to be created.
    - Perform crossover between two parents and create one child. The child is mutated based on a probability.
3. To calculate the fitness, each child plays 10 games against each of the three agents, one dumb, one random and one optimal.
    - The fitness = (wins_against_optimal_agent, wins_against_random_agent, wins_against_dumb_agent)
4. The top fittest children of size POPULATION_SIZE are selected.
5. Repeat 2-3 steps GENERATION amount of times.
6. The rules of the best individuals become the stratetgy.


### 3.3
The task 3.3 of the Mini-max was heavily inspired and some code was taken from this tutorial: https://realpython.com/python-minimax-nim/

### 3.4
https://andrewrowell.blog/2020/05/19/q-learning-nim-with-python/
https://github.com/andrewrowell/NimQLearning/blob/master/nim.py
https://github.com/abelmariam/nimPy/blob/master/Nim.py
https://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand11/Group6Lars/erikjarleberg.pdf


