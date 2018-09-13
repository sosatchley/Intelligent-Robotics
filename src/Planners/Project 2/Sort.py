'''
Created on Sep 4, 2018

@author: Shaneyboi
'''
import pyhop
import domains

def move(state, end):
#     if (state.robot_location != end) :
        state.robot_location = end
        return state
#     else:
#         return False
    
def take(state):
    if  (state.robot_location == 'A') and (state.holding == None) :
        state.holding = state.stack.get()
        return state
    else: 
        return False
    
def classify(state):
    if (state.holding == 'red'):
        state.red = True
        return state
    elif (state.holding == 'green'):
        state.green = True
        return state
    elif (state.holding == 'blue'):
        state.blue = True
        return state
    else:
        return False
        
def leave(state):
    if (state.holding == state.robot_location): 
        state.amounts[state.holding] += 1
        state.holding = None
        return state  
    else: 
        return False
        
pyhop.declare_operators(move, take, classify, leave)

pyhop.pyhop(domains.state22, domains.prob22, verbose=3)        