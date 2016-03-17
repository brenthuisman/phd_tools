#!/usr/bin/env python
import numpy,sys

#sources = [x.strip() for x in os.popen("find . -print | grep -i 'analog.mhd$'").readlines()]
#sources += [x.strip() for x in os.popen("find . -print | grep -i 'source.mhd$'").readlines()]

numpy.set_printoptions(threshold=numpy.nan) #print the full array, not just the edges

filename = sys.argv[-1]
data = numpy.fromfile(filename, dtype='<f4')

print data