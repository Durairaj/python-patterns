import numpy as np
import scipy.stats as st

def black_scholes(S, K, T, r, sigma, option_type):
    """Calculate the fair price of a European call or put option using the Black-Scholes model."""
    # Calculate the d1 and d2 terms
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # Calculate the fair price of the option
    if option_type == 'call':
        price = S * st.norm.cdf(d1) - K * np.exp(-r * T) * st.norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * st.norm.cdf(-d2) - S * st.norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type")
    return price

# Test the function
S = 100  # Underlying asset price
K = 105  # Strike price
T = 1  # Time to expiration (in years)
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility
option_type = 'call'  # 'call' or 'put'
price = black_scholes(S, K, T, r, sigma, option_type)
print(f'Option price: {price:.2f}')
