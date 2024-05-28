/// \file main.cpp

//Copyright Ian Parberry, November 2013.
//
//This file is made available under the GNU All-Permissive License.
//
//Copying and distribution of this file, with or without
//modification, are permitted in any medium without royalty
//provided the copyright notice and this notice are preserved.
//This file is offered as-is, without any warranty.

#include <windows.h>
#include <MMSystem.h>
#include <timeapi.h>
#include <stdio.h>
#include <conio.h>
#include <vector>


#include <algorithm>
#include "valuenoise.cpp"
#include "valuenoise.h"
#pragma comment(lib, "Winmm.lib")


const int CELLSIZE = 512; //width of square grid
const int NUMOCTAVES = 8; //number of octaves of 1/f noise
const int ALTITUDE = 512; //altitude scale value

CDesignerWorld g_cDesignerWorld;
typedef std::vector<std::vector<float>> HeightMatrix;

//Height distribution data.
const float min_elevation = 0.0f;
const float max_elevation = 500.0f;
const bool scaled = false;
//const int POINTCOUNT = 31;
/*int g_nUtahDistribution[POINTCOUNT] = {
  1, 4, 6, 7, 7, 8, 10, 11, 14, 30, 37, 30, 19, 11, 8, 5, 5, 4, 3, 3, 3, 3, 3, 3, 5, 4, 4, 3, 2, 2, 1
};*/

const int POINTCOUNT = 28;
int g_nUtahDistribution[POINTCOUNT] = {
  104, 34, 22, 17, 15, 13, 10, 8, 6, 5, 4, 3, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1
};

/// Print the header for a DEM file.
/// \param output Output file handle.

void printDEMfileHeader(FILE* output){
  if(output == NULL)return; //bail and fail

  fprintf(output, "nrows %d\n", CELLSIZE);
  fprintf(output, "ncols %d\n", CELLSIZE);
  fprintf(output, "xllcenter %0.6f\n", 0.0f);
  fprintf(output, "yllcenter %0.6f\n", 0.0f);
  fprintf(output, "cellsize 5.000000\n");
  fprintf(output, "NODATA_value  -9999\n");
} //printDEMfileHeader

int main(int argc, char *argv[]){ 
  //initialize the random number generator
  int seed = timeGetTime();
  srand(seed);
  printf("Pseudorandom number seed = %d\n", seed);

  //set up designer world
  g_cDesignerWorld.Initialize();
  g_cDesignerWorld.SetValueTable(g_nUtahDistribution, POINTCOUNT);
  HeightMatrix heights(CELLSIZE, std::vector<float>(CELLSIZE, 0.0f));

  //start the DEM file
  char filename[MAX_PATH];
  sprintf_s(filename, "%d.asc", seed);
  FILE* output;
  fopen_s(&output, filename, "wt");
  printDEMfileHeader(output);

  //get random origin
  float x = (float)rand();
  float z = (float)rand();

  float max_height = -std::numeric_limits<float>::infinity();
  float min_height = std::numeric_limits<float>::infinity();

  for(int i=0; i<CELLSIZE; i++){
    for(int j=0; j<CELLSIZE; j++) {
      float height = g_cDesignerWorld.GetHeight(x + i/256.0f, z + j/256.0f, 0.5f, 2.0f, NUMOCTAVES);
      heights[i][j] = height;
      if (height>max_height) {
        max_height = height;
      }
      if (height<min_height) {
        min_height = height;
      }
    }
  }
  
  //normalise heights
  if (scaled) {
    for(int i=0; i<CELLSIZE; i++){
    for(int j=0; j<CELLSIZE; j++) {
      heights[i][j] = ((heights[i][j] - min_height) / (max_height - min_height)) * (max_elevation - min_elevation) + min_elevation;

    }
  }
  }

  //generate and save grid heights to DEM file
  for(int i=0; i<CELLSIZE; i++){
    for(int j=0; j<CELLSIZE; j++)
      fprintf(output, "%0.2f ",
        heights[i][j]*ALTITUDE);
    fprintf(output, "\n");
    if(i%100 == 0)printf(".");
  } //for

  //shut down and exit
  printf("\n");
  fclose(output);

  printf("Hit Almost Any Key to Exit...\n");
  _getch();
  return 0;
} //main
