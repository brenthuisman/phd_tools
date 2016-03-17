#!/usr/bin/env python
import numpy,sys

filename = sys.argv[-1]
data = numpy.fromfile(filename, dtype='<i4')

print sum(data)