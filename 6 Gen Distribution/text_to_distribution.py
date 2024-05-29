import numpy as np
import matplotlib.pyplot as plt
import os
#import generate_distrubtion
from enum import Enum

def generate_terrain_distribution(num_bins, total_points, loc1, scale1, ratio1, loc2=None, scale2=None, ratio2=None):
    if loc2 is None or scale2 is None or ratio2 is None:
        # Single mode distribution
        values = np.random.normal(loc=loc1, scale=scale1, size=total_points)
    else:
        # Multi mode distribution
        size1 = int(total_points * ratio1)
        size2 = total_points - size1
        values1 = np.random.normal(loc=loc1, scale=scale1, size=size1)
        values2 = np.random.normal(loc=loc2, scale=scale2, size=size2)
        values = np.concatenate((values1, values2))

    values = np.clip(values, 0, num_bins - 1)
    hist, _ = np.histogram(values, bins=num_bins, range=(0, num_bins))
    hist = normalize_distribution(hist, total_points)
    return hist

def normalize_distribution(hist, total_points):
    diff = total_points - sum(hist)
    if diff > 0:
        indices = np.random.choice(np.arange(len(hist)), diff)
        for idx in indices:
            hist[idx] += 1
    elif diff < 0:
        indices = np.random.choice(np.arange(len(hist)), -diff)
        for idx in indices:
            hist[idx] -= 1
    return hist

def plot_distribution(distribution, title):
    plt.bar(range(len(distribution)), distribution)
    plt.title(title)
    plt.xlabel('Elevation Range')
    plt.ylabel('Number of Data Points')
    plt.show()

# Enum for terrain types
class Terrain(Enum):
    PLAINS = 1
    HILLY = 2
    SMOOTH_MOUNTAIN = 3
    JAG_MOUNTAIN = 4
    ISLANDS = 5
    PLATEUS = 6
    ARCHIPELAGO = 7

class Params:
    def __init__(self, terrain: Terrain):
        self.terrain = terrain
        self.dist_params = self._get_distribution_params()
        self.noise_params = self._get_noise_params()

    def _get_distribution_params(self):
        distribution_params = {
            Terrain.PLAINS: (5, 2, 1.0),
            Terrain.HILLY: (16, 8, 1.0),
            Terrain.SMOOTH_MOUNTAIN: (25, 5, 1.0),
            Terrain.JAG_MOUNTAIN: (25, 5, 1.0),
            Terrain.ISLANDS: (1, 5, 0.7, 25, 10, 0.3),
            Terrain.PLATEUS: (25, 2, 1.0),
            Terrain.ARCHIPELAGO: (5, 5, 0.6, 25, 10, 0.4)
        }
        return distribution_params.get(self.terrain)

    def _get_noise_params(self):
        noise_params = {
            Terrain.PLAINS: (0.5, 2.0, 4, 10, 80),           # Low frequency, low lacunarity
            Terrain.HILLY: (1.0, 2.0, 6, 80, 150),            # Medium frequency, medium lacunarity
            Terrain.SMOOTH_MOUNTAIN: (1.5, 2.0, 8, 150, 300),  # Higher frequency, higher lacunarity
            Terrain.JAG_MOUNTAIN: (2.0, 2.5, 10, 150, 350),    # Highest frequency, highest lacunarity
            Terrain.ISLANDS: (1.0, 2.0, 6, 0, 150),          # Medium frequency, medium lacunarity
            Terrain.PLATEUS: (1.5, 2.0, 4, 150, 300),          # Higher frequency, medium lacunarity
            Terrain.ARCHIPELAGO: (1.0, 2.0, 6, 0, 150)       # Medium frequency, medium lacunarity
        }
        return noise_params.get(self.terrain)

    def _get_erosion_params(self):
        erosion_params = {
            Terrain.PLAINS: (False, True, False, False),           
            Terrain.HILLY: (True, True, True, False),            
            Terrain.SMOOTH_MOUNTAIN: (True, True, True, False),  
            Terrain.JAG_MOUNTAIN: (True, True, True, False),    
            Terrain.ISLANDS: (False, True, True, False),          
            Terrain.PLATEUS: (False, False, False, True),         
            Terrain.ARCHIPELAGO: (False, False, True, False)       
        }
        return erosion_params.get(self.terrain)


# Obsolete function? 
def apply_erosion(terrain: Terrain, height_grid):
    return height_grid

def write_distribution_to_file(filename, terrain_type, distribution, noise_params, erosion_params):
    with open(filename, 'a') as file:
        file.write(f'Terrain type: "{terrain_type}"\n')
        file.write(f'const int POINTCOUNT = {len(distribution)};\n')
        file.write(f'int g_nUtahDistribution[POINTCOUNT] = {{\n  ')
        file.write(', '.join(map(str, distribution)))
        file.write('\n};\n')
        
        file.write('Noise Parameters:\n')
        file.write(f'  Frequency: {noise_params[0]}\n')
        file.write(f'  Lacunarity: {noise_params[1]}\n')
        file.write(f'  Octaves: {noise_params[2]}\n')
        file.write(f'  Min Height: {noise_params[3]}\n')
        file.write(f'  Max Height: {noise_params[4]}\n')

        file.write('Erosion Parameters:\n')
        code_text = (f'params = [[{erosion_params[0]}, nrows, 200], [{erosion_params[1]}, 7, 0.1] , [{erosion_params[2]}], [{erosion_params[3]}, {(noise_params[3] + noise_params[4]) / 2}]]')
        file.write(code_text)

        # file.write(f'  Valley: {erosion_params[0]}\n')
        # file.write(f'  Sediment Erosion: {erosion_params[1]}\n')
        # file.write(f'  Fluvial Erosion: {erosion_params[2]}\n')
        # file.write(f'  Plateau: {erosion_params[3]}\n')
        
        file.write('\n\n')

# Example usage
if __name__ == "__main__":
    terrains = [Terrain.PLAINS, Terrain.HILLY, Terrain.SMOOTH_MOUNTAIN, Terrain.JAG_MOUNTAIN, Terrain.ISLANDS, Terrain.PLATEUS, Terrain.ARCHIPELAGO]
    current_dir = os.path.dirname(__file__)
    output_file = os.path.join(current_dir, 'terrain_distributions.txt')
    open(output_file, 'w').close()

    for terrain in terrains:
        params = Params(terrain)
        distribution = generate_terrain_distribution(32, 256, *params.dist_params)
        plot_distribution(distribution, terrain.name)
        noise_params = params._get_noise_params()
        erosion_params = params._get_erosion_params()
        write_distribution_to_file(output_file, terrain.name, distribution, noise_params, erosion_params)
        print(f'{terrain.name} Distribution:', distribution)