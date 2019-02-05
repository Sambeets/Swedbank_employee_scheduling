
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
model.c = Param(model.k, within= PositiveReals)
model.a = Param(model.i, model.j, within= PositiveReals)
model.w = Param(model.i, model.j, model.k, within= PositiveReals)
model.theta0 = Param()
model.theta1 = Param()
model.theta2 = Param()

# Variables
model.alpha = Var(model.i, model.j, model.v, within=Binary) # variable alpha
model.beta = Var(model.i, model.j, model.v, within=Binary) # variable beta
model.tau = Var(model.i, model.j, model.v, within=Binary) # variable tau
model.delta = Var(model.i, model.j, within=NonNegativeReals, default=0.0) # variable



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
        #^ for v
    #^ for j
#^ for i 

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
