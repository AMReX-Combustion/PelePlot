#
# Make some pseudocolor plots with visit
#
# Usage:
#    visit -nowin -cli -s /path/to/this/script.py
#

# ========================================================================
#
# Imports
#
# ========================================================================
import sys
import os
import argparse
import subprocess as sp


# ========================================================================
#
# Main
#
# ========================================================================
# Parse arguments
parser = argparse.ArgumentParser(description="A simple VisIt pseudocolor image maker")
parser.add_argument(
    "-f",
    "--folder",
    dest="folder",
    help="Folder containing data",
    type=str,
    default=".",
)
args = parser.parse_args()
folder = os.path.abspath(args.folder)
hname = os.path.join(folder, "Header")
pfx = "magvort"
fname = os.path.join(folder, pfx + ".png")

# Open file
OpenDatabase("localhost:{0:s}".format(hname), 0)

# Make pseudocolor
AddPlot("Pseudocolor", "magvort", 1, 1)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = 0
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 30000
PseudocolorAtts.centering = PseudocolorAtts.Natural
PseudocolorAtts.colorTableName = "OrRd"
PseudocolorAtts.invertColorTable = 0
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID
PseudocolorAtts.lineType = PseudocolorAtts.Line
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
# PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
# PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
DrawPlots()

# Annotations
AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes2D.autoSetTicks = 0
AnnotationAtts.axes2D.xAxis.title.userTitle = 1
AnnotationAtts.axes2D.xAxis.title.title = "x"
AnnotationAtts.axes2D.xAxis.label.font.scale = 0.5
AnnotationAtts.axes2D.xAxis.tickMarks.majorMinimum = 0
AnnotationAtts.axes2D.xAxis.tickMarks.majorMaximum = 20
AnnotationAtts.axes2D.xAxis.tickMarks.minorSpacing = 0.2
AnnotationAtts.axes2D.xAxis.tickMarks.majorSpacing = 2.0
AnnotationAtts.axes2D.yAxis.title.userTitle = 1
AnnotationAtts.axes2D.yAxis.title.title = "y"
AnnotationAtts.axes2D.yAxis.label.font.scale = 0.5
AnnotationAtts.axes2D.yAxis.tickMarks.majorMinimum = -1
AnnotationAtts.axes2D.yAxis.tickMarks.majorMaximum = 1
AnnotationAtts.axes2D.yAxis.tickMarks.minorSpacing = 0.2
AnnotationAtts.axes2D.yAxis.tickMarks.majorSpacing = 1.0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.axesArray.axes.title.title = ""
SetAnnotationAttributes(AnnotationAtts)

# Legend
legend = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
legend.managePosition = 0
legend.numberFormat = "%# -9.1g"
legend.position = (0.82, 0.22)
legend.xScale = 0.3
legend.yScale = 0.3
legend.drawTitle = 0
legend.drawMinMax = 0

# View
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (0, 20, -1, 1)
View2DAtts.viewportCoords = (0.2, 0.8, 0.15, 0.95)
SetView2D(View2DAtts)

# Save the figure
SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 1
SaveWindowAtts.outputDirectory = folder
SaveWindowAtts.fileName = fname
SaveWindowAtts.family = 0
SaveWindowAtts.format = SaveWindowAtts.PNG
SaveWindowAtts.width = 1024 * 4
SaveWindowAtts.height = 1024 * 4
SaveWindowAtts.screenCapture = 0
SaveWindowAtts.saveTiled = 0
SaveWindowAtts.quality = 80
SaveWindowAtts.progressive = 0
SaveWindowAtts.binary = 0
SaveWindowAtts.stereo = 0
SaveWindowAtts.compression = SaveWindowAtts.PackBits
SaveWindowAtts.forceMerge = 0
SaveWindowAtts.resConstraint = SaveWindowAtts.ScreenProportions
SaveWindowAtts.advancedMultiWindowSave = 0
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()

# Crop image with imagemagick
cname = os.path.join(folder, pfx + "_c.png")
return_code = sp.call("convert -trim {0:s} {1:s}".format(fname, cname), shell=True)

sys.exit()
