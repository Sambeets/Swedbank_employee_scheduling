from pyomo.environ import *
import xlwt
from random import randint


def create_model(model):
    model.s = Param() # number of time slots 
    model.d = Param() # number of days
    model.t = Param() # number of Tasks 
    model.n = Param() # number of employees

    model.S = RangeSet(1,model.s) # Set of time
    model.D = RangeSet(1,model.d) # Set of day
    model.T = RangeSet(1,model.t) # Set of tasks 
    model.V = RangeSet(1,model.n) # Set of employees

    # Parameters

    model.c = Param(model.T, within= PositiveReals) # duration of tasks of type k 
    model.a = Param(model.S, model.D, within= PositiveReals) # delay proirities
    model.w = Param(model.S, model.D, model.T, within= PositiveReals) # number of tasks (type k) received at time (i,j)
    model.theta0 = Param(within=PositiveReals) # upper bound on the total working hours
    model.theta1 = Param(within=PositiveReals) # lower bound on the total working hours
    model.theta2 = Param(within= PositiveReals) # preparation time
    model.theta3 = Param(within= PositiveReals) # starting time of batch 1
    model.theta4 = Param(within= PositiveReals) # starting time of batch 2
    model.theta5 = Param(within= PositiveReals) # the slot index of the starting time of the lunch break
    model.theta6 = Param(within= PositiveReals) # the slot index of the ending time of the lunch break
    model.theta7 = Param(within= PositiveReals) # the duration of the lunchtime

    # Variables
    model.alpha = Var(model.S, model.D, model.V, within=Binary) # variable alpha (whether i,j is the starting time of employes v)
    model.beta = Var(model.S, model.D, model.V, within=Binary) # variable beta (whether i,j is the ending time of employees v)
    model.tau = Var(model.S, model.D, model.V, within=Binary) # variable tau (availability employee working at time i,j )
    model.delta = Var(model.S, model.D, within=NonNegativeReals) # variable (amount of delay at time i,j ) 


    # =============================================================================
    # # Constraints
    # 

    # Employees maximum working hours 
    def const0_rule(model, v):
        return sum(model.tau[i,j,v] for i in model.S for j in model.D ) <= model.theta0 - model.theta2
    model.const0 = Constraint(model.V, rule=const0_rule)

    # Employees minimum working hours 
    def const1_rule(model, v):
        return sum(model.tau[i,j,v] for i in model.S for j in model.D ) >= model.theta1 - model.theta2
    model.const1 = Constraint(model.V, rule=const1_rule)

    # 

    # Starting time of each Employee
    def const2_rule(model,j,v):
        return sum(model.alpha[i,j,v] for i in model.S) == 1
    model.const2 = Constraint(model.D, model.V, rule = const2_rule)
    # 

    # End time of each Employee
    def const3_rule(model,j,v):
        return sum(model.beta[i,j,v] for i in model.S) == 1
    model.const3 = Constraint(model.D, model.V, rule = const3_rule)

    #

    # Employees arrive in different batches
    def const4_rule(model,i,j,v):
        if i != model.theta3 and i != model.theta4:
            return model.alpha[i,j,v] == 0
        if i == model.theta3:
            return model.alpha[i,j,v] == randint(0,1)
        if i == model.theta4:
            return model.alpha[i,j,v] >= 0 
    model.const4 = Constraint(model.S, model.D, model.V,  rule = const4_rule)
    # 

    # Tasks are not assigned to Employees who didn't arrive 
    def const5_rule(model,i,j,v):
        val5 = sum(model.alpha[k,j,v] for k in range(1,i+1) )
        return model.tau[i,j,v] <= val5
    model.const5 = Constraint(model.S, model.D, model.V, rule = const5_rule)
    # 

    # Tasks are not assigned to Employees after leaving work
    def const6_rule(model,i,j,v):
        val6 = 1 - sum(model.beta[k,j,v] for k in range(1,i) )
        return model.tau[i,j,v] <= val6
    model.const6 = Constraint(model.S, model.D, model.V, rule=const6_rule)
    # 

    # Counts the delays due to working load 
    def const7_rule(model,i,j):
        return sum( model.c[k] * model.w[i,j,k] for k in model.T ) <= sum( model.tau[i,j,k] for k in model.V ) + model.delta[i,j]
    model.const7 = Constraint(model.S, model.D, rule = const7_rule)


    # Takes Lunch time into consideration
    def const8_rule(model,j):
        lhs_sum = 0
        rhs_sum = 0
        for i in model.S:
            if i >= model.theta5 or i <= model.theta6:
                lhs_sum += sum(model.c[k] * model.w[i,j,k] for k in model.T)
                rhs_sum += sum( model.tau[i,j,k] for k in model.V)
            #^ if
        #^ for
        return lhs_sum <= rhs_sum + model.delta[i,j]- model.n * model.theta7
    model.const8 = Constraint(model.D, rule = const8_rule)
    #

    # Extra wroking time 
    def const9_rule(model,i,j):
        lhs_sum = 0
        rhs_sum = 0
        for it in model.S:
            if it >= i:
                lhs_sum += sum(model.c[k] * model.w[i,j,k] for k in model.T)
                rhs_sum += sum( model.tau[i,j,k] for k in model.V )
            if it == len(model.S):
                rhs_sum += sum( model.tau[i,j,k] for k in model.V )
            #^ if
        #^ for
        return lhs_sum <= rhs_sum

    model.const9 = Constraint(model.S, model.D, rule = const9_rule)

    # Objective function: reduces the delays 
    def objective_rule(model):
        return sum(model.a[i,j] * model.delta[i,j] for i in model.S for j in model.D)
    model.objective = Objective(rule=objective_rule, sense=minimize)

