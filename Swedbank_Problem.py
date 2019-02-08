from pyomo.environ import *
import xlwt
from random import randint
import scipy.io


def prepare_data(input_file, output_file, team, theta, nV):
    nT = 6  # number of types of tasks
    nW = 4 # number of weeks
    if team == 3:
        nS = 18 # number of time slots per day 
        nD = 7  # number of days per week
        core_prepare_data(input_file, output_file, team, theta, nV, nS, nD, nT, nW)
    #^ if
    if team ==1 or team == 2:
        nS = 10
        nD = 5
        core_prepare_data(input_file, output_file, team, theta, nV, nS, nD, nT, nW)
    #^if 
def core_prepare_data(input_file, output_file, team, theta, nV, nS, nD, nT, nW):
    mat = scipy.io.loadmat(input_file)
    f = open(output_file, 'w+t')
    D = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # writing the number of time slots per day 
    f.write("param s := "+str(nS)+";\n")

    # writing the number of days per week   
    f.write("param d := "+str(nD*nW)+";\n")
    
    # writing the number of types of tasks
    f.write("param t := "+str(nT)+";\n")

    # writing the number of employees
    f.write("param n := "+str(nV)+";\n") 

    # writing the costs of each type  
    f.write("param c := 1 0.016 2 0.083 3 0.16 4 0.25 5 0.3 6 0.5;\n")

    # writing the
    f.write("param theta0 := "+str(theta[0])+";\n")

    # writing the
    f.write("param theta1 := "+str(theta[1])+";\n")
    
    # writing the
    f.write("param theta2 := "+str(theta[2])+";\n")

    # writing the
    f.write("param theta3 := "+str(theta[3])+";\n")
        
    # writing the
    f.write("param theta4 := "+str(theta[4])+";\n")
        
    # writing the
    f.write("param theta5 := "+str(theta[5])+";\n")

    # writing the
    f.write("param theta6 := "+str(theta[6])+";\n")

    # writing the
    f.write("param theta7 := "+str(theta[7])+";\n") 

    # writing the priority delays
    f.write("param a :=\n")
    for i in range(nS):
        if team == 3:
            f.write("("+str(i+1)+",*) 1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1 21 1 22 1 23 1 24 1 25 1 26 1 27 1 28 1\n")
        #^ if 
        if team == 1 or team == 2:
            f.write("("+str(i+1)+",*) 1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1 11 1 12 1 13 1 14 1 15 1 16 1 17 1 18 1 19 1 20 1\n")
    #^ for
    f.write(";\n")
    # writing down the w_{i,j,k} tensor
    f.write("param w :=\n")
    for i in range(nS):
        for j in range(nW):
            slot = (i % 18) + 1
            day_idx = i + nS*j
            # Fix the days using the list
            f.write("("+str(slot)+","+str(1 + nD*j)+",*) 1 "+str(mat['Monday'][day_idx,0])+" 2 "+str(mat['Monday'][day_idx,1])+" 3 "+str(mat['Monday'][day_idx,2])+" 4 "+str(mat['Monday'][day_idx,3])+" 5 "+str(mat['Monday'][day_idx,4])+" 6 "+str(mat['Monday'][day_idx,5])+"\n" )
            f.write("("+str(slot)+","+str(2 + nD*j)+",*) 1 "+str(mat['Tuesday'][day_idx,0])+" 2 "+str(mat['Tuesday'][day_idx,1])+" 3 "+str(mat['Tuesday'][day_idx,2])+" 4 "+str(mat['Tuesday'][day_idx,3])+" 5 "+str(mat['Tuesday'][day_idx,4])+" 6 "+str(mat['Tuesday'][day_idx,5])+"\n" )
            f.write("("+str(slot)+","+str(3 + nD*j)+",*) 1 "+str(mat['Wednesday'][day_idx,0])+" 2 "+str(mat['Wednesday'][day_idx,1])+" 3 "+str(mat['Wednesday'][day_idx,2])+" 4 "+str(mat['Wednesday'][day_idx,3])+" 5 "+str(mat['Wednesday'][day_idx,4])+" 6 "+str(mat['Wednesday'][day_idx,5])+"\n" )
            f.write("("+str(slot)+","+str(4 + nD*j)+",*) 1 "+str(mat['Thursday'][day_idx,0])+" 2 "+str(mat['Thursday'][day_idx,1])+" 3 "+str(mat['Thursday'][day_idx,2])+" 4 "+str(mat['Thursday'][day_idx,3])+" 5 "+str(mat['Thursday'][day_idx,4])+" 6 "+str(mat['Thursday'][day_idx,5])+"\n" )
            f.write("("+str(slot)+","+str(5 + nD*j)+",*) 1 "+str(mat['Friday'][day_idx,0])+" 2 "+str(mat['Friday'][day_idx,1])+" 3 "+str(mat['Friday'][day_idx,2])+" 4 "+str(mat['Friday'][day_idx,3])+" 5 "+str(mat['Friday'][day_idx,4])+" 6 "+str(mat['Friday'][day_idx,5])+"\n" )
            if team == 3:
                f.write("("+str(slot)+","+str(6 + nD*j)+",*) 1 "+str(mat['Saturday'][day_idx,0])+" 2 "+str(mat['Saturday'][day_idx,1])+" 3 "+str(mat['Saturday'][day_idx,2])+" 4 "+str(mat['Saturday'][day_idx,3])+" 5 "+str(mat['Saturday'][day_idx,4])+" 6 "+str(mat['Saturday'][day_idx,5])+"\n" )
            if team == 3:
                f.write("("+str(slot)+","+str(6 + nD*j)+",*) 1 "+str(mat['Saturday'][day_idx_s,0])+" 2 "+str(mat['Saturday'][day_idx_s,1])+" 3 "+str(mat['Saturday'][day_idx_s,2])+" 4 "+str(mat['Saturday'][day_idx_s,3])+" 5 "+str(mat['Saturday'][day_idx_s,4])+" 6 "+str(mat['Saturday'][day_idx_s,5])+"\n" )

                f.write("("+str(slot)+","+str(7 + nD*j)+",*) 1 "+str(mat['Sunday'][day_idx,0])+" 2 "+str(mat['Sunday'][day_idx,1])+" 3 "+str(mat['Sunday'][day_idx,2])+" 4 "+str(mat['Sunday'][day_idx,3])+" 5 "+str(mat['Sunday'][day_idx,4])+" 6 "+str(mat['Sunday'][day_idx,5])+"\n" )
        #^ for
    #^ for
    f.write(";")
    return 0 
