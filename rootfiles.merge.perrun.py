#!/usr/bin/env python

'''
This script using pyROOT and clitkMergeRootFiles (must be in your path) to merge any number of db-*.root files produced with gate_run_submit_cluster.sh under the specified run-dir (recursively) into pgdb.root.
'''

import sys,ROOT as r,subprocess,glob2 as glob,numpy as np

rundirs = glob.glob("./**/run.*")

lst = ['reconstructedProfileHisto','histo']
detoutputs = [	"ipnl-patient-spot-auger",
				"ipnl.post",
				"ipnl.pre",
				"iba-patient-spot-auger",
				"iba.post",
				"iba.pre"
				]
ext=".root"
matchruns={	"run.aEUT":"run.zvDh",
			"run.fE9t":"run.HKws",
			"run.RsPP":"run.5sPw",
			"run.HtFv":"run.KPX0"
}

rundirs = [f for f in rundirs if f.split('/')[-1] not in matchruns.values()]

def merge(sources,outfile):
	if len(sources) > 1:
		print "Starting merge..."
		cmdforclitk = ""
		for rootfile in sources:
			cmdforclitk=cmdforclitk+" -i "+rootfile.strip()
		subprocess.check_output(['rm -f '+outfile+ext],shell=True)
		subprocess.check_output(["clitkMergeRootFiles"+cmdforclitk+" -o "+outfile+ext],shell=True)
		tfile=r.TFile(outfile+ext,"READ")
	else:
		print "One file found, dump to .raw..."
		tfile=r.TFile(sources[0],"READ")
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
		subprocess.check_output(['rm -f '+outfile+'.raw'],shell=True)
		outdata.tofile(outfile+'.raw')

for rundir in rundirs:
	for detoutput in detoutputs:
		files = glob.glob(rundir+"/**/"+detoutput+ext)
		run = rundir.split('/')[-1]
		try:
			files += glob.glob(rundir.replace(run,matchruns[run])+"/**/"+detoutput+ext)
		except:
			pass
		if len(files) == 0:
			print "check", run, "because it has no files!"
			continue
		dest = run+"."+detoutput.replace("-patient-spot-auger",".auger.")+"merged"
		merge(files,dest)

print "Done!"
