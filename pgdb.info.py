#!/usr/bin/env python
import os,sys,ROOT as r

if len(sys.argv) < 2:
	print "Specify a PGDB phasespace (rootfile)."
	sys.exit()

rootfile = sys.argv[-1]

##now, correct for number of jobs/matieral
tfile=r.TFile(rootfile,"READ")
for item in tfile.GetListOfKeys():
	if "Hydrogen" in item.GetName():
		continue
	for thist in item.ReadObj().GetListOfKeys():
		name = thist.GetName()
		if 'Ngamma' in name:
			print thist.ReadObj().GetEntries(), "\ttot entries for",item.GetName()
			#print  thist.ReadObj().ProjectionX("whatever", 0, 0).GetEntries()
			print  thist.ReadObj().ProjectionX("whatever", 1, 1).GetEntries(), "\t",thist.ReadObj().ProjectionX("whatever", 1, 1).GetEntries()/thist.ReadObj().GetEntries()
			print  thist.ReadObj().ProjectionX("whatever", 2, 2).GetEntries(), "\t",thist.ReadObj().ProjectionX("whatever", 2, 2).GetEntries()/thist.ReadObj().GetEntries()
			print  thist.ReadObj().ProjectionX("whatever", 3, 3).GetEntries(), "\t",thist.ReadObj().ProjectionX("whatever", 3, 3).GetEntries()/thist.ReadObj().GetEntries()


print "Done! Your database can be found in db.root."