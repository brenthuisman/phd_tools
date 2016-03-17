#!/usr/bin/env python
import image,pickle

crush = [0,1,1,1]
outpostfix = ".x.list"

print "Loading..."

infile = "source.mhd"
tleimg = image.image(infile)
tleimg.save1dlist(outpostfix, crush)

infile = "source-tlevar.mhd"
tlevarimg = image.image(infile)
tlevarimg.save1dlist(outpostfix, crush)

infile = "analog.mhd"
analogimg = image.image(infile)
analogimg.save1dlist(outpostfix, crush)

# -----------------------------------------

crush = [1,1,1,0]
outpostfix = ".spect.list"

infile = "source.mhd"
tleimg = image.image(infile)
tleimg.save1dlist(outpostfix, crush)

infile = "source-tlevar.mhd"
tlevarimg = image.image(infile)
tlevarimg.save1dlist(outpostfix, crush)

infile = "analog.mhd"
analogimg = image.image(infile)
analogimg.save1dlist(outpostfix, crush)
