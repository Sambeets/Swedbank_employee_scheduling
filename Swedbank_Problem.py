
#
# Imports
#

from pyomo.environ import *

###################################
# Model Begins
###################################


model = AbstractModel()
model.i = Set() # Set of time
model.j = Set() # Set of day
model.k = Set() # Set of tasks
model.v = Set() # Set of employees

# Parameters
model.c = Param(model.k, within= PositiveReals) # duration of tasks of type k 
model.a = Param(model.i, model.j, within= PositiveReals) # delay proirities
model.w = Param(model.i, model.j, model.k, within= PositiveReals) # number of tasks (type k) received at time (i,j)
model.n = Param() # number of employees
model.theta0 = Param() # preparation time 
model.theta1 = Param() # starting time of batch 1
model.theta2 = Param() # starting time of batch 2

# Variables
model.alpha = Var(model.i, model.j, model.v, within=Binary) # variable alpha (whether i,j is the starting time of employes v)
model.beta = Var(model.i, model.j, model.v, within=Binary) # variable beta (whether i,j is the ending time of employees v)
model.tau = Var(model.i, model.j, model.v, within=Binary) # variable tau (availability employee working at time i,j )
model.delta = Var(model.i, model.j, within=NonNegativeReals, default=0.0) # variable (amount of delay at time i,j ) 



# Constraints

def const1_rule(model,i,j,v):
    return sum(sum(model.tau[i,j,v] for m in model.i) for n in model.j ) == 160- model.theta1
model.const1_rule = Constraint(model.i, model.j, model.v, rule=const1_rule)

def const2_rule(model,i):
    return sum(model.alpha[i,j,v] for n in model.i) == 1
model.const2_rule = Constraint(model.i, rule = const2_rule)

def const3_rule(model,i):
    return sum(model.beta[i,j,v] for n in model.i) == 1
model.const3_rule = Constraint(model.i, rule = const3_rule)

def const4_rule(model,i,j,v):
    if i != model.theta_1 or i != model.theta_2:
        return model.alpha[i,j,v] == 0
    else:
        return model.alpha[i,j,v] == 1
model.const4_rule = Constraint(model.i, model.j, model.v,  rule = const3_rule)

def const5_rule(model,i,j):
	return model.tao[i,j,v] <= sum(model.alpha[i,j,v] for n in model.k)
model.const5_rule = Constratint(model.i, model.j, rule = const5_rule)

def const6_rule(model,j,v):
	return model.tao[i,j,v] <= 1- sum(model.beta[i,j,v] for n in model.k)
model.const6_rule = Constratint(model.i, model.j, rule=const6_rule)

def const7_rule(model,i,j):
	return model.c[k] * model.w[j,j,k] <= sum(model.tao[i,j,v] + model.delta[i,j] for n in model.v)
model.const7_rule = Constratint(model.i, model.j, rule = const7_rule)


# pyomo solve --solver=glpk 02Model_Pyomo.py model2.dat
