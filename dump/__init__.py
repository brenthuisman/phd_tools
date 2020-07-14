import os,numpy as np,uproot

def readtxtnumber(filee):
	out=None
	with open(filee, 'r') as f:
		out=f.readlines()[0].strip('\n').strip()
	return float(out)

def binedges_to_centers(lst): # TODO move elsewhere? plot?
	retval = []
	for i,_ in enumerate(lst[:-1]):
		retval.append( (lst[i]+lst[i+1])/2. )
	return retval

def count_entries_in_phasespace(treefilename):
	assert(treefilename.endswith(".root"))
	f=uproot.open(treefilename)
	return f['PhaseSpace'].numentries

def count_ekine_in_phasespace(treefilename,thres):
	assert(treefilename.endswith(".root"))
	f=uproot.open(treefilename)
	arr = f['PhaseSpace/Ekine'].array()
	arr1 = arr[arr>thres]
	return len(arr1)

def profile_ekine_in_phasespace(treefilename,thres=1):
	assert(treefilename.endswith(".root"))
	f=uproot.open(treefilename)
	e,x=f['PhaseSpace'].arrays(["Ekine","X"],outputtype=tuple)
	selx=x[e>1]
	#MPS: 37 bins of 8mm
	#KES: 20 bins of 4mm, divide values by 0.8 to obtain FOV of 10cm, but is done later
	#mid=selx.max()-selx.min()
	x,y=None,None
	if 'iba' in treefilename:
		#half_fov=(20*4)/2.
		selx = selx[-40.<selx]
		selx = selx[selx<40.]
		y,x = np.histogram(selx,bins=20,range=(-40,40))#,range=(mid-half_fov,mid+half_fov))
	elif 'ipnl' in treefilename:
		#half_fov=(37*8)/2.
		selx = selx[-148.<selx] #37*8/2=148
		selx = selx[selx<148.]
		y,x = np.histogram(selx,bins=37,range=(-148,148))#,range=(mid-half_fov,mid+half_fov))
		#print selx.max(),selx.min()
		#print len(selx)
		#print y
	#print len(x),len(y)
	#print x,y
	return [binedges_to_centers(x),y.tolist()]

def thist_to_np_xy_cache(infile,key='reconstructedProfileHisto'):
	assert(infile.endswith(".root"))
	npzfile = infile+"."+str(key)+".npz"
	if os.path.isfile(npzfile):
		cached = np.load(npzfile)
		return [cached['x'].tolist(),cached['y'].tolist()]
	else:
		f=uproot.open(infile)
		outdata_x=binedges_to_centers(f[key].edges)
		outdata_y=f[key].values
		np.savez(npzfile, x=np.array(outdata_x), y=np.array(outdata_y))
		return [outdata_x,outdata_y]

def thist_to_np_xy(infile,key='reconstructedProfileHisto'):
	assert(infile.endswith(".root"))
	f=uproot.open(infile)
	outdata_x=binedges_to_centers(f[key].edges)
	outdata_y=f[key].values
	return [outdata_x,outdata_y]

