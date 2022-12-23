import numpy as np

def present_value(cash_flows, discount_rate):
    """Calculate the present value of a series of cash flows using a discount rate."""
    return sum([cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows)])

def value_company(projected_cash_flows, discount_rate, growth_rates):
    """Value a company based on projected cash flows and a discount rate, with multiple stages of growth."""
    # Calculate the present value of the cash flows in each growth stage
    present_values = []
    for i, cash_flows in enumerate(projected_cash_flows):
        growth_rate = growth_rates[i]
        # Apply the growth rate to the cash flows in the next stage
        if i < len(projected_cash_flows) - 1:
            projected_cash_flows[i + 1] = [cf * (1 + growth_rate) for cf in projected_cash_flows[i + 1]]
        present_values.append(present_value(cash_flows, discount_rate))
    # Return the sum of the present values as the estimated value of the company
    return sum(present_values)

# Test the function
projected_cash_flows = [[100, 110, 120], [140, 150, 160], [180, 190, 200]]  # Projected cash flows (in millions of dollars)
discount_rate = 0.1  # Discount rate
growth_rates = [0.05, 0.03]  # Growth rates for each stage
company_value = value_company(projected_cash_flows, discount_rate,
