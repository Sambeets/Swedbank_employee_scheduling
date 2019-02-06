
#
# Imports
#

from pyomo.environ import *

###################################
# Model Begins
###################################


model = AbstractModel("Swedbank Scheduling Tartu Uni 2019")

model.Ntime = Param() # number of time slots 
model.Nday = Param() # number of days
model.Ntask = Param() # number of Tasks 
model.n = Param() # number of employees

<<<<<<< HEAD
model.S = RangeSet(1,model.Ntime) # Set of time
model.D = RangeSet(1,model.Nday) # Set of day
model.T = RangeSet(1,model.Ntask) # Set of tasks 
model.V = RangeSet(1,model.n) # Set of employees
=======
model.S = RangeSet(model.Ntime) # Set of time
model.D = RangeSet(model.Nday) # Set of day
model.T = RangeSet(model.Ntask) # Set of tasks 
model.V = RangeSet(model.n) # Set of employees
>>>>>>> 43be84e576d11d7812899a9b311d46f0e545b9d8

# Parameters

model.c = Param(model.T, within= PositiveReals) # duration of tasks of type k 
model.a = Param(model.S, model.D, within= PositiveReals) # delay proirities
model.w = Param(model.S, model.D, model.T, within= PositiveReals) # number of tasks (type k) received at time (i,j)
<<<<<<< HEAD
model.theta0 = Param(within= PositiveReals) # preparation time 
model.theta1 = Param(within= PositiveReals) # starting time of batch 1
model.theta2 = Param(within= PositiveReals) # starting time of batch 2
model.theta3 = Param(within= PositiveReals) # the slot index of the starting time of the lunch break
model.theta4 = Param(within= PositiveReals) # the slot index of the ending time of the lunch break
model.theta5 = Param(within= PositiveReals) # the duration of the lunchtime
model.Maxtime = Param(within=PositiveReals)
model.Mintime = Param(within=PositiveReals)
=======
model.theta0 = Param() # preparation time 
model.theta1 = Param() # starting time of batch 1
model.theta2 = Param() # starting time of batch 2
model.theta3 = Param() # the slot index of the starting time of the lunch break
model.theta4 = Param() # the slot index of the ending time of the lunch break
model.theta5 = Param() # the duration of the lunchtime
>>>>>>> 43be84e576d11d7812899a9b311d46f0e545b9d8

# Variables
model.alpha = Var(model.S, model.D, model.V, within=Binary) # variable alpha (whether i,j is the starting time of employes v)
model.beta = Var(model.S, model.D, model.V, within=Binary) # variable beta (whether i,j is the ending time of employees v)
model.tau = Var(model.S, model.D, model.V, within=Binary) # variable tau (availability employee working at time i,j )
model.delta = Var(model.S, model.D, within=NonNegativeReals) # variable (amount of delay at time i,j ) 


# =============================================================================
# # Constraints
# 
<<<<<<< HEAD

def const11_rule(model, v):
    return sum(model.tau[i,j,v] for i in model.S for j in model.D ) <= model.Maxtime - model.theta1
model.const11 = Constraint(model.V, rule=const11_rule)
=======
def const1_rule(model, v):
    return sum(model.tau[i,j,v] for i in model.S for j in model.D ) == 160- model.theta1
model.const1 = Constraint(model.V, rule=const1_rule)
# 

def const2_rule(model,j,v):
    return sum(model.alpha[i,j,v] for i in model.S) == 1
model.const2 = Constraint(model.D, model.V, rule = const2_rule)
# 
>>>>>>> 43be84e576d11d7812899a9b311d46f0e545b9d8

def const3_rule(model,j,v):
    return sum(model.beta[i,j,v] for i in model.S) == 1
model.const3 = Constraint(model.D, model.V, rule = const3_rule)

<<<<<<< HEAD
def const12_rule(model, v):
    return sum(model.tau[i,j,v] for i in model.S for j in model.D ) >= model.Mintime - model.theta1
model.const12 = Constraint(model.V, rule=const12_rule)

# 

def const2_rule(model,j,v):
    return sum(model.alpha[i,j,v] for i in model.S) == 1
model.const2 = Constraint(model.D, model.V, rule = const2_rule)
# 

def const3_rule(model,j,v):
    return sum(model.beta[i,j,v] for i in model.S) == 1
