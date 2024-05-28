import load_dem
import landlab

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors



from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_grid

types = ['valley', 'fluvial', 'sediment']
valley = False

filename = '53526812.asc'  # Replace with your file path
elevation, cellsize = load_dem.load_asc_file(filename)
nrows, ncols = elevation.shape


mg = RasterModelGrid((nrows, ncols), cellsize)
z = mg.add_field('topographic__elevation', elevation.flatten(), at='node')
#plt.plot(mg.x_of_node, mg.y_of_node, '.')
D = 1  # m2/yr transport coefficient
dt = 0.2 * mg.dx * mg.dx / D
mg.set_closed_boundaries_at_grid_edges(True, False, True, False)
qs = mg.add_zeros('sediment_flux', at='link')

if valley:
  fault_trace_y = 50.0 + 0.25 * mg.x_of_node
  z[mg.y_of_node >
    fault_trace_y] += 10.0 + 0.01 * mg.x_of_node[mg.y_of_node > fault_trace_y]
  
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

# Plot the initial elevation grid in the first subplot
imshow_grid(mg, 'topographic__elevation')
axes[0].set_title('Initial Elevation')
#imshow_grid(mg, 'topographic__elevation')
plt.show()
for i in range(16):
    print('step '+ str(i))
    g = mg.calc_grad_at_link(z)
    qs[mg.active_links] = -D * g[mg.active_links]
    dzdt = -mg.calc_flux_div_at_node(qs)
    print(dzdt[mg.core_nodes] * dt)
    z[mg.core_nodes] += dzdt[mg.core_nodes] * dt

imshow_grid(mg, 'topographic__elevation')
axes[1].set_title('Final Elevation After Erosion')

# Display the plots
plt.tight_layout()
plt.show()

#imshow_grid(mg, 'topographic__elevation')
#splt.show()

elevation_grid = mg.node_vector_to_raster(z)
dem_output_file = "elevation_dem.asc"

# Save the DEM
load_dem.save_dem_as_ascii(elevation_grid, mg.dx, dem_output_file)

print(f"DEM file saved as {dem_output_file}")


