import numpy as np
import generate_distrubtion
from enum import Enum

list_of_terms = ['plains', 'hilly', 'smooth mountains', 'jagged mountains', 'islands', 'plateaus', 'archipelago']
valuenoise_params = ['frequency', 'lacunarity', 'octaves']

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
        #[num_modes, centres, spread, skew, kurtoses, weights]
        distribution_params = {
            Terrain.PLAINS: (10, 2),           
            Terrain.HILLY: (20, 5),            
            Terrain.SMOOTH_MOUNTAIN: (30, 7),  
            Terrain.JAG_MOUNTAIN: (40, 10),    
            Terrain.ISLANDS: (15, 3),          
            Terrain.PLATEUS: (25, 6),         
            Terrain.ARCHIPELAGO: (18, 4)       
        }
    
    def __get__noise_params(self):
        #[frequency, lacunarity, num_octaves, min_height, max_height]
        noise_params = {
            Terrain.PLAINS: (10, 2),           
            Terrain.HILLY: (20, 5),            
            Terrain.SMOOTH_MOUNTAIN: (30, 7),  
            Terrain.JAG_MOUNTAIN: (40, 10),    
            Terrain.ISLANDS: (15, 3),          
            Terrain.PLATEUS: (25, 6),         
            Terrain.ARCHIPELAGO: (18, 4)       
        }

    def __get__erosion_params(self):
        #[valley, sediment_erosion, fluvial_erosion, plateau]
        noise_params = {
            Terrain.PLAINS: (10, 2),           
            Terrain.HILLY: (20, 5),            
            Terrain.SMOOTH_MOUNTAIN: (30, 7),  
            Terrain.JAG_MOUNTAIN: (40, 10),    
            Terrain.ISLANDS: (15, 3),          
            Terrain.PLATEUS: (25, 6),         
            Terrain.ARCHIPELAGO: (18, 4)       
        }
    # other params include: valley (true/false), sediment_erosion(true/false)
    # fluvial erosion(true/false), plateau (true/false)


def apply_erosion(terrain : Terrain, height_grid):
    return None


