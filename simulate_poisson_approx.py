"""
Simulate Bernoulli approximation of a Poisson process on [0,T].
Divide [0,T] into n equal subintervals and in each generate an event with prob p = lambda_/n.
Repeat many times, collect counts and interarrival times, compare with Poisson(lambda_ * T) and Exponential(1/lambda_).
Saves optional plots if matplotlib is available.
"""
import numpy as np
import math
import json
import os

# PARAMETERS
T = 1.0          # total time interval
lam = 3.5        # rate parameter lambda (events per unit time)
n = 5000         # number of subintervals per trial
p = lam * T / n  # success prob per subinterval
trials = 20000   # number of repeated experiments to collect counts
seed = 12345

np.random.seed(seed)

# Simulation: counts
counts = np.random.binomial(n, p, size=trials)

# approximate event times for a single long simulation to inspect interarrival times
# generate one long realization by sampling Bernoullis across n subintervals and placing events uniformly within each subinterval
bernoulli = np.random.rand(n) < p
indices = np.nonzero(bernoulli)[0]
# if there are events, place them uniformly within their subinterval
if len(indices) > 0:
    times = (indices + np.random.rand(len(indices))) * (T / n)
    times.sort()
    interarrivals = np.diff(np.concatenate(([0.0], times)))  # time from 0 to first, then between events
else:
    times = np.array([])
    interarrivals = np.array([])

# Summary statistics
mean_count = counts.mean()
var_count = counts.var(ddof=0)

# Theoretical Poisson(lambda*T)
theor_mean = lam * T
theor_var = lam * T

# Interarrival empirical stats (if available)
if interarrivals.size > 0:
    mean_ia = interarrivals.mean()
    var_ia = interarrivals.var(ddof=0)
else:
    mean_ia = None
    var_ia = None

# Print summary
print("Poisson-approximation simulation summary")
print(f"Parameters: T={T}, lambda={lam}, n={n}, p=lambda*T/n={p:.6g}, trials={trials}")
print()
print("Counts over trials:")
print(f" empirical mean = {mean_count:.6f}")
print(f" empirical var  = {var_count:.6f}")
print(" theoretical (Poisson) mean = var = lambda * T = {:.6f}".format(theor_mean))
print()
print("Interpretation: As n -> infinity with p=lambda*T/n, the Binomial(n,p) count per interval converges in distribution to Poisson(lambda*T).")
print()
if interarrivals.size > 0:
    print("Interarrival times from one realization (approx):")
    print(f" number of events in realization = {len(times)}")
    print(f" empirical mean interarrival (including time from 0 to first) = {mean_ia:.6f}")
    print(f" empirical var interarrival = {var_ia:.6f}")
    print(" theoretical Exponential mean = 1/lambda = {:.6f}".format(1.0/lam))
    print()
    print("Note: exponential interarrival distribution arises in the limit as n->infty; here we used uniform placement within subintervals to approximate continuous-time events.")
else:
    print("No events in the single realization used for interarrival inspection.")

# Save a small JSON summary
out = {
    'T': T,
    'lambda': lam,
    'n': n,
    'p': p,
    'trials': trials,
    'counts_mean': float(mean_count),
    'counts_var': float(var_count),
    'theor_mean': float(theor_mean),
    'theor_var': float(theor_var),
    'realization_event_count': int(len(times)),
}
with open('poisson_approx_summary.json', 'w') as f:
    json.dump(out, f, indent=2)

# Optional plotting if matplotlib available
try:
    import matplotlib.pyplot as plt
    from scipy.stats import poisson, expon

    # Counts histogram vs Poisson pmf
    max_k = max(0, int(max(counts.max(), math.ceil(theor_mean + 4*math.sqrt(theor_var)))))
    vals, bins, _ = plt.hist(counts, bins=range(0, max_k+2), density=True, alpha=0.6, label='empirical')
    ks = np.arange(0, max_k+1)
    pmf = poisson.pmf(ks, theor_mean)
    plt.plot(ks, pmf, 'o-', label=f'Poisson({theor_mean:.2f})')
    plt.xlabel('Count per T')
    plt.ylabel('Probability')
    plt.title('Counts: empirical vs Poisson PMF')
    plt.legend()
    plt.grid(True)
    plt.savefig('counts_vs_poisson.png')
    plt.close()

    if interarrivals.size > 0:
        # Empirical interarrival histogram vs Exp
        plt.hist(interarrivals, bins=50, density=True, alpha=0.6, label='empirical interarrivals')
        xs = np.linspace(0, max(interarrivals.max(), 5.0/lam), 200)
        plt.plot(xs, expon.pdf(xs, scale=1.0/lam), 'r-', label=f'Exponential(mean={1.0/lam:.2f})')
        plt.xlabel('Interarrival time')
        plt.ylabel('Density')
        plt.title('Interarrival times: empirical vs exponential')
        plt.legend()
        plt.grid(True)
        plt.savefig('interarrivals_vs_exponential.png')
        plt.close()

    print('Saved plots: counts_vs_poisson.png, interarrivals_vs_exponential.png')
except Exception as e:
    print('matplotlib or scipy not available, skipped plotting. Exception:', str(e))

# End
print('\nSaved summary to poisson_approx_summary.json')
