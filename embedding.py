from dwave.system.samplers import DWaveSampler
from dwave.system.composites import LazyFixedEmbeddingComposite

chainstrength = 4

Q = { (0, 0): 2, (0, 1): -2, (0, 2): -2, (1, 2): 2}

sampler = LazyFixedEmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q, chain_strength=chainstrength, num_reads=100)
print(sampler.properties['embedding'])

for sample, energy in response.data(['sample', 'energy']):
    print(sample, energy)