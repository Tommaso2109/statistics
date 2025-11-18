"""
Pure-Python simulation of Bernoulli approximation to a Poisson process.
No external dependencies (uses random, math, json only).
"""
import random
import math
import json

# PARAMETERS
T = 1.0
lam = 3.5
n = 5000
p = lam * T / n
trials = 20000
seed = 12345

random.seed(seed)

# simulate counts
counts = []
for _ in range(trials):
    # do n Bernoulli trials, count successes
    c = 0
    # micro-optimization: localize
    r = random.random
    threshold = p
    for _ in range(n):
        if r() < threshold:
            c += 1
    counts.append(c)

# single realization for interarrival times
indices = []
r = random.random
for i in range(n):
    if r() < p:
        indices.append(i)

if indices:
    times = [ (i + random.random()) * (T/n) for i in indices ]
    times.sort()
    interarrivals = [times[0]] + [times[i] - times[i-1] for i in range(1, len(times))]
else:
    times = []
    interarrivals = []

# compute stats
mean_count = sum(counts) / len(counts)
var_count = sum((x-mean_count)**2 for x in counts) / len(counts)

# interarrival stats
if interarrivals:
    mean_ia = sum(interarrivals) / len(interarrivals)
    var_ia = sum((x-mean_ia)**2 for x in interarrivals) / len(interarrivals)
else:
    mean_ia = None
    var_ia = None

print('Poisson-approximation simulation summary (pure Python)')
print(f'Parameters: T={T}, lambda={lam}, n={n}, p=lambda*T/n={p:.6g}, trials={trials}')
print()
print('Counts over trials:')
print(f' empirical mean = {mean_count:.6f}')
print(f' empirical var  = {var_count:.6f}')
print(f' theoretical (Poisson) mean = var = lambda * T = {lam*T:.6f}')
print()
if interarrivals:
    print('Interarrival times from one realization (approx):')
    print(f' number of events in realization = {len(times)}')
    print(f' empirical mean interarrival (including time from 0 to first) = {mean_ia:.6f}')
    print(f' empirical var interarrival = {var_ia:.6f}')
    print(f' theoretical Exponential mean = 1/lambda = {1.0/lam:.6f}')
else:
    print('No events in the single realization used for interarrival inspection.')

out = {
    'T': T,
    'lambda': lam,
    'n': n,
    'p': p,
    'trials': trials,
    'counts_mean': mean_count,
    'counts_var': var_count,
    'theor_mean': lam*T,
    'theor_var': lam*T,
    'realization_event_count': len(times),
}
with open('poisson_approx_summary_purepy.json','w') as f:
    json.dump(out, f, indent=2)

print('\nSaved summary to poisson_approx_summary_purepy.json')
