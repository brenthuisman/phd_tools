#!/usr/bin/env python
import image,sys

crush = [0,1,1,1]
infile = sys.argv[-1] #in goes mhd
outpostfix = ".x"

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.saveprojection(outpostfix, crush)
