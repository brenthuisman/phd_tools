#!/usr/bin/env python
import sys,os,dump

if len(sys.argv) < 4:
	print "Specify (1) a fieldname, (2) a number of bins, (3) a run-dir with rootfiles with phasespaces."
	sys.exit()
fieldname = sys.argv[-3] #Ekine and EmissionPointZ most likely
nrbin = float(sys.argv[-2])
rootfiles = [x.strip() for x in os.popen("find "+sys.argv[-1]+" -print | grep -i 'interps.*.root$'").readlines()]
outname = filter(str.isalnum, sys.argv[-1]) + fieldname

print >> sys.stderr, 'Dumping', rootfiles

out = dump.dump(rootfiles,fieldname,nrbin,-nrbin,nrbin)#assume 1 bin = 2 mm
out.tofile(outname+'.txt', sep='\n')