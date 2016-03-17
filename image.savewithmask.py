#!/usr/bin/env python
import image,sys

if len(sys.argv) < 3:
	print "Supply an image and a mask."
	sys.exit()

maskfile = sys.argv[-1] #mask
infile = sys.argv[-2] #image

print >> sys.stderr, 'Processing', infile, maskfile

#todo: upconvert 3d-maskfile first
img = image.image(infile)
img.savewithmask('.msk',maskfile)