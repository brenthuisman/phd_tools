#!/usr/bin/env python
import sys,mac,tableio

if len(sys.argv) is 3:
	data = mac.tovoxel(sys.argv[-2],spacing=int(sys.argv[-1]))
else:
	data = mac.tovoxel(sys.argv[-1])
#tableio.print2d(data.boxes)
data.makeimage()
