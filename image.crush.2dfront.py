#!/usr/bin/env python
import image,sys

infile = sys.argv[-1] #in goes mhd
outpostfix = ".2dfront"
crush = [0,0,1,1]

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.saveprojection(outpostfix, crush)
