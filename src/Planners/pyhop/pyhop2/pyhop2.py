"""
Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Pyhop should work correctly in both Python 2.7 and Python 3.2.
For examples of how to use it, see the example files that come with Pyhop.

Pyhop provides the following classes and functions:

- foo = State('foo') tells Pyhop to create an empty state object named 'foo'.
  To put variables and values into it, you should do assignments such as
  foo.var1 = val1

- bar = Goal('bar') tells Pyhop to create an empty goal object named 'bar'.
  To put variables and values into it, you should do assignments such as
  bar.var1 = val1

- print_state(foo) will print the variables and values in the state foo.

- print_goal(foo) will print the variables and values in the goal foo.

- declare_operators(o1, o2, ..., ok) tells Pyhop that o1, o2, ..., ok
  are all of the planning operators; this supersedes any previous call
  to declare_operators.

- print_operators() will print out the list of available operators.

- declare_methods('foo', m1, m2, ..., mk) tells Pyhop that m1, m2, ..., mk
  are all of the methods for tasks having 'foo' as their taskname; this
  supersedes any previous call to declare_methods('foo', ...).

- print_methods() will print out a list of all declared methods.

- pyhop(state1,tasklist) tells Pyhop to find a plan for accomplishing tasklist
  (a list of tasks), starting from an initial state state1, using whatever
  methods and operators you declared previously.

- In the above call to pyhop, you can add an optional 3rd argument called
  'verbose' that tells pyhop how much debugging printout it should provide:
- if verbose = 0 (the default), pyhop returns the solution but prints nothing;
- if verbose = 1, it prints the initial parameters and the answer;
- if verbose = 2, it also prints a message on each recursive call;
- if verbose = 3, it also prints info about what it's computing.
"""

# Pyhop's planning algorithm is very similar to the one in SHOP and JSHOP
# (see http://www.cs.umd.edu/projects/shop). Like SHOP and JSHOP, Pyhop uses
# HTN methods to decompose tasks into smaller and smaller subtasks, until it
# finds tasks that correspond directly to actions. But Pyhop differs from 
# SHOP and JSHOP in several ways that should make it easier to use Pyhop
# as part of other programs:
# 
# (1) In Pyhop, one writes methods and operators as ordinary Python functions
#     (rather than using a special-purpose language, as in SHOP and JSHOP).
# 
# (2) Instead of representing states as collections of logical assertions,
#     Pyhop uses state-variable representation: a state is a Python object
#     that contains variable bindings. For example, to define a state in
#     which box b is located in room r1, you might write something like this:
#     s = State()
#     s.loc['b'] = 'r1'
# 
# (3) You also can define goals as Python objects. For example, to specify
#     that a goal of having box b in room r2, you might write this:
#     g = Goal()
#     g.loc['b'] = 'r2'
#     Like most HTN planners, Pyhop will ignore g unless you explicitly
#     tell it what to do with g. You can do that by referring to g in
#     your methods and operators, and passing g to them as an argument.
#     In the same fashion, you could tell Pyhop to achieve any one of
#     several different goals, or to achieve them in some desired sequence.
# 
# (4) Unlike SHOP and JSHOP, Pyhop doesn't include a Horn-clause inference
#     engine for evaluating preconditions of operators and methods. So far,
#     I've seen no need for it; I've found it easier to write precondition
#     evaluations directly in Python. But I could consider adding such a
#     feature if someone convinces me that it's really necessary.
# 
# Accompanying this file are several files that give examples of how to use
# Pyhop. To run them, launch python and type "import blocks_world_examples"
# or "import simple_travel_example".


from __future__ import print_function
import copy,sys, pprint
from collections import deque

############################################################
# States and goals

# Obtained from: https://stackoverflow.com/questions/750908/auto-repr-method
class AutoRepr(object):
    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

class State(AutoRepr):
    """A state is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name

class Goal(AutoRepr):
    """A goal is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name


### print_state and print_goal are identical except for the name

def print_state(state,indent=4):
    """Print each variable in state, indented by indent spaces."""
    if state != False:
        for (name,val) in vars(state).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

