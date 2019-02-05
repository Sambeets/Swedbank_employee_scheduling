
#
# Imports
#
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
    return sum(sum(model.tao[i,j,v] for m in model.i) for n in model.j ) == 160- model.theta1
model.const1_rule = Constraint(model.i, model.j, rule=const1_rule)

def const2_rule(model,i):
    return sum(model.alpha[i,j,v] for n in model.i) == 1
model.const2_rule = Constraint(model.i, rule = const2_rule)

def const3_rule(model,i):
    return sum(model.beta[i,j,v] for n in model.i) == 1
model.const3_rule = Constraint(model.i, rule = const3_rule)



# pyomo solve --solver=glpk 02Model_Pyomo.py model2.dat
