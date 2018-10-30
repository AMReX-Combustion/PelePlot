#
# Post-process data using VisIt. Generates data files of
# - the spatial average of u^+v^2+w^2
# - the spatial average of sound speed
# - the spatial average of u^2
# - the spatial average of dudx^2
# - the spatial average of (T-Tmean)^2
# - the spatial average of (div u)^2
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
# Function definitions
#
# ========================================================================
def save_curve(plotnum, fdir, fname):
    """Save curve data"""
    SetActivePlots(plotnum)
    HideActivePlots()
    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 1
    SaveWindowAtts.outputDirectory = fdir
    SaveWindowAtts.fileName = fname
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.CURVE
    SaveWindowAtts.width = 1024
    SaveWindowAtts.height = 1024
    SaveWindowAtts.screenCapture = 0
    SaveWindowAtts.saveTiled = 0
    SaveWindowAtts.quality = 80
    SaveWindowAtts.progressive = 0
    SaveWindowAtts.binary = 0
    SaveWindowAtts.stereo = 0
    SaveWindowAtts.compression = SaveWindowAtts.None
    SaveWindowAtts.forceMerge = 0
    # NoConstraint, EqualWidthHeight, ScreenProportions
    SaveWindowAtts.resConstraint = SaveWindowAtts.ScreenProportions
    SaveWindowAtts.advancedMultiWindowSave = 0
    SetSaveWindowAttributes(SaveWindowAtts)
    SaveWindow()
    HideActivePlots()


# ========================================================================
#
# Main
#
# ========================================================================
# Parse arguments
parser = argparse.ArgumentParser(
    description='A simple post-processing tool for the HIT setup')
parser.add_argument('-f', '--folder',
                    dest='folder',
                    help='Folder containing HIT data',
                    type=str,
                    default='.')
args, _ = parser.parse_known_args()
folder = os.path.abspath(args.folder)

# Get the list of data
hname = os.path.join(folder, "plt*/Header")
mname = os.path.join(folder, "movie.visit")
return_code = sp.call('ls -1 {0:s} | tee {1:s}'.format(hname, mname),
                      shell=True)

# Define reference values for variances
mean_temp = 300.0

# Open files
OpenDatabase("localhost:{0:s}".format(mname), 0)

# Define expressions
DefineScalarExpression("magvel2", "sqr(magvel)")
DefineScalarExpression("cs_mod", "sqrt(pressure/density)")
DefineScalarExpression("dudx2", "sqr(gradient(x_velocity)[0])")
DefineScalarExpression("u2", "sqr(x_velocity)")
DefineScalarExpression("var_temp", "sqr(Temp-{0:.16f})".format(mean_temp))
DefineScalarExpression("divu2", "sqr(divergence(_velocity))")

# Integrate on the whole domain
AddPlot("Pseudocolor", "magvel2", 1, 1)
AddPlot("Pseudocolor", "cs_mod", 1, 1)
AddPlot("Pseudocolor", "dudx2", 1, 1)
AddPlot("Pseudocolor", "u2", 1, 1)
AddPlot("Pseudocolor", "var_temp", 1, 1)
AddPlot("Pseudocolor", "divu2", 1, 1)
DrawPlots()
SetQueryFloatFormat("%g")
QueryOverTimeAtts = GetQueryOverTimeAttributes()
QueryOverTimeAtts.timeType = QueryOverTimeAtts.DTime  # Cycle, DTime, Timestep
QueryOverTimeAtts.startTimeFlag = 0
QueryOverTimeAtts.startTime = 0
QueryOverTimeAtts.endTimeFlag = 0
QueryOverTimeAtts.endTime = 1
QueryOverTimeAtts.strideFlag = 0
QueryOverTimeAtts.stride = 1
QueryOverTimeAtts.createWindow = 1
QueryOverTimeAtts.windowId = 2
SetQueryOverTimeAttributes(QueryOverTimeAtts)
SetActivePlots(0)
QueryOverTime("Weighted Variable Sum", do_time=1)
SetActivePlots(1)
QueryOverTime("Weighted Variable Sum", do_time=1)
SetActivePlots(2)
QueryOverTime("Weighted Variable Sum", do_time=1)
SetActivePlots(3)
QueryOverTime("Weighted Variable Sum", do_time=1)
SetActivePlots(4)
QueryOverTime("Weighted Variable Sum", do_time=1)
SetActivePlots(5)
QueryOverTime("Weighted Variable Sum", do_time=1)

# Hide all curve plots
SetActiveWindow(2)
SetActivePlots(0)
HideActivePlots()
SetActivePlots(1)
HideActivePlots()
SetActivePlots(2)
HideActivePlots()
SetActivePlots(3)
HideActivePlots()
SetActivePlots(4)
HideActivePlots()
SetActivePlots(5)
HideActivePlots()

# Save the square of the magnitude of velocity
save_curve(0, folder, "magvel2")

# Save the modified sound speed data
save_curve(1, folder, "cs_mod")

# Save the square of the x_velocity gradient
save_curve(2, folder, "dudx2")

# Save the square of the x_velocity
save_curve(3, folder, "u2")

# Save the square of the x_velocity
save_curve(4, folder, "var_temp")

# Save the square of the x_velocity
save_curve(5, folder, "dilatation")

sys.exit()
