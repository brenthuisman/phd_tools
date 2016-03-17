#!/usr/bin/env python
import sys,os,dump

if len(sys.argv) < 2:
	print "Specify a run-dir with rootfiles with phasespaces."
	sys.exit()
fieldname = 'Ekine' #Ekine and EmissionPointZ most likely'analog.mhd$'
rootfiles = [x.strip() for x in os.popen("find "+sys.argv[-1]+" -print | grep -i 'interps.*.root$'").readlines()]
outname = filter(str.isalnum, sys.argv[-1]) + fieldname

print >> sys.stderr, 'Dumping', rootfiles

out = dump.dump(rootfiles,fieldname,250,0,10)
out.tofile(outname+'.txt', sep='\n')