import ROOT as r,pickle,numpy as np

def dump(rootfiles,field,bins,lowrange,highrange):
	#get nr primaries
	prims=0
	#print '/'.join(rootfiles[0].split('/')[:-1])+'/stat-proton.txt'
	header = open('/'.join(rootfiles[0].split('/')[:-1])+'/stat-proton.txt','r')
	for line in header:
		newline = line.strip()
		if len(newline)==0:
			continue
		if 'NumberOfEvents' in newline:
			prims = float(newline.split()[-1])
	if prims is 0:
		print "No valid number of primaries detected. Aborting..." 
		return
	outdata = [0]*bins

	for rootfile in rootfiles:
		tfile=r.TFile(rootfile)
		tree=tfile.Get("PhaseSpace")
		#http://root.cern.ch/root/html/TTree.html#TTree:Draw@1
		tree.Draw(field+'>>hnew('+str(bins)+','+str(lowrange)+','+str(highrange)+')')
		#Note that this returns a TH1F, not TH1D, so not very precise.
		hnew = r.gPad.GetPrimitive("hnew");
		#because root is a bitch, it is 1-indexed. so thats why theres a shift.
		for i in range(1,hnew.GetNbinsX()+1):
			#print hnew.GetBinCenter(i), hnew.GetBinContent(i)
			outdata[i-1] = float(hnew.GetBinContent(i))/float(prims)

	return outdata

def getyield(rootfiles):
	#get nr primaries
	prims=0
	header = open('/'.join(rootfiles[0].split('/')[:-1])+'/stat-proton.txt','r')
	for line in header:
		newline = line.strip()
		if len(newline)==0:
			continue
		if 'NumberOfEvents' in newline:
			prims = float(newline.split()[-1])
	if prims is 0:
		print "No valid number of primaries detected. Aborting..." 
		return

	totentries = 0
	for rootfile in rootfiles:
		tfile=r.TFile(rootfile)
		tree=tfile.Get("PhaseSpace")
		totentries += tree.GetEntries()

	return float(totentries)/(len(rootfiles)*prims)

def getcount(rootfiles):
	totentries = 0
	for rootfile in rootfiles:
		tfile=r.TFile(rootfile)
		tree=tfile.Get("PhaseSpace")
		totentries += tree.GetEntries()

	return totentries

def savedump(rootfiles,field,bins,lowrange,highrange,outname):
	dumpdata = dump(rootfiles,field,bins,lowrange,highrange)
	#print dumpdata
	with open(outname,'w') as thefile:
		pickle.dump(dumpdata, thefile)


def thist2np(infile,dt='<f4'):
	tfile=r.TFile(infile,"READ")
	retval={}
	for item in tfile.GetListOfKeys():
		outname=item.ReadObj().GetName()
		outdata=[]
		for i in range(item.ReadObj().GetNbinsX()):
			#print hnew.GetBinCenter(i), hnew.GetBinContent(i)
			outdata.append(float(item.ReadObj().GetBinContent(i+1)))
		#outdata=np.array(outdata, dtype=dt)
		#outdata.tofile(outname+'.raw')
		retval[outname]=outdata
	return retval


def thist2np_xy(infile):
	tfile=r.TFile(infile,"READ")
	retval={}
	for item in tfile.GetListOfKeys():
		outname=item.ReadObj().GetName()
		outdata_x=[]
		outdata_y=[]
		for i in range(item.ReadObj().GetNbinsX()):
			outdata_x.append(float(item.ReadObj().GetXaxis().GetBinCenter(i+1)))
			outdata_y.append(float(item.ReadObj().GetBinContent(i+1)))
		retval[outname]=[outdata_x,outdata_y]
	return retval
