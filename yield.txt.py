#!/usr/bin/env python
import numpy,sys

filename = sys.argv[-1]

prims=0.
header = open(filename,'r')
for line in header:
	newline = line.strip()
	prims += float(newline.split()[-1])

print prims