#^ create model()

def solve(model):
    opt = SolverFactory('gurobi')
    instance = model.create_instance("data2.dat") # data.dat contains all data | data2.dat conntains data without w[i,j,k]
    results = opt.solve(instance) # solves and updates instance
    return instance, results
#^ solve()

def retrieve_results(instance, results):
    # Retrieving the results
    var_alpha = dict()
    var_beta = dict()
    var_tau = dict()
    var_delta = dict()
    instance.solutions.load_from(results)
    for var in instance.component_objects(Var, active=True):
        if str(var) == "alpha":
            varobject = getattr(instance, str(var))
            for index in varobject:
                var_alpha[index] = varobject[index].value
            #^ for
        #^ if
        if str(var) == "beta":
            varobject = getattr(instance, str(var))
            for index in varobject:
                var_beta[index] = varobject[index].value
            #^ for
        #^ if
        if str(var) == "tau":
            varobject = getattr(instance, str(var))
            for index in varobject:
                var_tau[index] = varobject[index].value
            #^ for
        #^ if
        if str(var) == "delta":
            varobject = getattr(instance, str(var))
            for index in varobject:
                var_delta[index] = varobject[index].value
            #^ for
        #^ if
    #^for
    return var_alpha, var_beta, var_tau, var_delta
#^ retrieve_results

def write_to_excel(file_name, instance, var_alpha, var_beta, var_tau, var_delta):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
                         num_format_str='#,##0.00')
    # style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')

    ws.write(0, 0, 'Employee', style0)
    ws.write(0, 1, 'Day', style0)
    ws.write(0, 2, 'Start Time', style0)
    ws.write(0, 3, 'End Time', style0)
    counter = 1
    for k in instance.V:
        for j in instance.D:
            for i in instance.S:
                if (i,j,k) in var_alpha.keys() and var_alpha[i,j,k] != 0:
                    ws.write(counter, 0, k)
                    ws.write(counter, 1, j)
                    ws.write(counter, 2, i)
                #^ if 
                if (i,j,k) in var_beta.keys() and var_beta[i,j,k] != 0:
                    ws.write(counter, 3, i)
                #^ if
            #^ for
            counter += 1
        #^ for
    #^ for
    wb.save(file_name)
#^ write_to_excel()

#===========
# Run It
#===========

model = AbstractModel("Swedbank Scheduling Tartu Uni 2019")
create_model(model)
instance, results = solve(model)

instance.load(results)
results.write()
# instance.display()
var_alpha, var_beta, var_tau, var_delta = retrieve_results(instance, results)
write_to_excel('example.xls', instance, var_alpha, var_beta, var_tau, var_delta)

# 
# 
# # pyomo solve --solver=glpk Swedbank_Problem.py data2.dat
# 
# =============================================================================
