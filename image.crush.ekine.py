#!/usr/bin/env python
import image,sys

crush = [1,1,1,0]
infile = sys.argv[-1] #in goes mhd
outpostfix = ".ekine"

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.saveprojection(outpostfix, crush)
