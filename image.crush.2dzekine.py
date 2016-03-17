#!/usr/bin/env python
import image,sys

infile = sys.argv[-1] #in goes mhd
outpostfix = ".2dzekine"
crush = [1,1,0,0]

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.saveprojection(outpostfix, crush)
