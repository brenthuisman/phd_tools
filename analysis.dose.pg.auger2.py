#!/usr/bin/env python
import os,sys,re,matplotlib as mpl,matplotlib.pyplot as plt,numpy as np,plot,glob2 as glob,image,pandas as pd
from scipy import interpolate

#detector output
sources = glob.glob("/home/brent/phd/scratch/find-spot-stage2/fromcluster/**/*mergedauger*.raw")
sources += glob.glob("/home/brent/phd/scratch/find-spot-stage2/fromcluster/**/*mergedProd.raw") 
#dose
sources += glob.glob("/home/brent/phd/scratch/find-spot/**/dosedist*Dose.mhd")
#PG yield production
sources += glob.glob("/home/brent/phd/scratch/find-spot/**/source*.mhd")


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

	# if fp.endswith(".mhd"):
	# 	im=image.image(fp)
	# elif fp.endswith(".raw"):
	if fp.endswith(".raw"):
		im=np.fromfile(fp, dtype='<f4')

	ct = None
	ctname=None
	if 'RPCT' in fp:
		ctname='replan'
		ct = row['replan'] #pointer
	else:
		ctname='orig'
		ct = row['orig'] #pointer

	if 'layer' in fp:
		row['loc'] = 'layer'
	elif 'spot' in fp:
		row['loc'] = 'spot'
	else:
		row['loc'] = 'full'
		continue #no full now

	if re.match('source-20(-61)?.mhd',fn):
		im=image.image(fp)
		ct['type'] = 'pg'
		ct['pg'] = im.get1dlist([0,1,1,1])
	elif re.match('dosedist-20(-61)?-Dose.mhd',fn):
		im=image.image(fp)
		ct['type'] = 'dose'
		msk = image.image( fp.replace("Dose.mhd","Edep.mhd") )
		msk.to90pcmask()
		im.applymask(msk)
		ct['dose'] = im.get1dlist([0,1,1]) #dose is 3D,removed last index
	elif 'mergedauger-1.raw' in fn:
		ct['type'] = 'auger18'
		pc=0.03
		im = np.histogram(np.random.choice(range(len(im)),sum(im)*pc,p=im/sum(im)),bins=len(im))[0]
		print row['loc'], "auger18", sum(im)
		ct['auger18'] = im
	elif 'mergedauger-2.raw' in fn:
		ct['type'] = 'auger36'
		pc=0.03
		im = np.histogram(np.random.choice(range(len(im)),sum(im)*pc,p=im/sum(im)),bins=len(im))[0]
		print row['loc'], "auger36", sum(im)
		ct['auger36'] = im
	elif 'Prod.raw' in fn:
		ct['type'] = 'pgprod'
		ct['pgprod'] = im
	else:
		continue #skip

	# if 'merged' in fn:
	# 	row['njob'] = fn.split("merged")[0]

	row['plotgroup'] = row['loc']#+row['njob']
	
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
		elif 'auger18' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['auger18'] = ct['auger18']
		elif 'auger36' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['auger36'] = ct['auger36']
		elif 'pgprod' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['pgprod'] = ct['pgprod']
	except KeyError as e:
		print row['plotgroup']
		print data_singleton
		sys.exit(1)

##data is now in order. lets plot!

def fit_rebin(x,y):
	#take max
	maxind = np.argmax(y)
	#go towards end and find 50% thrshold
	nextind=maxind+1
	while y[nextind] > 0.5*y[maxind]:
		nextind+=1
	# go x bins left and right and fit within
	hm_left=nextind-5
	hm_right=nextind+5
	xbp=x[hm_left:hm_right]
	ybp=y[hm_left:hm_right]
	tck,u = interpolate.splprep( [xbp,ybp] ,k=2 )#cubic spline
	xnew,ynew = interpolate.splev(  np.linspace( 0, 1, 200 ), tck,der = 0)

	#ax1.plot( xbp,ybp,'' , xnew ,ynew )

	#take mean value in tail-window as minimum
	floor=np.mean(y[hm_right:])
	#take max val in BP window as max
	top=np.max(ybp)
	falloffval_50pc=(top-floor)*.5
	nextind=len(ynew)-1
	while ynew[nextind] < falloffval_50pc:
		nextind-=1
	falloffpos = xnew[nextind]
	return falloffpos,[xbp,ybp,'',xnew,ynew]

