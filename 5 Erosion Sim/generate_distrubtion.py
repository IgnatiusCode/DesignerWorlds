import numpy as np

list_of_terms = ['plains', 'hilly', 'smooth mountains', 'jagged mountains', 'islands', 'plateaus', 'archipelago']
valuenoise_params = ['frequency', 'lacunarity', 'octaves']
distribution_params = ['num_modes', 'centre', 'spread', 'skew', 'kurtosis']
import matplotlib.pyplot as plt

#todo:
#come up with some more terrain descriptors you think might fit unique types of distributions
#match the descriptors to a range of distrubution and value noise params
#check the appearance of the terrain generated to see if it matches/ is different enough

#depending on the input descriptor, create a distribtuion (28 numbers) using a random value in the range of each of the 
#param ranges


from scipy.stats import skewnorm, t, uniform, gamma

from scipy.stats import pearson3


def generate_data(num_modes, centres, spreads, skews, kurtoses, weights=None, n_samples=20, data_range=(0, 256)):
    if weights is None:
        weights = np.ones(num_modes) / num_modes  # Equal weights if not provided
    else:
        weights = np.array(weights)
        weights /= np.sum(weights)  # Normalize weights to ensure they sum up to 1
    
    all_data = []
    for i in range(num_modes):
        # Generate Pearson Type III (gamma) distribution for each mode
        mode_data = pearson3.rvs(skews[i], loc=centres[i], scale=spreads[i], size=n_samples)
        
        # Add mode data to the list, scaled by its weight
        all_data.append(weights[i] * mode_data)
    
    # Combine all modes
    combined_data = np.sum(all_data, axis=0)
    
    # Scale the combined data to fit within the desired range
    combined_data -= combined_data.min()  # Shift data to be positive
    
    # Calculate scaling factor to make the sum of combined_data equal to 256
    scaling_factor = 256 / np.sum(combined_data)
    
    # Apply the scaling factor and round to the nearest integer
    combined_data = np.round(combined_data * scaling_factor).astype(int)
    
    # Clip the data to ensure it falls within the specified range
    combined_data = np.clip(combined_data, data_range[0], data_range[1])

    while sum(combined_data) < 256:
        combined_data[0] += 1
    
    while sum(combined_data) > 256:
        for i in range (0, n_samples):
            if combined_data[i] > 0:
                combined_data[i] -= 1
                break


    
    return combined_data

# def generate_data(num_modes, centres, spreads, skews, kurtoses, weights=None, n_samples=20, data_range=(0, 256)):
#     if weights is None:
#         weights = [1] * num_modes  # Equal weights if not provided
    
#     # Normalize weights to ensure they sum up to 1
#     weights = np.array(weights)
#     weights /= np.sum(weights)
    
#     data = np.zeros(n_samples)
#     for i in range(num_modes):
#         # Generate base normal distribution for each mode
#        # mode_data = np.random.gamma(centres[i], spreads[i], size=(n_samples))

#         shape = centres[i] / spreads[i]  # Shape parameter for Gamma distribution
#         scale = spreads[i]  # Scale parameter for Gamma distribution
#         mode_data = gamma.rvs(shape, scale=scale, size=n_samples)
        
#         # Adjust skewness
#         mode_data = skewnorm.rvs(skews[i], loc=mode_data.mean(), scale=mode_data.std(), size=n_samples)
        
#         # Adjust kurtosis indirectly by varying degrees of freedom
#         if kurtoses[i] > 0:
#             degrees_of_freedom = 2 / (kurtoses[i] + 1)  # Convert kurtosis to degrees of freedom
#         else:
#             degrees_of_freedom = 100  # High degrees of freedom for non-skew-t distributions
        
#         # Generate t-distributed data
#         #mode_data = t.rvs(df=degrees_of_freedom, loc=mode_data.mean(), scale=mode_data.std(), size=n_samples)


