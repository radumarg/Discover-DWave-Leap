from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel

# setup scenario
pumps = [0, 1, 2, 3]
costs = [
    [36, 27],
    [56, 65],
    [48, 36],
    [52, 16],
]
flow = [2, 7, 3, 8]
demand = 20
time = [0, 1]

# build a variable for each pump
x = [[f'P{p}_AM', f'P{p}_PM'] for p in pumps]

# initialize BQM
bqm = BinaryQuadraticModel('BINARY')

# objective
for p in pumps:
    for t in time:
        bqm.add_variable(x[p][t], costs[p][t])

# constraint 1: each pump should run once per day
for p in pumps:
    c1 = [(x[p][t], 1) for t in time]
    bqm.add_linear_inequality_constraint(
        c1,
        lb = 1,
        ub = len(pumps),
        lagrange_multiplier = 5,
        label = 'c1_pump_' + str(p)
    )

# constraint 2: at most 3 pumps per timeslot
for t in time:
    c2 = [(x[p][t], 1) for p in pumps]
    bqm.add_linear_inequality_constraint(
        c2,
        constant = -3,
        ub = len(pumps),
        lagrange_multiplier = 1000,
        label = 'c2_time_' + str(t)
    )

# constraint 3: satisfy the daily demand
c3 = [(x[p][t], flow[p]) for t in time for p in pumps]
bqm.add_linear_equality_constraint(
    c3,
    constant = -demand,
    lagrange_multiplier = 28,
)

sampler = EmbeddingComposite(DWaveSampler())
sampleset = sampler.sample(bqm, num_reads = 100)

sample = sampleset.first.sample
total_flow = 0
total_cost = 0

print("\n\tAM\tPM")
for p in pumps:
    printout = 'P' + str(p)
    for time in range(2):
        printout += "\t" + str(sample[x[p][time]])
        total_flow += sample[x[p][time]] * flow[p]
        total_cost += sample[x[p][time]] * costs[p][time]
    print(printout)

print("\nTotal flow\t", total_flow)
print("\nTotal cost\t", total_cost, "\n")

print(bqm)