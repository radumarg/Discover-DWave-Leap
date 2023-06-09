import dimod

exact_solver = dimod.ExactSolver()
Q = { (0, 0): 1, (3, 3): 1, (0, 1): -2, (1, 2): 2, (2, 3): -2}

bqm = dimod.BinaryQuadraticModel.from_qubo(Q, offset= -2)
results = exact_solver.sample(bqm)

for sample, energy in results.data(['sample', 'energy']):
    print(sample, energy)