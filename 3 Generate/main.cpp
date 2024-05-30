/// \file main.cpp

// Copyright Ian Parberry, November 2013.
//
// This file is made available under the GNU All-Permissive License.
//
// Copying and distribution of this file, with or without
// modification, are permitted in any medium without royalty
// provided the copyright notice and this notice are preserved.
// This file is offered as-is, without any warranty.

#include <windows.h>
#include <MMSystem.h>
#include <timeapi.h>
#include <stdio.h>
#include <conio.h>
#include <vector>
#include <limits>
#include <ctime>
#include <math.h>

#include <algorithm>
// value noise
#include "valuenoise.cpp"
#include "valuenoise.h"

// simplex noise
#include "Simplex.cpp"
#include "Simplex.h"

// perlin noise
#include "Perlin.cpp"
#include "Perlin.h"
#pragma comment(lib, "Winmm.lib")

// const int CELLSIZE = 512; //width of square grid
// const int NUMOCTAVES = 8; //number of octaves of 1/f noise
// const int ALTITUDE = 512; //altitude scale value

// for value noise
CDesignerWorld g_cDesignerWorld;
// for simplex noise
SDesignerWorld g_sDesignerWorld;
// for perlin noise
PDesignerWorld g_pDesignerWorld;
typedef std::vector<std::vector<float>> HeightMatrix;

// Height distribution data.
const float min_elevation = 0.0f;
const float max_elevation = 25.0f;
const bool scaled = true;

// Change this to the relevant output of the text file terain_distributions.txt
const int POINTCOUNT = 32;
int g_nUtahDistribution[POINTCOUNT] = {
  90, 18, 12, 13, 12, 6, 11, 9, 5, 2, 3, 5, 3, 3, 0, 1, 3, 5, 1, 1, 4, 4, 4, 4, 0, 2, 2, 3, 7, 3, 4, 16
};


/// Print the header for a DEM file.
/// \param output Output file handle.

void printDEMfileHeader(FILE *output)
{
  if (output == NULL)
    return; // bail and fail

  fprintf(output, "nrows %d\n", CELLSIZE);
  fprintf(output, "ncols %d\n", CELLSIZE);
  fprintf(output, "xllcenter %0.6f\n", 0.0f);
  fprintf(output, "yllcenter %0.6f\n", 0.0f);
  fprintf(output, "cellsize 5.000000\n");
  fprintf(output, "NODATA_value  -9999\n");
} // printDEMfileHeader

int main(int argc, char *argv[])
{
  // initialize the random number generator
  int seed = timeGetTime();
  srand(seed);
  printf("Pseudorandom number seed = %d\n", seed);

  // set up designer world
  // // if use simplex noise
  // g_sDesignerWorld.Initialize();
  // g_sDesignerWorld.SetValueTable(g_nUtahDistribution, POINTCOUNT);

  // if use value noise
  g_cDesignerWorld.Initialize();
  g_cDesignerWorld.SetValueTable(g_nUtahDistribution, POINTCOUNT);

  // // if use perlin noiser
  // g_pDesignerWorld.Initialize();
  // g_pDesignerWorld.SetValueTable(g_nUtahDistribution, POINTCOUNT);

  HeightMatrix heights(CELLSIZE, std::vector<float>(CELLSIZE, 0.0f));

  // start the DEM file
  char filename[MAX_PATH];
  sprintf_s(filename, "%d.asc", seed);
  FILE *output;
  fopen_s(&output, filename, "wt");
  printDEMfileHeader(output);

  // get random origin
  float x = (float)rand();
  float z = (float)rand();

  float max_height = -std::numeric_limits<float>::infinity();
  float min_height = std::numeric_limits<float>::infinity();

  for (int i = 0; i < CELLSIZE; i++)
  {
    for (int j = 0; j < CELLSIZE; j++)
    {
      // // get height from simplex noise
      // float height = g_cDesignerWorld.GetHeight(x + i / 256.0f, z + j / 256.0f, 0.5f, 2.0f, NUMOCTAVES);

      // // Seed the random number generator
      // srand(time(nullptr));
      // // Generate a random float around 10
      //float randomNumber = 40.0f + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / 2.0f)) - 1.0f;
    
      // get height from value noise
      float height = g_cDesignerWorld.GetHeight(x + i / 256.0f, z + j / 256.0f, 0.5f, 2.0f, NUMOCTAVES);

      // // get height from perlin noise
      // float height = g_pDesignerWorld.GetHeight(x + i / 256.0f, z + j / 256.0f, 0.5f, 2.0f, NUMOCTAVES);
      // // increase the height 
      // heights[i][j] = abs(height) * 30.0f;
      
      // increase the height to a random times (about 40)
      heights[i][j] = height;
      // printf("%f/", pow(height, rn));
      if (height > max_height)
      {
        max_height = height;
      }
      if (height < min_height)
      {
        min_height = height;
      }
    }
  }

  // normalise heights
  if (scaled)
  {
    for (int i = 0; i < CELLSIZE; i++)
    {
      for (int j = 0; j < CELLSIZE; j++)
      {
        heights[i][j] = ((heights[i][j] - min_height) / (max_height - min_height)) * (max_elevation - min_elevation) + min_elevation;
      }
    }
  }

  // generate and save grid heights to DEM file
  for (int i = 0; i < CELLSIZE; i++)
  {
    for (int j = 0; j < CELLSIZE; j++)
      fprintf(output, "%0.2f ",
        heights[i][j]*ALTITUDE);
    fprintf(output, "\n");
    if (i % 100 == 0)
      printf(".");
  } // for

  // shut down and exit
  printf("\n");
  fclose(output);

  printf("Hit Almost Any Key to Exit...\n");
  _getch();
  return 0;
} // main
