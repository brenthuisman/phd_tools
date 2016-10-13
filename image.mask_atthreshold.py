#!/usr/bin/env python
import image,sys

infile = sys.argv[-1] #in goes mhd
thres = float(sys.argv[-2])

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
print "Max val in image:",img.imdata.max()
print "Mask at threshold:",thres
img.savemask_atthreshold(thres)
