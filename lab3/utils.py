import logging
from collections import namedtuple
import random
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor
import numpy as np

Nimply = namedtuple("Nimply", "row, num_objects") #move

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
    

def pure_random(state: Nim) -> Nimply: #function from the professor
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)



def nim_sum_val(state: Nim) -> int: #function from the professor
  *_, result = accumulate(state.rows, xor)
  return result

def active_rows_index(state):
    
    active_rows_index = []
    idx = 0
    
    for o in state.rows:
        if o > 0:
          active_rows_index.append(idx)
        idx += 1
        
    return active_rows_index

def cook_status(state): #part of the function is from the professor
    
    cooked = dict()
    
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ] #possible moves
    
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows) #number of rows that are not 0
    cooked["active_rows_index"] = active_rows_index(state) #get the index of rows that are not 0
    
    #get the index and the value of rows that only have one elem
    cooked["rows_with_one_element"] = [(index, r) for index, r in enumerate(state.rows) if r == 1] 
    
    #get the index and the value of rows that have more than one elem
    cooked["rows_multiple_elem"] = [(index, r) for index, r in enumerate(state.rows) if r > 1]
    
    #get the shortest row
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    
    #get the long row
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    
    
    cooked["nim_sum"] = nim_sum_val(state) #get the best move
    
    cooked["pure_random"] = pure_random(state) #get a random move

    brute_force = list()
    
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum_val(tmp)))
        
    cooked["brute_force"] = brute_force

    return cooked
