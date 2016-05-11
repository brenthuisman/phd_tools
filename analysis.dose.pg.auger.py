#!/usr/bin/env python
import os,sys,matplotlib as mpl,matplotlib.pyplot as plt,numpy as np,plot,glob2 as glob,image,pandas as pd
from scipy import interpolate

#detector output
sources = glob.glob("/home/brent/phd/scratch/ct-stage2/fromcluster/**/mergedauger.raw") 
sources += glob.glob("/home/brent/phd/scratch/ct-stage2/fromcluster/**/mergedGammProdCount-Prod.raw") 
#dose
sources += glob.glob("/home/brent/phd/scratch/CT-w-blok/*/output/dosedist-Dose.mhd") 
#PG yield production
sources += glob.glob("/home/brent/phd/scratch/CT-w-blok/fromcluster/**/source.mhd") 


if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print nr, "files found:", sources[:3], '...', sources[-3:]

data_singleton = {}

N=100.*100.

# Load up
for fp in sources:
	if 'gatesim50' not in fp:
		continue #skip

	dn,fn=os.path.split(fp)

	row = {}
	row['replan'] = {}
	row['orig'] = {}

	if fp.endswith(".mhd"):
		im=image.image(fp)
	elif fp.endswith(".raw"):
		im=np.fromfile(fp, dtype='<f4')

	ct = None
	ctname=None
	if 'RPCT' in fp:
		ctname='replan'
		ct = row['replan'] #pointer
	else:
		ctname='orig'
		ct = row['orig'] #pointer

	if 'source.mhd' in fp:
		ct['type'] = 'pg'
		ct['pg'] = im.get1dlist([0,1,1,1])
		# if N == None:
		# 	N = im.header['NDims']#/len(ct['pg'])
		# 	print N
	elif 'dosedist-Dose.mhd' in fp:
		ct['type'] = 'dose'
		msk = image.image( os.path.join(os.path.split(fp)[0],"dosedist-Edep.mhd") )
		msk.to90pcmask()
		im.applymask(msk)
		ct['dose'] = im.get1dlist([0,1,1]) #dose is 3D,removed last index
		row['nprim'] = 1e7 #incorrect
	# elif 'dosedist-Dose-Squared.mhd' in fp:
	# 	ct['type'] = 'dosesq'
	# 	ct['dosesq'] = im.get1dlist([0,1,1])
	# elif 'dosedist-Edep.mhd' in fp:
	# 	ct['type'] = 'doseunc'
	# 	ct['doseunc'] = im.get1dlist([0,1,1])
	elif 'mergedauger.raw' in fp:
		ct['type'] = 'auger'
		ct['auger'] = im
		row['nprim'] = 1e7 #incorrect
	elif 'mergedGammProdCount-Prod.raw' in fp:
		ct['type'] = 'pgprod'
		ct['pgprod'] = im
		row['nprim'] = 1e7 #incorrect
	else:
		continue #skip

	if 'layer' in fp:
		row['loc'] = 'layer'
	elif 'spot' in fp:
		row['loc'] = 'spot'
	else:
		row['loc'] = 'full'

	#nprim
	if 'N24n' in fp:#plan,full
		row['nprim'] = 1e7
	if 'Hsl6' in fp:#plan,layer
		row['nprim'] = 1e7
	if 'YsgV' in fp:#plan,layer
		row['nprim'] = 1e6
		continue
	if 'Z2bG' in fp:#plan,spot
		row['nprim'] = 1e7
	if 'vtwj' in fp:#plan,spot
		row['nprim'] = 1e6
		continue
	if 'y1M5' in fp:#plan,spot
		row['nprim'] = 1e5
		continue

	if 'eTVQ' in fp:#replan,full
		row['nprim'] = 1e7
	if 'qjEk' in fp:#replan,layer
		row['nprim'] = 1e7
	if 'EkjX' in fp:#replan,layer
		row['nprim'] = 1e6
		continue
	if 'CzF4' in fp:#replan,spot
		row['nprim'] = 1e7
	if 'WAKg' in fp:#replan,spot
		row['nprim'] = 1e6
		continue
	if 'LIeR' in fp:#replan,spot
		row['nprim'] = 1e5
		continue

	row['plotgroup'] = row['loc']+str(row['nprim'])
	
	try:
		if row['plotgroup'] not in data_singleton.keys():
			data_singleton[row['plotgroup']] = row
		elif 'dose' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['dose'] = ct['dose']
		elif 'dosesq' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['dosesq'] = ct['dosesq']
		elif 'doseunc' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['doseunc'] = ct['doseunc']
		elif 'pg' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['pg'] = ct['pg']
		elif 'auger' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['auger'] = ct['auger']
		elif 'pgprod' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['pgprod'] = ct['pgprod']
	except KeyError as e:
		print row['plotgroup']
		print data_singleton
		sys.exit(1)

