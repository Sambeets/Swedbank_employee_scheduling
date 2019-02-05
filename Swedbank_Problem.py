
#
# Imports
#
# wl_abstract.py: AbstractModel version of warehouse location determination problem
from pyomo.environ import *

model = AbstractModel()
model.i = Set() # Set of time
model.j = Set() # Set of day
model.k = Set() # Set of tasks
model.v = Set() # Set of employees

# Parameters
model.c = Param(model.k, within= PositiveReals)
model.theta1 = Param()

# Variables
model.alpha = Var(model.i, model.j, model.v, within=Binary) # parameter alpha
model.beta = Var(model.i, model.j, model.v, within=Binary) # parameter beta
model.tao = Var(model.i, model.j, model.v, within=Binary) # parameter beta
model.delta = Var(model.i, model.j, model.v, within=NonNegativeIntegers, default=0.0) # variable




# Constraints

def const1_rule(model,i,j):
    return sum(sum(model.tao[i,j,v] for i in model.i) for j in model.j ) == 160- model.theta1
model.const1_cust = Constraint(model.i, model.j, model.v, rule=one_per_cust_rule)



# pyomo solve --solver=glpk 02Model_Pyomo.py model2.dat