#!/usr/bin/env python
import image,sys

infile = sys.argv[-1] #in goes mhd

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
#img.insert_block('z','-',30)
img.insert_block('z','+',50)
img.saveas(".block.50.z.+")