model.const3 = Constraint(model.D, model.V, rule = const3_rule)

# 
def const4_rule(model,i,j,v):
    if i != model.theta1 and i != model.theta2:
        return model.alpha[i,j,v] == 0
    else:
        return model.alpha[i,j,v] >= 0
model.const4 = Constraint(model.S, model.D, model.V,  rule = const4_rule)
# 

def const5_rule(model,i,j,v):
    val5 = sum(model.alpha[k,j,v] for k in range(1,i+1) )
    return model.tau[i,j,v] <= val5
model.const5 = Constraint(model.S, model.D, model.V, rule = const5_rule)
# 

def const6_rule(model,i,j,v):
    val6 = 1 - sum(model.beta[k,j,v] for k in range(1,i) )
    return model.tau[i,j,v] <= val6
model.const6 = Constraint(model.S, model.D, model.V, rule=const6_rule)
# 

def const7_rule(model,i,j):
    return sum( model.c[k] * model.w[i,j,k] for k in model.T ) <= sum( model.tau[i,j,k] for k in model.V ) + model.delta[i,j]
model.const7 = Constraint(model.S, model.D, rule = const7_rule)


'''
# Lunch time
def const8_rule(model,j):
    lhs_sum = 0
    rhs_sum = 0
    for i in model.S:
        if i >= model.theta3 or i <= model.theta4:
            lhs_sum += sum(model.c[k] * model.w[i,j,k] for k in model.T)
            rhs_sum += sum( model.tau[i,j,k] for k in model.V)
        #^ if
    #^ for
    return lhs_sum <= rhs_sum + model.delta[i,j]- model.n * model.theta5
model.const8 = Constraint(model.D, rule = const8_rule)
'''
#
=======
# 

def const4_rule(model,i,j,v):
    if i != model.theta1 and i != model.theta2:
        return model.alpha[i,j,v] == 0
    else:
        return Constraint.Skip #Infeasible
model.const4 = Constraint(model.S, model.D, model.V,  rule = const4_rule)
# 

def const5_rule(model,i,j,v):
    val5 = sum(model.alpha[k,j,v] for k in range(1,i+1) )
    return model.tau[i,j,v] <= val5
model.const5 = Constraint(model.S, model.D, model.V, rule = const5_rule)
# 

def const6_rule(model,i,j,v):
    val6 = sum(model.beta[k,j,v] for k in range(1,i+1) )
    return model.tau[i,j,v] <= val6
model.const6 = Constraint(model.S, model.D, model.V, rule=const6_rule)
# 

def const7_rule(model,i,j):
	return sum( model.c[k] * model.w[i,j,k] for k in model.T ) <= sum( model.tau[i,j,k] for k in model.V ) + model.delta[i,j] )
model.const7 = Constraint(model.S, model.D, rule = const7_rule)
#

def const8_rule(model,j):
    lhs_sum = 0
    rhs_sum = 0
    if i >= model.theta3 or i <= model.theta4:
        lhs_sum += sum(model.c[k] * model.w[i,j,k] for k in model.T)
    if i >= model.theta3 or i <= model.theta4:
        rhs_sum += sum( model.tao[i,j,k] for k in model.V)
    
    return lhs_sum <= rhs_sum + model.delta[i,j]- model.n * model.theta5
model.const8 = Constraint(model.D, rule = const8_rule)
#


>>>>>>> 43be84e576d11d7812899a9b311d46f0e545b9d8

def objective_rule(model):
    return sum(model.a[i,j] * model.delta[i,j] for i in model.S for j in model.D)
model.objective = Objective(rule=objective_rule, sense=minimize)
<<<<<<< HEAD
'''
opt = SolverFactory('cplex')
instance = model.create_instance("data2.dat") # data.dat contains all data | data2.dat conntains data without w[i,j,k]
results = opt.solve(instance) # solves and updates instance
instance.load(results)
results.write()
#instance.display()

#model.pprint()
'''
=======

opt = SolverFactory('glpk')
instance = model.create_instance("data2.dat") # data.dat contains all data | data2.dat conntains data without w[i,j,k]
results = opt.solve(instance) # solves and updates instance
instance.display()
>>>>>>> 43be84e576d11d7812899a9b311d46f0e545b9d8

# 
# 
# # pyomo solve --solver=glpk Swedbank_Problem.py data2.dat
# 
# =============================================================================
