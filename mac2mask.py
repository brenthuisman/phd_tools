#!/usr/bin/env python
import sys,mac,tableio

data = mac.tovoxel(sys.argv[-1])
#tableio.print2d(data.boxes)
#tableio.print2d(data.density)
#tableio.print2d(data.phantom)
data.makemask()