#^ core_prepare_data()

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
        return sum(i*( model.beta[i,j,v] - model.alpha[i,j,v] )  for i in model.S for j in model.D) + len(model.D) <= model.theta0 - model.theta2
    model.const0 = Constraint(model.V, rule=const0_rule)

    # Employees minimum working hours 
    def const1_rule(model, v):
        return sum( i*( model.beta[i,j,v] - model.alpha[i,j,v] ) for i in model.S for j in model.D) + len(model.D) >= model.theta1 - model.theta2
    model.const1 = Constraint(model.V, rule=const1_rule)

    # 

    # Starting time of each Employee
    def const2_rule(model, j, v):
        return sum(model.alpha[i,j,v] for i in model.S) == 1
    model.const2 = Constraint(model.D, model.V, rule = const2_rule)
    # 

    # End time of each Employee
    def const3_rule(model,j,v):
        return sum(model.beta[i,j,v] for i in model.S) == 1
    model.const3 = Constraint(model.D, model.V, rule = const3_rule)

    #

    # Start time is less than End time
    # def const4_rule(model,i,j,v):
    #     if i <= model.theta3 or i <= model.theta4:
    #         return model.beta[i,j,v] == 0
    #     else:
    #         return model.beta[i,j,v] >= 0
    def const4_rule(model,j,v):
        return sum ( i*( model.beta[i,j,v] - model.alpha[i,j,v]) for i in model.S) >= -1

    model.const4 = Constraint(model.D, model.V, rule = const4_rule)

    # Employees arrive in different batches
    def const5_rule(model,i,j,v):
        if i != model.theta3 and i != model.theta4:
            return model.alpha[i,j,v] == 0
        else:
            return model.alpha[i,j,v] >=0
    model.const5 = Constraint(model.S, model.D, model.V,  rule = const5_rule)
    # 

    # Tasks are not assigned to Employees who didn't arrive 
    def const6_rule(model,i,j,v):
        val5 = sum(model.alpha[k,j,v] for k in range(1,i+1) )
        return model.tau[i,j,v] <= val5
    model.const6 = Constraint(model.S, model.D, model.V, rule = const6_rule)
    # 

    # Tasks are not assigned to Employees after leaving work
    def const7_rule(model,i,j,v):
        val6 = 1 - sum(model.beta[k,j,v] for k in range(1,i) )
        return model.tau[i,j,v] <= val6
    model.const7 = Constraint(model.S, model.D, model.V, rule=const7_rule)
    # 

    # Counts the delays due to working load 
    def const8_rule(model,i,j):
        return sum( model.c[k] * model.w[i,j,k] for k in model.T ) <= sum( model.tau[i,j,k] for k in model.V ) + model.delta[i,j]
    model.const8 = Constraint(model.S, model.D, rule = const8_rule)


    # Takes Lunch time into consideration
    def const9_rule(model,j):
        lhs_sum = 0
        rhs_sum = 0
        for i in model.S:
            if i >= model.theta5 or i <= model.theta6:
                lhs_sum += sum(model.c[k] * model.w[i,j,k] for k in model.T)
                rhs_sum += sum( model.tau[i,j,k] for k in model.V)
            #^ if
        #^ for
        return lhs_sum <= rhs_sum + model.delta[i,j]- model.theta7*model.n # Fix this!!!
    model.const9 = Constraint(model.D, rule = const9_rule)
    

    # Extra wroking time 
    def const10_rule(model,i,j):
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

    model.const10 = Constraint(model.S, model.D, rule = const10_rule)

    # Objective function: reduces the delays 
    def objective_rule(model):
        return sum(model.a[i,j] * model.delta[i,j] for i in model.S for j in model.D)
    model.objective = Objective(rule=objective_rule, sense=minimize)