def fit_smooth(x,y):
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

	#ax1.plot( xbp,ybp,'' , xnew ,ynew )	

	#take mean value in tail-window as minimum
	floor=np.mean(y[hm_right:])
	#take max val in BP window as max
	top=np.max(ybp)
	falloffval_50pc=(top-floor)*.5
	nextind=len(ynew)-1
	while ynew[nextind] < falloffval_50pc:
		nextind-=1
	falloffpos = xnew[nextind]
	return falloffpos,[xbp,ybp,'',xnew,ynew]


def plot_smooth(ax1,dataset,auger,label=''):
	#auger = 'auger18'
	#auger = 'auger36'
	
	global color_index
	colors=plot.colors
	x_axis = np.linspace(0,300,150)#300mm,2mm voxels, shift already compensated for
	##remove shift with new data!!!!
	#x_axis_au = np.linspace(0+7.96,250+7.96,500)#250mm in 500 bins!!!!
	x_axis_au = np.linspace(0,250,500)#250mm in 500 bins!!!!

	color_index+=1
	scalepg=np.max(dataset['dose'])/np.max(dataset['pg'])
	scaleau=np.max(dataset['dose'])/np.max(dataset[auger])
	scalepp=np.max(dataset['dose'])/np.max(dataset['pgprod'])
	#ax1.step(x_axis,dataset['pg']*scalepg, label='pg,scaled,'+label, color=colors[color_index], lw=0.5)
	color_index+=1
	ax1.step(x_axis,dataset['dose'], label='dose,'+label, color=colors[color_index],lw=0.5)
	color_index+=1

	ax1.step(x_axis_au,dataset[auger]*scaleau, label=auger+','+label, color=colors[color_index],lw=0.5)

	falloff,fitplot=fit_smooth(x_axis_au,dataset[auger]*scaleau)
	print auger, falloff
	ax1.plot(*fitplot)
	#ax1.step(x_axis_au,dataset['pgprod']*scalepp, label='pgprod,'+label, color=colors[color_index],lw=0.5)
	#ax1.step(x_axis,dataset['dose-edep'], label='dose-edep,'+label, color=colors[color_index],lw=0.5)
	#plot.fill_between_steps(ax1,x_axis,dataset['dose-unc'],dataset['dose+unc'],alpha=0.25,color=colors[color_index], lw=0.01)
	


def plot_rebin(ax1,dataset,auger,label=''):
	#auger = 'auger18'
	#auger = 'auger36'

	global color_index
	colors=plot.colors
	x_axis = np.linspace(0,300,150)#300mm,2mm voxels, shift already compensated for
	##remove shift with new data!!!!
	#x_axis_au = np.linspace(0+7.96,250+7.96,500)#250mm in 500 bins!!!!
	x_axis_au = np.linspace(0,250,500)#250mm in 500 bins!!!!

	color_index+=1
	scalepg=np.max(dataset['dose'])/np.max(dataset['pg'])
	scaleau=np.max(dataset['dose'])/np.max(dataset[auger])
	scalepp=np.max(dataset['dose'])/np.max(dataset['pgprod'])
	#ax1.step(x_axis,dataset['pg']*scalepg, label='pg,scaled,'+label, color=colors[color_index], lw=0.5)
	color_index+=1
	ax1.step(x_axis,dataset['dose'], label='dose,'+label, color=colors[color_index],lw=0.5)
	color_index+=1

	augerdata=[] #rebin to 1 bin / 10mm
	for i in range(len(dataset[auger]))[::20]:
		augerdata.append(sum(dataset[auger][i:i+20]))
	scaleau=np.max(dataset['dose'])/np.max(augerdata)
	augerdata=np.array(augerdata)*scaleau
	ax1.step(x_axis_au,augerdata, label=auger+','+label, color=colors[color_index],lw=0.5)

	falloff,fitplot=fit_rebin(x_axis_au,augerdata)
	print falloff
	ax1.plot(*fitplot)
	#fit(ax1,x_axis_au,dataset[auger]*scaleau)
	#ax1.step(x_axis_au,dataset['pgprod']*scalepp, label='pgprod,'+label, color=colors[color_index],lw=0.5)
	#ax1.step(x_axis,dataset['dose-edep'], label='dose-edep,'+label, color=colors[color_index],lw=0.5)
	#plot.fill_between_steps(ax1,x_axis,dataset['dose-unc'],dataset['dose+unc'],alpha=0.25,color=colors[color_index], lw=0.01)



