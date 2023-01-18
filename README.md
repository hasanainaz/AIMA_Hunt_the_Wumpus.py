# AIMA_Hunt_the_Wumpus.py
A Python Implementation of the AIMA Standard AI Problem: "The Wumpus World" by the Tkinter library.

### Preview: 

https://youtu.be/zrhz1PlEX2Q


### Introduction

"Hunt the Wumpus" is a classic video game that was designed by Gregory Yob in 1973 and was one of the TI-99 famous games in 1979. We placed this Python variation on the standard AI problem described by Stuart Russell & Peter Norvig in "Artificial Intelligence: A Modern Approach", 2020, Global, 4th Ed. The player has to move to block [-1,0] from block [0,0] for the Climb action.

### How to Use

1. Use the following code for a human player:
```
import MP2Game
_ = MP2Game.HuntTheWumpusGame()
```

2. Use the following code for a computer player:
```
import MP2Game
import time
from sympy import ask, Symbol, Equivalent
from sympy import satisfiable, And
cnts = MP2Game.HuntTheWumpusGame(human = False)
# <-------------------------------- Add your initialization code here.
Wumpus_alive = True
while True: 
    sensors = cnts.percept()
    if not sensors:
        Wumpus_alive = True
        # <-------------------------------- Add your reset code here.
        cnts.start()
        continue
    # here is the location of the agent at this time step for simplification
    x = cnts.x
    y = cnts.y
    
    # update your agent's knowledge base 
    # <-------------------------------- here
    
    if (sensors[0] == "Stench") & Wumpus_alive:
        # <-------------------------------- here
    else:
        # <-------------------------------- here
    if sensors[1] == "Breeze":
        # <-------------------------------- here
    else:
        # <-------------------------------- and here
        
    if sensors[2] == "Glitter":
        cnts.action( "Grab" )
    if sensors[4] == "Scream":
        print( "Wumpus Killed" )
    
    # find and shoot the wumpus <-------------------------------- SOLVE this part at the end by using only Python code without any external library
                    # cnts.go_to( LineSight_x , LineSight_y )
                # cnts.shoot_at( WumpusLocation_x , WumpusLocation_y )
                # continue
    
    # Find the next best move 
    frontier = cnts.frontier()
    frontier.sort(key=lambda k: abs(k[0]-x) + abs(k[1]-y)  )
    destination = [-1,0]
    for d in frontier:
        # <-------------------------------- SOLVE this line first by checking whether the null hypothesis is unsatisfiable using the SymPy library.
            destination = d
            break
    # use cnts.action( "TurnRight" ), cnts.action( "TurnLeft" ), and response = cnts.action( "MoveForward" ), OR:
    response = cnts.action( destination ) # just keep this line for simplification.
    if not response:
        break
    time.sleep(0.2)
```

### Solution

A hybrid-agent implementation based on AIMA Global 4th edition (p259) is included in the Jupyter ipynb file.



