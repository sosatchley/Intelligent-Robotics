import pyhop
import domains

def move(state, start_pos, end_pos):
    if (state.robot_location == start_pos) :
        state.robot_location = end_pos
        return state
    else:
        return False
        
def mop(state, room):
    if (state.robot_location == room) :
        state.clean.append(room)
        return state
    else:
        return False
    
def lock(state, room):
    if (state.robot_location == room) and (room in state.clean):
        state.locked.append(room)
        return state
    else:
        return False

pyhop.declare_operators(move, mop, lock)

def clean_lock(state, room):
    return [('move', state.robot_location, room), 
            ('mop', room), 
            ('lock', room)]
pyhop.declare_methods('clean_lock', clean_lock)

def clean_lock_all(state, rooms):
    return [[('clean_lock', room)] for room in rooms]
#     return [('clean_lock', rooms[0]),
#             ('clean_lock', rooms[1]),
#             ('clean_lock', rooms[2]),
#             ('clean_lock', rooms[3]),
#             ('clean_lock', rooms[4])]
     
# Ideally, this function would include all dirty rooms in the state and 
# iteratively or recursively break the function down into the smaller
# methods and operations. I can't seem to figure out how to recurse or 
# iterate with pyhop's source code.

pyhop.declare_methods('clean_lock_all', clean_lock_all)

# pyhop.pyhop(domains.mopper1, domains.moprob, verbose=3)
pyhop.pyhop(domains.mopper2, domains.mopall, verbose=3)