# print data_singleton
# sys.exit(1)
# compute correct unc
# for key, valuee in data_singleton.iteritems():
# 	for value in [valuee['orig'],valuee['replan']]:
# 		data = np.array(value['dose'])
# 		sq = np.array(value['dosesq'])

# 		#mu = np.mean(data)
# 		#N=len(data) #TODO: ik denk dat N=#bins compressed zijn, dus product van de crushed dims
# 		assert len(data) == len(sq)

# 		# # var = sum-of-squares/# - sq(sum/#)
# 		# # var = ( sum([i**2 for i in binn]) / N ) - ( (mu)**2 ) #JM!!!
# 		# if (mean != 0.0 && N != 1 && squared != 0.0){
# 		#   *po = sqrt( (1.0/(N-1))*(squared/N - pow(mean/N, 2)))/(mean/N);
# 		# }
# 		# else *po = 1;
# 		var = []
# 		for sq_i,dose_i in zip(sq,data):
# 			if dose_i > 0 and sq_i >0:
# 				var.append( ( (sq_i / N) - ( (dose_i/N)**2 ) ) / (dosi_N-1) )
# 			else:
# 				var.append(1.)

# 		#print var #var is too small to be interesting, and also negative.
# 		with np.errstate(invalid='ignore'):
# 			#bug! this is always NaN
# 			value['doseunc'] = np.sqrt(np.array(var))
# 			#print value['doseunc']
# 		value['dose-unc'],value['dose+unc'] = plot.geterrorbands(value['doseunc'],value['dose'])

##data is now in order. lets plot!
def fit(ax1,x,y):
	#first, smooth that bitch out
	ysm=pd.rolling_mean(y,30,center=True)
	y=np.nan_to_num(ysm)
	#take max
	maxind = np.argmax(y)
	#go towards end and find 50% thrshold
	nextind=maxind+1
	while y[nextind] > 0.5*y[maxind]:
		nextind+=1
	# go 30 bins left and right and fit within
	hm_left=nextind-100
	hm_right=nextind+100
	xbp=x[hm_left:hm_right]
	ybp=y[hm_left:hm_right]
	tck,u = interpolate.splprep( [xbp,ybp] ,k=5 )#cubic spline
	xnew,ynew = interpolate.splev(  np.linspace( 0, 1, 200 ), tck,der = 0)
	ax1.plot( xbp,ybp,'' , xnew ,ynew )	
	#take mean value in tail-window as minimum
	floor=np.mean(y[hm_right:])
	#take max val in BP window as max
	top=np.max(ybp)
	falloffval_50pc=(top-floor)*.5
	nextind=maxind+1
	while y[nextind] > falloffval_50pc:
		nextind+=1
	print x[nextind]


def plotwunc(ax1,dataset,label=''):
	global color_index
	colors=plot.colors
	x_axis = np.linspace(0,300,150)#300mm,2mm voxels
	x_axis_au = np.linspace(0-7.96*2,300-7.96*2,500)#300mm,2mm voxels

	color_index+=1
	scalepg=np.max(dataset['dose'])/np.max(dataset['pg'])
	scaleau=np.max(dataset['dose'])/np.max(dataset['auger'])
	scalepp=np.max(dataset['dose'])/np.max(dataset['pgprod'])
	ax1.step(x_axis,dataset['pg']*scalepg, label='pg,scaled,'+label, color=colors[color_index], lw=0.5)
	color_index+=1
	#ax1.step(x_axis,dataset['dose'], label='dose,'+label, color=colors[color_index],lw=0.5)
	color_index+=1

	ax1.step(x_axis_au,dataset['auger']*scaleau, label='auger,'+label, color=colors[color_index],lw=0.5)

	#fit(ax1,x_axis_au,dataset['auger']*scaleau)
	#ax1.step(x_axis_au,dataset['pgprod']*scalepp, label='pgprod,'+label, color=colors[color_index],lw=0.5)
	#ax1.step(x_axis,dataset['dose-edep'], label='dose-edep,'+label, color=colors[color_index],lw=0.5)
	#plot.fill_between_steps(ax1,x_axis,dataset['dose-unc'],dataset['dose+unc'],alpha=0.25,color=colors[color_index], lw=0.01)
	

for key, value in data_singleton.iteritems():
	print key
	color_index=0
	f, plo = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=True)

	plotwunc(plo,value['orig'],'orig')
	plotwunc(plo,value['replan'],'replan')
	#ax1.autoscale(axis='x',tight=True)
	plot.texax(plo)

	plo.set_title("Yield")
	# plo.set_ylim([1e-1,1.1e2])
	plo.set_ylabel('Dose [gy], PG Yield [a.u.]')
	plo.set_xlabel('Depth [mm]')
	#plo.xaxis.set_label_coords(1.1,-0.1)

	lgd = plo.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	f.savefig(key+'.pdf', bbox_inches='tight')
	#f.savefig(key+'.png', bbox_inches='tight',dpi=300)
	plt.close('all')
