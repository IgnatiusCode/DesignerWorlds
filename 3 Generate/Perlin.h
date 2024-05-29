#pragma once

/// \brief Designer World generator -- simplex.
///
/// The Designer World generator makes 2D noise suitable for terrain height maps.
/// It combines Value Noise with a height distribution.

class PDesignerWorld
{
private:
    static const int SIZE = 256;  ///< Size of height table;
    static const int MASK = 0xFF; ///< Mask for height table indices.

    float m_fPosition[SIZE];           ///< Value table.
    int m_nPermute[SIZE];              ///< Permutation table. Holds a random permutation.
    void InitSampleTable(float scale); /// Fill sample table.
    // float noise(float x, float z);     ///< Noise generator.

public:
    void Initialize();                                          ///< Initialize.
    float GetHeight(float x, float z, float a, float b, int n); ///< Get height.
    void SetValueTable(int table[], const int n);               //< Set value table.
}; // CDesignerWorld