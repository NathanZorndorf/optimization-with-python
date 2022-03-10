import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

range_i = range(1, 6)

# Variables
model.x = pyo.Var(range_i, bounds=(0, None), within=pyo.Integers)
x = model.x

model.y = pyo.Var(bounds=(0, None))
y = model.y

# Constraints
def cond1(model):
    sum1 = sum(model.x[i] for i in range_i)
    return(sum1 + model.y <= 20)
model.c1 = pyo.Constraint(rule=cond1)

model.c2 = pyo.ConstraintList()
for i in range_i:
    model.c2.add(x[i] + y >= 15)

def cond3(model):
    sum3 = sum(model.x[i]*i for i in range_i)
    return(sum3 >= 10)
model.c3 = pyo.Constraint(rule=cond3)

def cond4(model):
    return(model.x[5] + 2*model.y >= 30)
model.c4 = pyo.Constraint(rule=cond4)

# model.c5 = pyo.ConstraintList()
# for i in range_i:
#     model.c5.add(x[i] >= 0)
# model.c6 = pyo.Constraint(y >= 0)


# Objective
model.objective = pyo.Objective(
    sense=pyo.minimize,
    expr=sum([x[i] for i in range_i])+y
)

# Solve using GLPK
opt = pyo.SolverFactory('glpk')

# Save results
results = opt.solve(model)

# Print results
print(results)
model.pprint()
print('x = ', [pyo.value(x[i]) for i in range_i])
print('y = ', pyo.value(y))