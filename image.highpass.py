#!/usr/bin/env python
import image,sys

infile = sys.argv[-1] #in goes mhd
thres = float(sys.argv[-2])

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.savehighpass(thres)
