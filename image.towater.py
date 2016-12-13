#!/usr/bin/env python
import image,sys,numpy

infile = sys.argv[-1] #in goes mhd

print >> sys.stderr, 'Processing', infile

print "This tool will set all voxel to water (HU=0)."

img = image.image(infile)
img.towater()
img.saveas(".water")