def print_goal(goal,indent=4):
    """Print each variable in goal, indented by indent spaces."""
    if goal != False:
        for (name,val) in vars(goal).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(goal.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

############################################################
# Helper functions that may be useful in domain models

def forall(seq,cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True

def find_if(cond,seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x): return x
    return None

############################################################
# Commands to tell Pyhop what the operators and methods are

operators = {}
methods = {}

def declare_operators(*op_list):
    """
    Call this after defining the operators, to tell Pyhop what they are. 
    op_list must be a list of functions, not strings.
    """
    operators.update({op.__name__:op for op in op_list})
    return operators

def declare_methods(task_name,*method_list):
    """
    Call this once for each task, to tell Pyhop what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({task_name:list(method_list)})
    return methods[task_name]

############################################################
# Commands to find out what the operators and methods are

def print_operators(olist=operators):
    """Print out the names of the operators"""
    print('OPERATORS:', ', '.join(olist))

def print_methods(mlist=methods):
    """Print out a table of what the methods are for each task"""
    print('{:<14}{}'.format('TASK:','METHODS:'))
    for task in mlist:
        print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))

############################################################
# The actual planner

def pyhop(state,tasks,verbose=0):
    """
    Try to find a plan that accomplishes tasks in state. 
    If successful, return the plan. Otherwise return False.
    """
    if verbose>0: print('** pyhop, verbose={}: **\n   state = {}\n   tasks = {}'.format(verbose, state.__name__, tasks))
    result = find_first_plan(state, tasks, verbose)
    if verbose>0: print('** result =',result,'\n')
    return result

def find_first_plan(state, tasks, verbose=0):
    p = PlannerStep(state, tasks, verbose)
    choices = deque()
    while not p.is_complete():
        next_options = p.get_next_step()
        if next_options:
            for option in next_options:
                choices.append(option)

        if choices:
            p = choices.pop()
        else:
            if verbose>0: print("** No plan found **")
            return False
    return p.plan

def multi_pyhop(state,tasks,n,verbose=0):
    if verbose>0: print('** pyhop, verbose={}: **\n   state = {}\n   tasks = {}'.format(verbose, state.__name__, tasks))
    result = find_n_plans(state, tasks, n, verbose)
    if verbose>0:
        print('** found', len(result), 'plans:')
        for p in range(len(result)):
            print("Plan {} (length {}): {}".format(p + 1, len(result[p]), result[p]))
    return result

def find_n_plans(state, tasks, n, verbose=0):
    found = False
    end = True
    p = PlannerStep(state, tasks, verbose)
    choices = deque()
    plans = []
    while True:
        if p.is_complete():
            plans.append(p.plan)
            if len(plans) >= n:
                return plans
            else:
                found = True
                end = not end
        else:
            found = False
            next_options = p.get_next_step()
            if next_options:
                for option in next_options:
                    choices.append(option)
        if choices:
            if found and not end:
                p = choices.popleft()
            else:
                p = choices.pop()
        else:
            if verbose>0: print("** No plans left to be found **")
            return plans

class PlannerStep:
    def __init__(self, state, tasks, verbose, prev_states = set()):
        self.verbose = verbose
        self.state = state
        self.prev_states = {s for s in prev_states}
        self.prev_states.add(str(state))
        self.tasks = tasks
        self.plan = []
        self.depth = 0

    def is_complete(self):
        return self.tasks == []

    def get_next_step(self):
        if self.verbose > 1: print('depth {} tasks {}'.format(self.depth,self.tasks))
        if self.tasks == []:
            if self.verbose > 2: print('depth {} returns plan {}'.format(self.depth, self.plan))
            return [self]
        task1 = self.tasks[0]
        if task1[0] in operators:
            if self.verbose > 2: print('depth {} action {}'.format(self.depth, task1))
            return self.apply_operator(task1)
        elif task1[0] in methods:
            if self.verbose > 2: print('depth {} method instance {}'.format(self.depth, task1))
            return self.apply_method(task1)
        else:
            if self.verbose>2: print('depth {} returns failure'.format(self.depth))
            return []

    def apply_operator(self, task1):
        operator = operators[task1[0]]
        newstate = operator(copy.deepcopy(self.state), *task1[1:])
        if self.verbose > 2:
            print('depth {} new state:'.format(self.depth))
            print_state(newstate)
        if newstate:
            if str(newstate) in self.prev_states:
                if self.verbose > 2: print("Cycle; pruning...")
                return []
            else:
                return [self.operator_planner_step(newstate)]
        else:
            return []

    def operator_planner_step(self, newstate):
        p = PlannerStep(newstate, self.tasks[1:], self.verbose, self.prev_states)
        p.plan = self.plan + [self.tasks[0]]
        p.depth = self.depth + 1
        return p

    def apply_method(self, task1):
        relevant = methods[task1[0]]
        planner_steps = []
        for method in relevant:
            subtask_alternatives = method(self.state, *task1[1:])
            if subtask_alternatives:
                if self.verbose > 2:
                    print(len(subtask_alternatives), "alternative subtask lists")
                for subtasks in subtask_alternatives:
                    if self.verbose > 2:
                        print('depth {} new tasks: {}'.format(self.depth, subtasks))
                    planner_steps.append(self.method_planner_step(subtasks))
        return planner_steps

    def method_planner_step(self, subtasks):
        updated_tasks = subtasks + self.tasks[1:]
        p = PlannerStep(self.state, updated_tasks, self.verbose, self.prev_states)
        p.plan = self.plan
        p.depth = self.depth + 1
        return p
