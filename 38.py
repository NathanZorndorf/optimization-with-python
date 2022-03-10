from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x = solver.NumVar(None, 3, 'x')
y = solver.NumVar(0, None, 'y')

solver.Add(-x + 2*y <= 8)
solver.Add(2*x + y <= 14)
solver.Add(2*x - y <= 10)

solver.Maximize(x+y)

results = solver.Solve()

print('x:', x.solution_value())
print('y', y.solution_value())
