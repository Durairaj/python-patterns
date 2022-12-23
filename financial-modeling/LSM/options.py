import numpy as np

# Simulate asset paths using a geometric Brownian motion model
def simulate_asset_paths(S0, r, sigma, T, M, I):
    dt = T / M
    paths = np.zeros((M + 1, I))
    paths[0] = S0
    for t in range(1, M + 1):
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.standard_normal(I))
    return paths

# Calculate the exercise value of a European call option at time t
def exercise_value(S, K):
    return np.maximum(S - K, 0)

# Estimate the expected continuation value using least squares regression
def expected_continuation_value(X, Y):
    beta = np.linalg.lstsq(X, Y, rcond=None)[0]
    return X @ beta

# Price a European call option using the LSM method
def price_call_option(S0, K, r, sigma, T, M, I):
    # Simulate asset paths
    paths = simulate_asset_paths(S0, r, sigma, T, M, I)
    # Initialize option values to the exercise values at maturity
    V = exercise_value(paths[-1], K)
    # Loop backwards through time
    for t in range(M - 1, 0, -1):
        # Calculate the exercise value at time t
        X = paths[t]
        Y = V * np.exp(-r * dt)
        # Use least squares regression to estimate the ECV
        ecv = expected_continuation_value(X, Y)
        # Select paths for which the exercise value is greater than the ECV
        mask = exercise_value(X, K) > ecv
        # Set the option value for these paths to the exercise value
        V[mask] = exercise_value(X[mask], K)
        # Set the option value for the remaining paths to the ECV
        V[~mask] = ecv[~mask] * np.exp(-r * dt)
    # Calculate the average option value over all paths as the final estimate of the option price
    return np.mean(V) * np.exp(-r * T)

# Test the function
S0 = 100  # Initial asset price
K = 105   # Strike price
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility
T = 1     # Time to maturity (in years)
M = 50    # Number of time steps
I = 10000 # Number of paths
call_price = price_call_option(S0, K, r, sigma, T, M, I)
print(f'Price of European call option: {call_price:.2f}')
