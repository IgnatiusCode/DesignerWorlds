import numpy as np
import generate_distrubtion
from enum import Enum

list_of_terms = ['plains', 'hilly', 'smooth mountains', 'jagged mountains', 'islands', 'plateaus', 'archipelago']
valuenoise_params = ['frequency', 'lacunarity', 'octaves']

class Terrain(Enum):
    PLAINS = 1
    HILLY = 2
    SMOOTH_MOUTAIN = 3
    JAG_MOUNTAIN = 4
    ISLANDS = 5
    PLATEUS = 6
    ARCHIPELAGO = 7



