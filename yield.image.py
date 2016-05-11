#!/usr/bin/env python
import sys,image

infile = sys.argv[-1]
img = image.image(infile)
#data = numpy.fromfile(filename, dtype='<f4')

print img.imdata.sum()