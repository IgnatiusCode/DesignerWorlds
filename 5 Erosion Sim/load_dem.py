import numpy as np
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_grid
import rasterio
from rasterio.transform import from_origin

def load_asc_file(filename):
    with open(filename, 'r') as file:
        # Read and ignore the header lines
        nrows = int(file.readline().split()[1])
        ncols = int(file.readline().split()[1])
        xllcenter = float(file.readline().split()[1])
        yllcenter = float(file.readline().split()[1])
        cellsize = float(file.readline().split()[1])
        nodata_value = float(file.readline().split()[1])
        
        # Initialize an empty matrix with the given dimensions
        matrix = np.zeros((nrows, ncols))
        
        # Read the rest of the file into the matrix
        for i in range(nrows):
            line = file.readline().strip()
            values = line.split()
            for j in range(ncols):
                matrix[i, j] = float(values[j])
                
    return matrix, cellsize

def save_dem_as_ascii(grid, cell_size, output_file):
    # Create the transform for the raster
    transform = from_origin(0, grid.shape[0] * cell_size, cell_size, cell_size)

    # Save the grid as an ASCII Grid file
    with rasterio.open(
        output_file,
        'w',
        driver='AAIGrid',
        height=grid.shape[0],
        width=grid.shape[1],
        count=1,
        dtype=str(grid.dtype),
        crs='+proj=latlong',
        transform=transform
    ) as dst:
        dst.write(grid, 1)


