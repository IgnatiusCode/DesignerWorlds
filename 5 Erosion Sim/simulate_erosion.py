import load_dem
import landlab

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_grid

# read npz
data = np.load('river_network_106576406.npz')
terrian_heights, land_mask = data["height"], data["land_mask"]  # get terrian_heights
nrows, ncols = terrian_heights.shape  # nrows, ncols 
elevation = terrian_heights
cellsize = 5.0

types = ['valley', 'fluvial', 'sediment']

# =================================================origin============================================================
# Replace with your file path
# filename = r'C:\Users\jsmnz\OneDrive\Desktop\DesignerWorld4610\DesignerWorlds-1\5 Erosion Sim\106576406.asc'
# filename = r'106341437.asc'
# elevation, cellsize = load_dem.load_asc_file(filename)
# nrows, ncols = elevation.shape
# ===================================================================================================================  
valley = True
plateau = False
plateau_height = 10000
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))


def initialise_model(nrows, ncols, elevation, cellsize):
    mg = RasterModelGrid((nrows, ncols), cellsize)
    z = mg.add_field('topographic__elevation', elevation.flatten(), at='node')
    # plt.plot(mg.x_of_node, mg.y_of_node, '.')
    imshow_grid(mg, 'topographic__elevation')
    axes[0].set_title('Initial Elevation')
    plt.show()

    return z, mg


def get_valley(z, mg, grid_width, valley_width):

    valley_min = np.random.uniform(0, grid_width - valley_width)
    valley_max = valley_min+valley_width

    fault_trace_y = valley_min + 0.25 * mg.x_of_node
    fault_trace_y1 = valley_max + 0.25 * mg.x_of_node

    condition = (mg.y_of_node > fault_trace_y) & (
        mg.y_of_node < fault_trace_y1)
    # z[condition] -= 1000
    valley_center_y = (fault_trace_y + fault_trace_y1) / 2.0
    valley_width = fault_trace_y1 - fault_trace_y
    distance_from_center = abs(mg.y_of_node - valley_center_y)
    max_depth = 1000  # Maximum depth at the center of the valley

    normalized_distance = distance_from_center / (valley_width / 2.0)
    z[condition] = max_depth * (normalized_distance[condition]-1)


# z[mg.core_nodes]+10000

def get_plateaus(z, mg, plateau_height):
    z[mg.core_nodes > plateau_height] = plateau_height


def get_erosion(z, mg, D=7, dt_coeff=0.3):
    D = 7  # m2/yr transport coefficient
    dt = dt_coeff * mg.dx * mg.dx / D
    mg.set_closed_boundaries_at_grid_edges(True, False, True, False)
    qs = mg.add_zeros('sediment_flux', at='link')
    for i in range(10):
        print('step ' + str(i))
        g = mg.calc_grad_at_link(z)
        qs[mg.active_links] = -D * g[mg.active_links]
        dzdt = -mg.calc_flux_div_at_node(qs)
        print(dzdt[mg.core_nodes] * dt)
        z[mg.core_nodes] += dzdt[mg.core_nodes] * dt

    imshow_grid(mg, 'topographic__elevation')
    axes[1].set_title('Final Elevation After Erosion')
    plt.tight_layout()
    plt.show()


def save_to_ascii(mg, z, dem_output_file="elevation_dem.asc"):
    elevation_grid = mg.node_vector_to_raster(z)
    dem_output_file = "elevation_dem.asc"

# Save the DEM
    load_dem.save_dem_as_ascii(elevation_grid, mg.dx, dem_output_file)

    print(f"DEM file saved as {dem_output_file}")


params = [[True, nrows, 200], [True, 7, 0.3], [False], [False]]
# main


def erode_terrain(params, nrows, ncols, elevation, cellsize):

    z, mg = initialise_model(nrows, ncols, elevation, cellsize)
    if params[0][0] == True:
        get_valley(z, mg, params[0][1], params[0][2])
    if params[1][0] == True:
        get_erosion(z, mg, params[1][1], params[1][2])
    if params[3][0] == True:
        get_plateaus(z, mg, params[3][1])

    save_to_ascii(mg, z)


erode_terrain(params, nrows, ncols, elevation, cellsize)
