from utils import *

def nim_sum(nim): #hard coded optimal agent

  X = nim._rows[0]

  # X is the nim_sum(bitwise xor) of all heap sizes
  for i in range(1, len(nim._rows)):
    X = X ^ nim._rows[i]

  nim_sum_val = []

  # calculate the nim_sum between X and each heap size
  for i in nim._rows:
    val = i ^ X
    nim_sum_val.append(val)

  row = "false"
 
  for i in range(len(nim_sum_val)):
    if nim_sum_val[i] < nim._rows[i]:
      row = i
      break
  
  # reduce that heap to value nim_sum
  if (row != "false"):
    num_objects = nim._rows[row] - nim_sum_val[row]
    move = Nimply(row, num_objects)
  
  else:
    rand_row = random.randrange(0,len(nim._rows))

    while(nim._rows[rand_row] == 0):
      rand_row = random.randrange(0,len(nim._rows))

    if(nim._rows[rand_row] != 1):
      rand_obj = random.randrange(1, nim._rows[rand_row])
                                  
    else: rand_obj = 1

    move = Nimply(rand_row, rand_obj)
  
  return move