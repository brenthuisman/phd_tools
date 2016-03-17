#!/usr/bin/env python
import image,sys

crush = [1,1,0,1]
infile = sys.argv[-1] #in goes mhd
outpostfix = ".z"

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.saveprojection(outpostfix, crush)
