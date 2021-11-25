#!/usr/bin/env python

from paraview.simple import *

# create a new 'CSV Reader'
pointCloudcsv = CSVReader(FileName=['pointCloud.csv'])

# create a new 'TTK DimensionReduction'
tTKDimensionReduction1 = TTKDimensionReduction(Input=pointCloudcsv, ModulePath='default')
tTKDimensionReduction1.InputColumns = ['Points:0', 'Points:1', 'Points:2']
tTKDimensionReduction1.UseAllCores = 0

# create a new 'Table To Points'
tableToPoints2 = TableToPoints(Input=tTKDimensionReduction1)
tableToPoints2.XColumn = 'Component_0'
tableToPoints2.YColumn = 'Component_1'
tableToPoints2.ZColumn = 'Component_0'
tableToPoints2.a2DPoints = 1

# create a new 'Gaussian Resampling'
gaussianResampling2 = GaussianResampling(Input=tableToPoints2)
gaussianResampling2.ResampleField = ['POINTS', 'ignore arrays']
gaussianResampling2.ResamplingGrid = [128, 64, 3]
gaussianResampling2.SplatAccumulationMode = 'Sum'

# create a new 'Table To Points'
tableToPoints1 = TableToPoints(Input=pointCloudcsv)
tableToPoints1.XColumn = 'Points:0'
tableToPoints1.YColumn = 'Points:1'
tableToPoints1.ZColumn = 'Points:2'

# create a new 'Gaussian Resampling'
gaussianResampling1 = GaussianResampling(Input=tableToPoints1)
gaussianResampling1.ResampleField = ['POINTS', 'ignore arrays']
gaussianResampling1.ResamplingGrid = [64, 64, 128]

# create a new 'Outline'
outline1 = Outline(Input=gaussianResampling1)

# create a new 'Slice'
slice1 = Slice(Input=gaussianResampling2)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [-0.00547350355230147, 0.0452015383244153, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# create a new 'TTK PersistenceDiagram'
tTKPersistenceDiagram1 = TTKPersistenceDiagram(Input=slice1)
tTKPersistenceDiagram1.ScalarField = ['POINTS', 'SplatterValues']
tTKPersistenceDiagram1.InputOffsetField = [None, '']

# create a new 'Threshold'
threshold1 = Threshold(Input=tTKPersistenceDiagram1)
threshold1.Scalars = ['CELLS', 'PairIdentifier']
threshold1.ThresholdRange = [-0.1, 999.0]

# create a new 'Threshold'
persistenceThreshold = Threshold(Input=threshold1)
persistenceThreshold.Scalars = ['CELLS', 'Persistence']
persistenceThreshold.ThresholdRange = [3.0, 999.0]

# create a new 'TTK TopologicalSimplification'
tTKTopologicalSimplification1 = TTKTopologicalSimplification(Domain=slice1, Constraints=persistenceThreshold)
tTKTopologicalSimplification1.ScalarField = ['POINTS', 'SplatterValues']
tTKTopologicalSimplification1.InputOffsetField = [None, '']
tTKTopologicalSimplification1.VertexIdentifierField = [None, '']

# create a new 'TTK MorseSmaleComplex'
tTKMorseSmaleComplex1 = TTKMorseSmaleComplex(Input=tTKTopologicalSimplification1)
tTKMorseSmaleComplex1.ScalarField = ['POINTS', 'SplatterValues']
tTKMorseSmaleComplex1.OffsetField = ['POINTS', 'SplatterValues']

# create a new 'TTK IcospheresFromPoints'
tTKIcospheresFromPoints1 = TTKIcospheresFromPoints(Input=tTKMorseSmaleComplex1)
tTKIcospheresFromPoints1.Radius = 0.075

# find source
tTKMorseSmaleComplex1_1 = FindSource('TTKMorseSmaleComplex1')

# create a new 'Threshold'
threshold2 = Threshold(Input=OutputPort(tTKMorseSmaleComplex1_1,1))
threshold2.Scalars = ['CELLS', 'SeparatrixType']
threshold2.ThresholdRange = [1.0, 1.0]

# create a new 'Threshold'
threshold3 = Threshold(Input=threshold2)
threshold3.Scalars = ['CELLS', 'NumberOfCriticalPointsOnBoundary']

# create a new 'TTK GeometrySmoother'
tTKGeometrySmoother1 = TTKGeometrySmoother(Input=threshold3)
tTKGeometrySmoother1.IterationNumber = 100
tTKGeometrySmoother1.InputMaskField = [None, '']

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=tTKGeometrySmoother1)

# create a new 'Tube'
tube1 = Tube(Input=extractSurface1)
tube1.Scalars = ['POINTS', 'CellDimension']
tube1.Vectors = [None, '']
tube1.Radius = 0.0414543533325195

SaveData('SplatterValues.vtp', slice1)
SaveData('GaussianResampling.vti', gaussianResampling1)
SaveData('MorseComplexeCriticalPoint.vtp', tTKIcospheresFromPoints1)
SaveData('MorseComplexeEdge.vtp', tube1)