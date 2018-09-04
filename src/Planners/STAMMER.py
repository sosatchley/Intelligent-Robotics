import pyhop
import domains
def GoTo(state, start, end):
    if (state.at['robot'] == start):
        state.at['robot'] = end
        return state
    else:
        return False
    
def shred(state, document):
    if state.holding == document:
        state.shredded.append(document)
        state.holding = None
        return state
    else:
        return False
        
def take(state, document, office):
    if (state.at[document] == office) and (state.at['robot'] == office) and (state.holding == None):
        state.holding = document
        del state.at[document]
        return state
    else:
        return False
        
def leave(state, document, office):
    if (state.holding == document):
        state.at[document] = office
        state.holding = None
        return state
    else:
        return False
        
def sign(state, document, office):
    if (state.at[document] == office):
        state.signed.append(document)
        return state
    else:
        return False
    
pyhop.declare_operators(GoTo, shred, take, leave, sign)
print("")
pyhop.print_operators()

def goAndGet(state, document):
    robot_start = state.at['robot']
    doc_start = state.at[document]
    return [('GoTo', robot_start, doc_start),
            ('take', document, doc_start)]
pyhop.declare_methods('goAndGet', goAndGet)
     
def deliver(state, document, office):
    robot_start = state.at['robot']
    return[('GoTo', robot_start, office),
           ('leave', document, office)]
pyhop.declare_methods('deliver', deliver)
 
def takeAndSign(state, document, office):
    return [('deliver', document, office),
            ('sign', document, office),
            ('take', document, office)]
pyhop.declare_methods('takeAndSign', takeAndSign)



pyhop.pyhop(domains.state1, domains.prob1, verbose=1)

    


