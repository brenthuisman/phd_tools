#!/usr/bin/env python
import image,sys

infile = sys.argv[-1] #in goes mhd

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.save90pcmask()
