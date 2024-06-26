#include <stdlib.h>
#include <stdio.h>
#include <algorithm>

#include "Simplex.h"
#include "SimplexNoise.cpp"
SimplexNoise simplexNoise;

// const int CELLSIZE = 4000; // width of square grid
// const int NUMOCTAVES = 8;  // number of octaves of 1/f noise
// const int ALTITUDE = 4000; // altitude scale value

/// Initialize the permutation table.

void SDesignerWorld::Initialize()
{
    // start with identity permutation
    for (int i = 0; i < SIZE; i++)
        m_nPermute[i] = i;
    // randomize
    for (int i = SIZE - 1; i > 0; i--)
    {
        int j = rand() % (i + 1); // note the fix to Perlin's original code
        int temp = m_nPermute[i];
        m_nPermute[i] = m_nPermute[j];
        m_nPermute[j] = temp;
    } // for
} // Initialize

/// Set the value table.
/// \param table Table of values.
/// \param n Size of table.
void SDesignerWorld::SetValueTable(int table[], const int n)
{
    // check that the values add up to 256
    int sum = 0;
    for (int i = 0; i < n; i++)
        sum += table[i];
    if (sum != SIZE)
    {
        printf("Height distribution values must sum to %d, not %d\n", SIZE, sum);
        return; // fail and bail
    } // if
    // fill the table
    float delta = 2.0f / (float)(n - 1); // interval size
    float min = -1.0f;                   // lower limit if interval
    int k = 0;                           // fill in m_fPosition[k]
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < table[i]; j++)
            m_fPosition[k++] = min + delta * (float)rand() / (float)RAND_MAX;
        min += delta;
    } // for
    // missed the largest values, get them now
    for (int j = 0; j < table[n - 1]; j++)
        m_fPosition[k++] = 1.0f;
} // SetValueTable
/// Get random height value at a point in the terrain.
/// Computes 1/f noise using the sample table.
/// \param x X coordinate of point at which to sample
/// \param z Z coordinate of point at which to sample
/// \param a Frequency
/// \param b Lacunarity
/// \param n Number of octaves
/// \return Height value between 0.0 and 1.0

float SDesignerWorld::GetHeight(float x, float z, float a, float b, int n)
{
    float result = 0.0f; // resulting height
    float scale = 1.0f;  // scale of next octave
    float sum_scales = 1.0f;
    float decrese_unit = scale / n;

    for (int i = 0; i < n; i++)
    // while(n > 0)
    { // for each octave
        result += scale * simplexNoise.noise(x, z);
        scale *= a; // scale down amplitude of next octave
        sum_scales += scale;
        a *= b;
        a *= b; // scale down wavelength of next octave
    } // for

    return result;
} // GetHeight