#!/usr/bin/env python

'''
This script using pyROOT and clitkMergeRootFiles (must be in your path) to merge any number of db-*.root files produced with gate_run_submit_cluster.sh under the specified run-dir (recursively) into pgdb.root.
'''

import sys,ROOT as r,subprocess,glob2 as glob,numpy as np

lst = ['reconstructedProfileHisto','histo']

if len(sys.argv) is not 2:
	print "Specify an input filename."
	#print "Specify 1) a number of jobs per material and 2) input filename."
	sys.exit()
else:
	#njobs = int(sys.argv[-2])
	indir = '.'
	outfile = 'merged'+str(sys.argv[-1])
	infile = '*'+str(sys.argv[-1])

sources = glob.glob(indir+"/**/"+infile)#,recursive=True
# if len(sources)>3:
# 	sources=sources[90:100]
#print sources

if len(sources) == 0:
	print "No file found, exiting..."
	sys.exit()
if len(sources) == 1:
	print "One file found, convert single file to numpy array..."
	tfile=r.TFile(sources[0],"READ")
	for item in tfile.GetListOfKeys():
		if item.ReadObj().GetName() not in lst:
			continue
		outdata=[]
		for i in range(item.ReadObj().GetNbinsX()):
			#print hnew.GetBinCenter(i), hnew.GetBinContent(i)
			outdata.append(float(item.ReadObj().GetBinContent(i+1)))
		outdata=np.array(outdata, dtype='<f4')
		#print outdata
		subprocess.check_output(['rm -f '+outfile[:-5]+'.raw'],shell=True)
		outdata.tofile(outfile[:-5]+'.raw')
	sys.exit()

nr = len(sources)
print nr, "files found:", sources[:3], '...', sources[-3:]

sources2 = []
for i in sources:
	if r.TFile(i,"READ"):
		sources2.append(i)
	else:
		print i, "was found to be unreadable, remove folder!"
nr = len(sources2)
print nr, "files found:", sources2[:3], '...', sources2[-3:]

cmdforclitk = ""
for rootfile in sources2:
	cmdforclitk=cmdforclitk+" -i "+rootfile.strip()

print "Starting merge..."
#print cmdforclitk
subprocess.check_output(['rm -f '+outfile],shell=True)
subprocess.check_output(["clitkMergeRootFiles"+cmdforclitk+" -o "+outfile],shell=True)

##now, correct for number of jobs/matieral
# if njobs is not 1:
# 	factor = 1./float(njobs)
# 	tfile=r.TFile("merged.root","UPDATE")
# 	for item in tfile.GetListOfKeys():
# 		for thist in item.ReadObj().GetListOfKeys():
# 			# name = thist.GetName()
# 			# if 'EpEpgNorm' in name or 'GammaZ' in name:
# 			# 	print name
# 			thist.ReadObj().Scale(factor)
# 	tfile.Write()
# 	print "histograms scaled by factor",factor

tfile=r.TFile(outfile,"READ")
for item in tfile.GetListOfKeys():
	#print item.GetName()
	#print item.ReadObj().GetName()
	if item.ReadObj().GetName() not in lst:
		continue

	outdata=[]
	for i in range(item.ReadObj().GetNbinsX()):
		#print hnew.GetBinCenter(i), hnew.GetBinContent(i)
		outdata.append(float(item.ReadObj().GetBinContent(i+1)))
	outdata=np.array(outdata, dtype='<f4')
	subprocess.check_output(['rm -f '+outfile[:-5]+'.raw'],shell=True)
	outdata.tofile(outfile[:-5]+'.raw')

print "Done! Your database can be found in", outfile
