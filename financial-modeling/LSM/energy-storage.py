import numpy as np

# Simulate paths for the underlying factors using Monte Carlo simulation
def simulate_factors(num_paths, num_steps, factor_distributions):
    paths = np.zeros((num_steps + 1, num_paths, len(factor_distributions)))
    for i, (name, distribution) in enumerate(factor_distributions.items()):
        paths[:, :, i] = distribution.rvs(size=(num_steps + 1, num_paths))
    return paths

# Calculate the revenue of the storage system at each time step based on the simulated values of the underlying factors
def calc_revenue(paths, storage_params):
    revenue = np.zeros((paths.shape[0], paths.shape[1]))
    for t in range(1, paths.shape[0]):
        revenue[t] = storage_params['charging_rate'] * paths[t, :, 0] * storage_params['capacity']
        revenue[t] -= storage_params['discharging_rate'] * paths[t, :, 1] * storage_params['capacity']
    return revenue

# Estimate the expected future revenue using least squares regression
def expected_future_revenue(X, Y):
    beta = np.linalg.lstsq(X, Y, rcond=None)[0]
    return X @ beta

# Value an energy storage system using the LMS method
def value_storage_system(storage_params, factor_distributions, discount_rate, num_paths, num_steps):
    # Simulate paths for the underlying factors
    paths = simulate_factors(num_paths, num_steps, factor_distributions)
    # Calculate the revenue of the storage system at each time step
    revenue = calc_revenue(paths, storage_params)
    # Initialize the present value of the expected future revenue to the revenue at the final time step
    present_value = np.exp(-discount_rate * storage_params['lifetime']) * revenue[-1]
    # Loop backwards through time
    dt = storage_params['lifetime'] / num_steps
    for t in range(num_steps - 1, 0, -1):
        # Calculate the present value of the expected future revenue at time t
        X = paths[t]
        Y = present_value * np.exp(-discount_rate * dt)
        # Use least squares regression to estimate the expected future revenue
        efr = expected_future_revenue(X, Y)
        # Update the present value of the expected future revenue
        present_value = efr * np.exp(-discount_rate * dt) + revenue[t] * np.exp(-discount_rate * dt)
    # Return the average present value of the expected future revenue as the final estimate of the storage system value
    return np.mean(present_value)

# Test the function
storage_params = {
    'capacity': 100,   # Storage capacity (MWh)
    'charging_rate': 10,  # Charging rate (MW)
    'discharging
