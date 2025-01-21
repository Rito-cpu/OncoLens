import numpy as np

from pyDOE import lhs

# TODO: Define num of samples (n_lhs), define ranges for each parameter

# Define the ranges for each parameter in your input space
# parameter_ranges = [(min_val_param1, max_val_param1), (min_val_param2, max_val_param2), ...]

# Generate Latin Hypercube Samples
# lhs_samples = lhs(len(parameter_ranges), samples=n_lhs)
# lhs_samples_scaled = [(param[1] - param[0]) * lhs_samples[:, i] + param[0] for i, param in enumerate(parameter_ranges)]

# Define strata (customize based on your problem)
# strata = [param1_range, param2_range, ...]

# Sample from each stratum
# stratified_samples = []
# for stratum in strata:
#     stratum_samples = lhs(len(stratum), samples=n_stratified)
#     stratified_samples.append(stratum_samples)

# Combine LHS and Stratified Samples
# all_samples = np.concatenate([lhs_samples_scaled, np.concatenate(stratified_samples)], axis=1)

# Example: Train GDRS model and make predictions
# for sample_set in all_samples:
#     gdrs_model.train(sample_set)
#     predictions = gdrs_model.predict()
#     capture_upper_lower_bounds(predictions)

def create_parameter_ranges(min_values, max_values):
    if  len(min_values) != len(max_values):
        raise ValueError("Minimum value list must have same length as maximum value list")

    parameter_ranges = []
    for min_val, max_val in zip(min_values, max_values):
        parameter_ranges.append((min_val, max_val))

    return parameter_ranges

def lhs_processing(min_param_list, max_param_list, n_lhs:int, n_stratified: int):
    # Define ranges for each parameter in input space
    parameter_ranges = create_parameter_ranges(min_param_list, max_param_list)

    # Generate LHS samples
    # n_lhs = number of samples
    lhs_samples = lhs(len(parameter_ranges), samples=n_lhs)
    lhs_samples_scaled = [(param[1] - param[0]) * lhs_samples[:, i] + param[0] for i, param in enumerate(parameter_ranges)]

    # Define strata (customize based on your problem)
    strata = [parameter_ranges[0], parameter_ranges[1], parameter_ranges[2]]

    # Sample from each stratum
    stratified_samples = []
    for stratum in strata:
        stratum_samples = lhs(len(stratum), samples=n_stratified)
        stratified_samples.append(stratum_samples)

    # Combine LHS and Stratified Samples
    all_samples = np.concatenate([lhs_samples_scaled, np.concatenate(stratified_samples)], axis=1)
    # TODO: left off here


if __name__ == "__main__":
    print(create_parameter_ranges([1, 2, 3], [11, 12, 13]))
