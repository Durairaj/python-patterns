import numpy as np

def present_value(cash_flows, discount_rate):
    """Calculate the present value of a series of cash flows using a discount rate."""
    return sum([cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows)])

def value_company(projected_cash_flows, discount_rate):
    """Value a company based on projected cash flows and a discount rate."""
    return present_value(projected_cash_flows, discount_rate)

# Test the function
projected_cash_flows = [100, 110, 120, 130, 140]  # Projected cash flows (in millions of dollars)
discount_rate = 0.1  # Discount rate
company_value = value_company(projected_cash_flows, discount_rate)
print(f'Company value: {company_value:.2f}')
