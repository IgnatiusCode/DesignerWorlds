import numpy as np
import generate_distrubtion
import sys
sys.path.append('../')
from enum import Enum
import simulate_erosion

list_of_terms = ['plains', 'hilly', 'smooth mountains', 'jagged mountains', 'islands', 'plateaus', 'archipelago']
valuenoise_params = ['frequency', 'lacunarity', 'octaves']

class Terrain(Enum):
    PLAINS = 1
    HILLY = 2
    SMOOTH_MOUNTAIN = 3
    JAG_MOUNTAIN = 4
    VALLEY = 5
    PLATEUS = 6
    ARCHIPELAGO = 7

class Params:
    def __init__(self, terrain: Terrain):
        self.terrain = terrain
        self.dist_params = self._get_distribution_params()
        self.noise_params = self._get_noise_params()
        self.erosion_params = self.__get__erosion_params()

    def _get_distribution_params(self):
        #[num_modes, centres, spread, skew, kurtoses, weights]
        distribution_params = {
            Terrain.PLAINS: [0,[], [], [],[]],           
            Terrain.HILLY: (20, 5),            
            Terrain.SMOOTH_MOUNTAIN: (30, 7),  
            Terrain.JAG_MOUNTAIN: (40, 10),  
            Terrain.VALLEY: (10,10),   
            Terrain.PLATEUS: (25, 6),         
            Terrain.ARCHIPELAGO: (18, 4)       
        }
    
    def __get__noise_params(self):
        #[frequency, lacunarity, num_octaves, min_height, max_height]
        noise_params = {
            Terrain.PLAINS: [0, 0, 0, 0, 1],           
            Terrain.HILLY: [0, 0, 0, 0, 1],            
            Terrain.SMOOTH_MOUNTAIN: [0, 0, 0, 0, 1],  
            Terrain.JAG_MOUNTAIN: [0, 0, 0, 0, 1], 
            Terrain.VALLEY: [0, 0, 0, 0, 1],           
            Terrain.PLATEUS: [0, 0, 0, 0, 1],         
            Terrain.ARCHIPELAGO: [0, 0, 0, 0, 1]      
        }

    def __get__erosion_params(self):
        #[valley, sediment_erosion, fluvial_erosion, plateau]
        noise_params = {
            Terrain.PLAINS: [False,True,False,False],           
            Terrain.HILLY: [False, True, False, False],            
            Terrain.SMOOTH_MOUNTAIN: [False,True,False,False],  
            Terrain.JAG_MOUNTAIN: [False,True,False,False],
            Terrain.VALLEY: [True, True, False, False],            
            Terrain.PLATEUS: [False,False,False,True],         
            Terrain.ARCHIPELAGO: [False,False,False,False]       
        }
    # other params include: valley (true/false), sediment_erosion(true/false)
    # fluvial erosion(true/false), plateau (true/false)


def apply_erosion(p : Params, height_grid):
    simulate_erosion.erode_terrain(p.erosion_params)




