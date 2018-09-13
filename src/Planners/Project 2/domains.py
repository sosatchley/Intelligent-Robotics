'''
Created on Sep 2, 2018

@author: Shane
'''
import pyhop
import Queue
state1 = pyhop.State('state1')
state1.at = {'robot':'dock', 'birthCertificate':'Office 1'}
state1.holding = None
state1.signed = []
state1.shredded = []

prob1 = [('goAndGet', 'birthCertificate'),
         ('takeAndSign', 'birthCertificate', 'Office 2'),
         ('deliver', 'birthCertificate', 'Office 1')]

prob12 = [('take_deliver', 'birthCertificate', 'Office 2')]
prob13 = [('take_sign_deliver', 'birthCertificate', 'Office 3', 'Office 2')]

state2 = pyhop.State('state2')
state2.at = {'robot':'dock', 'Doc1':'AlbertsOffice', 'Doc2':'StusOffice', 
             'Doc3':'TedsOffice'}
state2.holding = None
state2.signed = []
state2.shredded = []

prob2 = [('take_sign_deliver', 'Doc1', 'MattsOffice', 'AlbertsOffice'),
         ('take_sign_deliver', 'Doc2', 'StusOffice', 'AlbertsOffice'),
         ('take_sign_deliver', 'Doc3', 'AlbertsOffice', 'AlbertsOffice')]

state3 = pyhop.State('state3')
state3.at = {'robot':'AlbertsOffice', 'Doc1':'AlbertsOffice', 'Doc2':'StusOffice', 
             'Doc3':'TedsOffice', 'Doc4':'AlbertsOffice', 'Doc5':'MattsOffice'}
state3.holding = None
state3.signed = []
state3.shredded = []

prob3 = [('take_sign_deliver', 'Doc1', 'MattsOffice', 'MattsOffice'),
         ('take_sign_deliver', 'Doc2', 'StusOffice', 'AlbertsOffice'),
         ('take_sign_deliver', 'Doc3', 'AlbertsOffice', 'StusOffice'),
         ('take_sign_deliver', 'Doc4', 'StusOffice', 'TedsOffice'),
         ('seek_destroy', 'Doc5')]


state22 = pyhop.State('state22')
state22.robot_location = 'A'
state22.holding = None
state22.amounts = {'red':0, 'green':0, 'blue':0}
state22.stack = Queue.Queue()
state22.stack.put(2)
state22.red = False
state22.green = False
state22.blue = False

prob22 = [('move', 'A', 'red')]

mopper1 = pyhop.State('mopper')
mopper1.robot_location = 'Hallway'
mopper1.clean = []
mopper1.locked = []
mopper1.dirty = ['Room 1']

moprob = [('clean_lock', 'Room 1')]

mopper2 = pyhop.State('mopper')
mopper2.robot_location = 'Hallway'
mopper2.clean = []
mopper2.locked = []
mopper2.dirty = ['Room 1', 'Room 2', 'Room 3', 'Room 4', 'Room 5']

mopall = ['clean_lock_all', mopper2.dirty]

