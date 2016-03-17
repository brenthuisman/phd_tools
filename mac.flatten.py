#!/usr/bin/env python
import sys,datetime,tableio

outmac=['#Merged macfile created on '+datetime.datetime.isoformat(datetime.datetime.now())]

def readmac(filename):
	macfile = open(filename,'r')
	mac = []
	for line in macfile.readlines():
		if line.startswith("/control/execute"):
			mac.extend(readmac(line.split()[-1].split('/')[-1]))
		else:
			mac.append(line.strip())
	macfile.close()
	return mac

outmac.extend(readmac(sys.argv[-1]))

for line in outmac:
	print line