#^ create model()

def solve(model, solver, data_file):
    opt = SolverFactory(solver)
    instance = model.create_instance(data_file)
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
    ws = wb.add_sheet('Time Table')

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
# WRap it in a function
def do_it(input_file, solver, team, params, number_employees):
    model = AbstractModel("Swedbank Scheduling Tartu Uni 2019")
    print("Starts to create the model")
    create_model(model)
    print("Finished creating the model")
    print("Starts to read input data")
    prepare_data(input_file+".mat", input_file+'.dat', team , params, number_employees)
    print("Finished reading the input data")
    print(" Starts to solve the model")
    instance, results = solve(model,'gurobi', input_file+'.dat')
    print(" Finished solving the model")
    instance.load(results)
    results.write()
    # instance.display()
    if results.solver.Message != 'Model was proven to be infeasible':
        print("Solution Found!")
        var_alpha, var_beta, var_tau, var_delta = retrieve_results(instance, results)
        write_to_excel(input_file+'_'+str(number_employees)+'.xls', instance, var_alpha, var_beta, var_tau, var_delta)
    else:
        print("Sorry no solution, please modify the parameters")
    #^ do_it()

# input_file = 'MonthMatrix_P_S1'
# solver = 'gurobi'
# team = 1
# params = [160, 80, 12, 1, 6, 4, 7, 0.5]
# number_employees = 10
# do_it(input_file, solver, team, params, number_employees)

