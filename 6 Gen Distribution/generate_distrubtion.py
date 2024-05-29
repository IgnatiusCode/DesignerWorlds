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


from scipy.stats import skewnorm, t


def generate_data(num_modes, centres, spreads, skews, kurtoses, weights=None, n_samples=20, data_range=(0, 256)):
    if weights is None:
        weights = [1] * num_modes  # Equal weights if not provided
    
    # Normalize weights to ensure they sum up to 1
    weights = np.array(weights)
    weights /= np.sum(weights)
    
    data = np.zeros(n_samples)
    for i in range(num_modes):
        # Generate base normal distribution for each mode
        mode_data = np.random.normal(centres[i], spreads[i], size=(n_samples,))
        
        # Adjust skewness
        mode_data = skewnorm.rvs(skews[i], loc=mode_data.mean(), scale=mode_data.std(), size=n_samples)
        
        # Adjust kurtosis indirectly by varying degrees of freedom
        if kurtoses[i] > 0:
            degrees_of_freedom = 2 / (kurtoses[i] + 1)  # Convert kurtosis to degrees of freedom
        else:
            degrees_of_freedom = 100  # High degrees of freedom for non-skew-t distributions
        
        # Generate t-distributed data
        mode_data = t.rvs(df=degrees_of_freedom, loc=mode_data.mean(), scale=mode_data.std(), size=n_samples)
        
        # Ensure all generated numbers are positive
        min_value = np.Infinity
        for d in mode_data:
            if d < min_value:
                min_value = d
        mode_data = [x+min_value for x in mode_data]
        
        # Add mode to overall data with weight
        data += mode_data
    
    # Calculate scaling factor to make the sum of rounded numbers equal to 256
    scaling_factor = (data_range[1] - data_range[0]) / np.sum(np.round(data))
    
    # Scale the data by the calculated factor and round to the nearest integer
    data = np.round(data * scaling_factor).astype(int)
    
    # Clip the data to ensure it falls within the specified range
    data = np.clip(data, data_range[0], data_range[1])
    
    return data

# Example usage
distribution_params = {
    'num_modes': 2,         # Number of modes
    'centres': [5, 50.0],    # Means or centres of the distributions
    'spreads': [10.0, 50.0],      # Spreads or standard deviations of the distributions
    'skews': [0.0, 0.0],        # Skewnesses of the distributions
    'kurtoses': [0.0, 0.0],     # Kurtoses of the distributions
    'weights': [30.0, 70.0],   # Weights of the distributions
}

""" distribution_params = {
    'num_modes': 1,         # Number of modes
    'centres': [2.0],    # Means or centres of the distributions
    'spreads': [20.0],      # Spreads or standard deviations of the distributions
    'skews': [5.0],        # Skewnesses of the distributions
    'kurtoses': [0.0],     # Kurtoses of the distributions
    'weights': [100.0],   # Weights of the distributions
} """

data = generate_data(**distribution_params, n_samples=50, data_range=(0, 256))
print(data)
# Plot histogram
plt.hist(data, bins=20, alpha=0.7, color='blue', edgecolor='black')
plt.title('Histogram of Generated Numbers')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()