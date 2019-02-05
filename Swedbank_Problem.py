
#
# Imports
#

from pyomo.environ import *

###################################
# Model Begins
###################################


model = AbstractModel()
model.S = Set() # Set of time
model.D = Set() # Set of day
model.T = Set() # Set of tasks
model.V = Set() # Set of employees

# Parameters
model.c = Param(model.T, within= PositiveReals) # duration of tasks of type k 
model.a = Param(model.S, model.D, within= PositiveReals) # delay proirities
model.w = Param(model.S, model.D, model.T, within= PositiveReals) # number of tasks (type k) received at time (i,j)
model.n = Param() # number of employees
model.theta0 = Param() # preparation time 
model.theta1 = Param() # starting time of batch 1
model.theta2 = Param() # starting time of batch 2

# Variables
model.alpha = Var(model.S, model.D, model.V, within=Binary) # variable alpha (whether i,j is the starting time of employes v)
model.beta = Var(model.S, model.D, model.V, within=Binary) # variable beta (whether i,j is the ending time of employees v)
model.tau = Var(model.S, model.D, model.V, within=Binary) # variable tau (availability employee working at time i,j )
model.delta = Var(model.S, model.D, within=NonNegativeReals, default=0.0) # variable (amount of delay at time i,j ) 



# Constraints

def const1_rule(model, v):
    return sum(sum(model.tau[i,j,v] for i in model.S) for j in model.D ) == 160- model.theta1
model.const1_rule = Constraint(model.V, rule=const1_rule)

def const2_rule(model,j,v):
    return sum(model.alpha[i,j,v] for i in model.S) == 1
model.const2_rule = Constraint(model.D, model.V, rule = const2_rule)

def const3_rule(model,j,v):
    return sum(model.beta[i,j,v] for i in model.S) == 1
model.const3_rule = Constraint(model.D, model.V, rule = const3_rule)

def const4_rule(model,i,j,v):
    if i != model.theta_1 and i != model.theta_2:
        return model.alpha[i,j,v] == 0
model.const4_rule = Constraint(model.S, model.D, model.V,  rule = const3_rule)

def const5_rule(model,i,j,v):
    return model.tao[i,j,v] <= sum(model.alpha[k,j,v] for k in range(i+1) )
model.const5_rule = Constratint(model.S, model.D, model.V, rule = const5_rule)

def const6_rule(model,i,j,v):
	return model.tao[i,j,v] <= 1- sum(model.beta[k,j,v] for k in range(i+1) )
model.const6_rule = Constratint(model.S, model.D, model.V, rule=const6_rule)

def const7_rule(model,i,j):
	return sum( model.c[k] * model.w[i,j,k] for k in model.T ) <= sum( model.tao[i,j,k] for k in model.V ) + model.delta[i,j]
model.const7_rule = Constratint(model.S, model.D, rule = const7_rule)


# pyomo solve --solver=glpk 02Model_Pyomo.py model2.dat
