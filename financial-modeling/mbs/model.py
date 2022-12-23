import pandas as pd
import numpy as np

def default_probability(loan_data, credit_score_bins, default_rates):
    """Calculate the default probability of a mortgage loan based on the borrower's credit score."""
    # Compute the credit score of the borrower
    credit_score = loan_data['credit_score']
    # Determine the credit score bin
    bin_idx = np.searchsorted(credit_score_bins, credit_score)
    # Return the default rate for the corresponding credit score bin
    return default_rates[bin_idx]

def present_value(cash_flows, discount_rate):
    """Calculate the present value of a series of cash flows using a discount rate."""
    return sum([cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows)])

def value_mbs(loan_data, credit_score_bins, default_rates, recovery_rates, discount_rate):
    """Value a mortgage-backed security based on the underlying mortgage loans, credit score bins, default rates, recovery rates, and a discount rate."""
    # Calculate the default probability of each loan
    loan_data['default_probability'] = loan_data.apply(lambda x: default_probability(x, credit_score_bins, default_rates), axis=1)
    # Calculate the expected cash flows of each loan
    loan_data['expected_cash_flow'] = loan_data['loan_amount'] * (1 - loan_data['default_probability']) * (1 - recovery_rates)
    # Calculate the present value of the expected cash flows
    loan_data['present_value'] = loan_data['expected_cash_flow'].apply(lambda x: present_value(x, discount_rate))
    # Return the sum of the present values as the estimated value of the MBS
    return sum(loan_data['present_value'])

# Test the function
#
