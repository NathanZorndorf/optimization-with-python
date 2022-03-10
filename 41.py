import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

Ng = 5

# Variables
model.Pg = pyo.Var(range(Ng), bounds=(0, None), within=pyo.Reals)
Pg = model.Pg

# Parameters
model.Pd = [50, 20, 30]
Pd = model.Pd
model.GenLimits = [20, 10, 40, 50, 5]
model.Cg = [.10, .05, .30, .40, .01]
Cg = model.Cg

# Constraints
## COnstraint 1
pg_sum = sum(Pg[i] for i in range(Ng)) # structure for variables
pd_sum = sum(Pd) # structure for parameters
model.balance = pyo.Constraint(expr= pg_sum == pd_sum)

## Constraint 2
def cond(model):
    return(model.Pg[0] + model.Pg[3] >= model.Pd[0])
model.cond = pyo.Constraint(rule=cond)

## Constraint 3
model.limits = pyo.ConstraintList()
for i in range(Ng):
    model.limits.add(Pg[i] <= model.GenLimits[i])

# Objective function
model.obj = pyo.Objective(
    sense=pyo.minimize, 
    expr=sum([Cg[i] * Pg[i] for i in range(Ng)])
)

# Solve using GLPK
opt = pyo.SolverFactory('glpk')

# Save results
results = opt.solve(model)

# Print results
print(results)

print('Pg = ', [pyo.value(Pg[i]) for i in range(Ng)])

model.pprint()