def get_corr(dataset,label=''):
	x_axis = np.linspace(0,300,150)
	x_axis_au = np.linspace(0,250,500)
	
	dos_pl=dataset['orig']['dose']
	dos_rp=dataset['replan']['dose']
	aug1_pl=dataset['orig']['auger18']
	aug1_rp=dataset['replan']['auger18']
	aug2_pl=dataset['orig']['auger36']
	aug2_rp=dataset['replan']['auger36']

	def get_corr_factor(arr1,arr2,xarr):
		#get falloff and get y-axis of each fit.
		binsize=xarr[1]-xarr[0] #one bin is binsize mm

		falloff1,fitplot1=fit_smooth(xarr,arr1)
		falloff2,fitplot2=fit_smooth(xarr,arr2)

		#print falloff1, falloff2
		shift_mm = falloff1-falloff2
		shift = int(shift_mm/binsize) #need know shift in number of bins
		#return shift_mm,shift
		
		#check corr for unshifted data
		fitdat1 = fitplot1[-1]
		fitdat2 = fitplot2[-1]
		print "Unshifted correlation:",np.corrcoef(fitdat1,fitdat2)[0,1]

		# apply shift by cutting off bins from the correct size. if 0 bins, no shift.
		if shift<0:
			fitdat1=fitdat1[:shift]
			fitdat2=fitdat2[-shift:]
		elif shift>0:
			fitdat1=fitdat1[shift:]
			fitdat2=fitdat2[:-shift]

		#normalize
		fitdat1_norm = np.convolve(fitdat1,np.ones(len(fitdat1))/len(fitdat1),'same')
		fitdat2_norm = np.convolve(fitdat2,np.ones(len(fitdat2))/len(fitdat2),'same')

		#return shift and get coeff
		return shift_mm,np.corrcoef(fitdat1_norm,fitdat2_norm)[0,1]

	#print "Dose", get_corr_factor(dos_pl,dos_rp,x_axis)
	print "aug 1-8mev", get_corr_factor(aug1_pl,aug1_rp,x_axis_au)
	print "aug 3-6mev", get_corr_factor(aug2_pl,aug2_rp,x_axis_au)



for key, value in data_singleton.iteritems():
	print key
	color_index=0
	f, (pl,pr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=True)

	plot_smooth(pl,value['orig'],'auger18','orig')
	plot_smooth(pl,value['replan'],'auger18','replan')
	plot_smooth(pr,value['orig'],'auger36','orig')
	plot_smooth(pr,value['replan'],'auger36','replan')
	get_corr(value)

	plot.texax(pl)
	plot.texax(pr)

	pl.set_title("Yield")
	# plo.set_ylim([1e-1,1.1e2])
	pl.set_ylabel('Dose [gy], PG Yield [a.u.]')
	pl.set_xlabel('Depth [mm]')
	#plo.xaxis.set_label_coords(1.1,-0.1)

	lgd = pl.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	lgd = pr.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	f.savefig(key+'.pdf', bbox_inches='tight')
	#f.savefig(key+'.png', bbox_inches='tight',dpi=300)
	plt.close('all')
