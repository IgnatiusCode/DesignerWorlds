import numpy as np

list_of_terms = ['plains', 'hilly', 'mountainous', 'islands']
valuenoise_params = ['frequency', 'lacunarity', 'octaves']
distribution_params = ['num_modes', 'centre', 'spread', 'min_value', 'max_value', 'skew', 'kurtosis']

#todo:
#come up with some more terrain descriptors you think might fit unique types of distributions
#match the descriptors to a range of distrubution and value noise params
#check the appearance of the terrain generated to see if it matches/ is different enough

#depending on the input descriptor, create a distribtuion (28 numbers) using a random value in the range of each of the 
#param ranges