#         mode_data = mode_data - np.min(mode_data)

#         shape = max(kurtoses[i] + 1, 0.1)  # Shape parameter for Gamma distribution
#         scale = max(mode_data.std(), 0.1)  # Scale parameter for Gamma distribution
#         gamma_data = gamma.rvs(shape, loc=0, scale=scale, size=n_samples)
        
#         # Ensure all generated numbers are positive
#         gamma_data = gamma_data - np.min(gamma_data)
        
#         # Add mode to overall data with weight
#         data += weights[i] * gamma_data

#         #min_value = np.Infinity
#         #for d in mode_data:
#         #    if d < min_value:
#         #        min_value = d
#         #mode_data = [x+min_value for x in mode_data]
        
#         # # Add mode to overall data with weight
#         # data += mode_data
    
#     # Calculate scaling factor to make the sum of rounded numbers equal to 256
#     scaling_factor = (data_range[1] - data_range[0]) / np.sum(np.round(data))
    
#     # Scale the data by the calculated factor and round to the nearest integer
#     data = np.round(data * scaling_factor).astype(int)
    
#     # Clip the data to ensure it falls within the specified range
#     data = np.clip(data, data_range[0], data_range[1])
    
#     return data

# Example usage
distribution_params = {
    'num_modes': 2,         # Number of modes
    'centres': [5, 20.0],    # Means or centres of the distributions
    'spreads': [5.0, 5.0],      # Spreads or standard deviations of the distributions
    'skews': [0.0, 0.0],        # Skewnesses of the distributions
    'kurtoses': [0.0, 0.0],     # Kurtoses of the distributions
    'weights': [50.0, 50.0],   # Weights of the distributions
}

distribution_params = {
    'num_modes': 1,         # Number of modes
    'centres': [2.0],    # Means or centres of the distributions
    'spreads': [20.0],      # Spreads or standard deviations of the distributions
    'skews': [5.0],        # Skewnesses of the distributions
    'kurtoses': [0.0],     # Kurtoses of the distributions
    'weights': [100.0],   # Weights of the distributions
}

distribution_params_plateau = {
    'num_modes': 1,
    'centres': [8.0], # Mean elevation of the plateau
    'spreads': [1.0], # Low variation in elevation
    'skews': [-2], # Skewness
    'kurtoses': [8.0], # Kurtosis
    'weights': [100.0], # Equal weight for the plateau
}

distribution_params_mountainous = {
    'num_modes': 2,
    'centres': [5.0, 100.0],
    'spreads': [1.0, 2.0],
    'skews': [0.0, -10.0],  # More skewed towards higher elevations
    'kurtoses': [0.0, 0.0],
    'weights': [60.0, 40.0],  # More weight towards higher elevations
}

distribution_params_hilly = {
    'num_modes': 4,
    'centres': [2, 4, 6, 8],
    'spreads': [5,5,5,5],
    'skews': [-1,-1,-1,-1],  
    'kurtoses': [5,5,5,5],
    'weights': [0.1,0.1,0.4,0.4],  
}

distribution_params_arch = {
    'num_modes': 2,
    'centres': [0.0, 10.0],
    'spreads': [1.0, 2.0],
    'skews': [5.0, 0],  # More skewed towards higher elevations
    'kurtoses': [5.0, 5.0],
    'weights': [1.0, 4.0],  # More weight towards higher elevations
}

distribution_params_plains = {
    'num_modes': 1,
    'centres': [10.0],
    'spreads': [1.0],
    'skews': [0.0],  # More skewed towards higher elevations
    'kurtoses': [5.0],
    'weights': [1.0],  # More weight towards higher elevations
}




data = generate_data(**distribution_params_plains, n_samples=32, data_range=(0, 256))
print(*data , sep=", ")
# Plot histogram
plt.hist(data, bins=20, alpha=0.7, color='blue', edgecolor='black')
plt.title('Histogram of Generated Numbers')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()