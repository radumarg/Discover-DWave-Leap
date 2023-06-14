from dimod import ConstrainedQuadraticModel, Binary, quicksum
from dwave.system import LeapHybridCQMSampler
import random
import numpy as np

# Problem setup
num_packages = 300

# Priority for each package, 3 = high_priority, 1 = low_priority
priority = [random.choice([1,2,3]) for i in range(num_packages)]

# Number of days since each package was ordered (More days need to be priorited higher)
days_since_order = [random.choice([0,1,2,3]) for i in range(num_packages)]

# Weight for each package
cost = [random.randint(1, 100) for i in range(num_packages)]

# Maximum weight and number of packges a trick can handle
max_weight = 300
max_parcels = 100

# Weights for the objective function
obj_weight_priority = 1
obj_weight_days = 1

num_items = len(cost)

# Build the CQM
cqm = ConstrainedQuadraticModel()

# Create binary variables
bin_variables = [Binary(i) for i in range(num_items)]

# ------------------------ Objective functions -------------------------------
# 1. Maximize priority shipping packages
objective1 = -obj_weight_priority * quicksum(priority[i] * bin_variables[i] for i in range(num_items))

# 2. Minimize customer wait time
objective2 = -obj_weight_days * quicksum(days_since_order[i] * bin_variables[i] for i in range(num_items))

# Add the objective to the CQM
cqm.set_objective(objective1 + objective2)

# ------------------------------- Constraints ----------------------------------
# Add the maximum capacity constraint
cqm.add_constraint(quicksum(cost[i] * bin_variables[i] for i in range(num_items)) <= max_weight, label='max_weight')

# Add the maximum trick capacity constraint
cqm.add_constraint(quicksum(bin_variables[i] for i in range(num_items)) <= max_parcels, label='max_parcels')

# ----------------------- Submit to the CQM solver ----------------------------------
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, time_limit = 5, label='Truck Packing Demo')
print(sampleset.info)

# ----------------------- Process the results  ----------------------------------
feasible_sols = np.where(sampleset.record.is_feasible == True)

if len(feasible_sols[0]):
    first_feasible_sol = np.where(sampleset.record[feasible_sols[0][0]][0] == 1)
    print(first_feasible_sol)

# # get the first feasible solution
# frst = next(itertools.filterfalse(
#     lambda d: not getattr(d, 'is_feasible'), list(sampleset.data())
#     ))