import pyhop

def move(state, mover, start, end):
    if state.at[mover] == start:
        state.at[mover] = end
        return state
    else:
        return False

def take(state, obj, location):
    if state.at['robot'] == state.at[obj] and state.at[obj] == location:
        state.holding = obj
        del state.at[obj]
        return state
    else:
        return False

def drop(state, obj, location):
    if state.at['robot'] == location and state.holding == obj:
        state.holding = None
        state.at[obj] = location
        return state
    else:
        return False

pyhop.declare_operators(move, take, drop)
print('')
pyhop.print_operators()

def deliver(state, obj, destination):
    obj_start = state.at[obj]
    return [('move', 'robot', state.at['robot'], obj_start),
            ('take', obj, obj_start),
            ('move', 'robot', obj_start, destination),
            ('drop', obj, destination)]

pyhop.declare_methods('deliver', deliver)

state1 = pyhop.State('state1')
state1.at = {'robot':'dock', 'mail':'mailroom'}
state1.holding = None

pyhop.pyhop(state1,[('deliver','mail','office')],verbose=3)