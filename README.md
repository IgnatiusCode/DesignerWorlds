# COMP4610/8610 Computer Graphics Final Project

### Group 90
  - Ignatius Fisher, u7297613 (COMP4610)
  - Jasmin Zhou, u7145232 (COMP4610)
  - Fangzhou Wang, u7765264 (COMP8610)

## Designer Worlds

  This GitHub repository: https://github.com/IgnatiusCode/DesignerWorlds
  is based on 
  Ian Parberry, "Designer Worlds: Procedural Generation of Infinite Terrain from
  Real-World Elevation Data", Journal of Computer Graphics Techniques, Vol. 3,
  No. 1, pp. 74-85, 2014.

  See also http://larc.unt.edu/ian/research/valuenoise/.

### ABSTRACT

  Procedural terrain generation is most commonly done by modeling fast noise textures such as Perlin
and Simplex noise. These often require mathematical understanding and there is a missing link 
between the types of terrain generated and the mathematical underpinnings required to find and tune
ideal parameters, especially for terrain designers. Additionally, terrain generated using
procedural noise functions is often unrealistically smooth and uniform. To solve this, we build 
upon existing methods using Value noise by linking a dictionary of terrain descriptors to noise 
parameters based on real-world height distributions and comparing different types of noise.
Additionally, we model the real-world process of erosion to increase the realism of the terrain. 
Our program provides a more robust framework to generate procedural terrain based on real-world 
data and links physical terrain descriptions to procedurally generated noise textures with 
increased resemblance to terrain formed by real-world processes.


### CONTENTS
  
  1. Data
  2. Analyze
  3. Generate
  4. View
  5. Erosion Sim
  6. Gen Distribution

Sections 1-2 are mostly unmodified from Parberry's method and were only used to observe histogram distributions of different types of landscapes. We have added a method to create distributions from gray images rather
than DEM files.

3. Generate

  This folder contains a Visual Studio 2012 Solution and C++ source code
  for the base terrain Generator. It contains methods to generate terrain based
  on different types of noise (simplex, perlin, and value noise). The respective classes 
  are g_sDesignerWorld, g_pDesignerWorld and g_cDesignerWorld. The default method is using
  value noise.The max and minimum height can be set to scale the terrain. Rather than using 
  the distribution generated using section 2, we use the distributions in section 6, 
  terrain_distributions.txt. 
  The parameters frequency, lacunarity, and ocataves are represented by a, b and NUMOCTAVES and
  are used as inputs into the GetHeight method. When this code is run, it will output a randomly 
  generated .asc file using the specified parameters.

4. View

  This contains the basis .tgd file containing texture information that we use to visualise the 
  results in Terragen 4.

5. Erosion Sim

  This folder contains python source code to apply erosion post-processing effects. It uses a list
  of params to apply erosion effects. The parameters unique to each terrain type are similarly 
  found in section 6, terrain_distributions.txt. When simulate_erosion is run with a correct input
  ASCII file as generated in section 3, it will display a 2D height map of the before and after
  erosion applications and output the corresponding ASCII file. For fluvial erosion, the river network 
  must be generated separately by running with the correct ASCII file from section 3 in fluvial.py. The
  height map is then stored to an .npz file and can be used as an input to sediment_erosion.py to apply other
  erosion effects.

6. Gen Distribution

  This folder contains python source code and text files to describe the parameters for each terrain type. 
  Histogram visualisions are also included. Running generate_distribution will output a list of 32 numbers
  sampled according to the distribution given for each terrain type. Running text_to_distribution will write
  the parameter summary for the distribution, value noise, and erosion simulation to the terrain_distributions.txt
 file.
