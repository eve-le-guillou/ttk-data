# 1-Manifold Learning example

![1-Manifold Learning example Image](https://topology-tool-kit.github.io/img/gallery/1manifoldLearning.jpeg)


## Pipeline description

This example first loads cloud of points with elevation values from disk. 

In a pre-processing, the [DimensionReduction](https://topology-tool-kit.github.io/doc/html/classttk_1_1DimensionReduction.html) is used to reduce the dimension of the input to 3D points. The data is then converted to a format understandable by Paraview using the TableToPoints filter. Gaussian Resampling is applied to the data (upper left view in the above screenshot). This filter has the effect of injecting input points to a structured data. For each injection, each point will "splat", or distribute values to nearby vertices.

Then, the [PersistenceDiagram](https://topology-tool-kit.github.io/doc/html/classttkPersistenceDiagram.html) is computed and thresholds are applied based on persistence to maintain only the most persistent features. This results in a simplified persistence diagram (bottom left view in the above screenshot).

The simplified persistence diagram is then used as a constraint for the [TopologicalSimplification](https://topology-tool-kit.github.io/doc/html/classttkTopologicalSimplification.html) of the input scalar data.

This simplified data is then used as the input of the computation of [MorseSmaleComplex](https://topology-tool-kit.github.io/doc/html/classttk_1_1MorseSmaleComplex.html) (right view, above screenshot). This complex is composed of elements of 3 dimensions: dimension 0, which corresponds to the critical points of the Morse-Smale Complex, dimension 1, which corresponds to its edges (in grey on the screenshot) and dimension 2, which corresponds to its surfaces. Only certain edges are displayed here: using thresholds, the edges connecting at least one critical point situated on the boundary are discarded. This way, the "S" shape made by the cloud of points is outlined.

## ParaView
To reproduce the above screenshot, go to your [ttk-data](https://github.com/topology-tool-kit/ttk-data) directory and enter the following command:
``` bash
$ paraview states/1manifoldLearning.pvsm
```

## Python code

``` python  linenums="1"
--8<-- "python/1manifoldLearning.py"
```

## Inputs
- [pointCloud.csv](https://github.com/topology-tool-kit/ttk-data/raw/dev/pointCloud.csv): a four-dimensional table containing point coordinates and their elevation.

## Outputs
- `SplatterValues.vtp`: Slice of the gaussian resampling in VTK file format (bottom left view, above screenshot). You are free to change the `vtp` file extension to that of any other supported file format (e.g. `csv`) in the above python script.
- `GaussianResampling.vti`: the output of the gaussian resampling (upper left view, above screenshot). This should be displayed as a volume.
- `MorseComplexeCriticalPoints.vtp`: the output critical points (or 0 dimensional elements) of the Morse Smale Complex in VTK file format (right view, above screenshot). You are free to change the `vtp` file extension to that of any other supported file format (e.g. `csv`) in the above python script.
- `MorseComplexeEdge.vtp`: cylinders, representing the edges (or 1 dimensional elements) of the output Morse Smale Complexe in VTK file format (right view, above screenshot). You are free to change the `vtp` file extension to that of any other supported file format (e.g. `csv`) in the above python script.


## C++/Python API

[DimensionReduction](https://topology-tool-kit.github.io/doc/html/classttk_1_1DimensionReduction.html)

[GeometrySmoother](https://topology-tool-kit.github.io/doc/html/classttkGeometrySmoother.html)

[MorseSmaleComplex](https://topology-tool-kit.github.io/doc/html/classttk_1_1MorseSmaleComplex.html)

[IcospheresFromPoints](https://topology-tool-kit.github.io/doc/html/classttkIcospheresFromPoints.html)

[PersistenceDiagram](https://topology-tool-kit.github.io/doc/html/classttkPersistenceDiagram.html)

[TopologicalSimplification](https://topology-tool-kit.github.io/doc/html/classttkTopologicalSimplification.html)
