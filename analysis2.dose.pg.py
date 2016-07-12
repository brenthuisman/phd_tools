#!/usr/bin/env python
import os,sys,re,matplotlib as mpl,matplotlib.pyplot as plt,numpy as np,plot,glob2 as glob,image,pandas as pd
from scipy import interpolate,signal

#detector output
sources = glob.glob("/home/brent/phd/scratch/find-spot-stage2/fromcluster/*auger.merged.raw") 
#dose
sources += glob.glob("/home/brent/phd/scratch/find-spot/**/dosedist*Dose.mhd")

rundefs= {	"9P19": ["orig","lay0","4.73"],
			"aEUT": ["replan","lay0","4.73"],
			"fE9t": ["orig","lay10","13.31"],
			"AXu6": ["replan","lay10","13.31"],
			"eKX7": ["orig","lay20","18.8"],
			"2SV6": ["replan","lay20","18.8"],
			"4qJv": ["orig","lay30","9.88"],
			"oyzA": ["replan","lay30","9.88"],
			"RsPP": ["orig","lay38","7.77"],
			"HtFv": ["replan","lay38","7.77"],
}

if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print nr, "files found:", sources[:3], '...', sources[-3:]

data_singleton = {}

def addneutronnoise(y):
	floor = np.nanmean(y[:4]+y[-4:])
	mu, sigma = floor , np.sqrt(floor)
	noise = [int(x) for x in np.random.normal(mu, sigma, len(y))]
	return np.nansum([y,noise],axis=0) #piecewise sum

# Load up
for fp in sources:
	dn,fn=os.path.split(fp)

	row = {}
	row['replan'] = {}
	row['orig'] = {}

	ct = None
	ctname=None

	if 'dosedist' in fp:
		if 'layer' in fp:
			if 'RPCT' in fp:
				ctname='replan'
				ct = row['replan'] #pointer
			else:
				ctname='orig'
				ct = row['orig'] #pointer
		else:
			continue #only load layers

	if fn.endswith(".raw"):
		im=addneutronnoise(np.fromfile(fp, dtype='<f4'))
		#im=np.fromfile(fp, dtype='<f4')
		run = fn.split(".")[1]
		try:
			row['loc'] = rundefs[run][1]
			row['CMU'] = rundefs[run][2]
		except:
			continue
		if rundefs[run][0] == 'orig':
			ctname='orig'
			ct = row['orig'] #pointer
		if rundefs[run][0] == 'replan':
			ctname='replan'
			ct = row['replan'] #pointer

	if re.match('dosedist-\d{1,2}-Dose.mhd',fn):
		row['loc'] = 'lay'+str(re.findall('\d{1,2}',fn)[0])
		im=image.image(fp)
		ct['type'] = 'dose'
		msk = image.image( fp.replace("Dose.mhd","Edep.mhd") )
		msk.to90pcmask()
		im.applymask(msk)
		ct['dose'] = im.get1dlist([0,1,1]) #dose is 3D,removed last index
	elif 'ipnl' in fn and 'auger' in fn:
		ct['type'] = 'ipnl'
		ct['ipnl'] = im
	elif 'iba' in fn and 'auger' in fn:
		ct['type'] = 'iba'
		ct['iba'] = im[::-1] #turn that thing around!
	else:
		continue #skip

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
		elif 'ipnl' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['ipnl'] = ct['ipnl']
		elif 'iba' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['iba'] = ct['iba']
		elif 'pgprod' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['pgprod'] = ct['pgprod']
	except KeyError as e:
		print fn
		print ct['type']
		print row['plotgroup']
		#print data_singleton
		sys.exit(1)

	if fn.endswith(".raw"):
		run = fn.split(".")[1]
		try:
			data_singleton[row['plotgroup']]['CMU']=rundefs[run][2]
		except:
			pass

##data is now in order. lets plot!

def fit(ax1,x,y):
	assert len(x) == len(y)
	scale=max(y)
	y = [yy/scale for yy in y] #scale down or interpolate fucks up...
	#take max,tail,halfdiff
	maxind = np.argmax(y)
	tail = np.mean(y[-3:])
	halfdiff = tail+0.5*( np.max(y)-tail )
	#go from back towards halfdiff
	nextind=len(y)-1
	while y[nextind] < halfdiff:
		nextind-=1
	#fit on interval max to floor. find where floor ends (tail+10% of halfdiff)
	floorind=len(y)-1
	while y[floorind] < tail+0.1*halfdiff:
		floorind-=1
	assert maxind < floorind
	hm_left= maxind-5
	hm_right= floorind
	xbp=x[hm_left:hm_right]
	ybp=y[hm_left:hm_right]
	#fit that bitch
	spl = interpolate.UnivariateSpline( xbp,ybp , s=None, k=2)
	xnew = np.linspace( xbp[0], xbp[-1], 1000 )
	ynew = spl(xnew)
	
	# find falloff on ynew, but there where halfdiff is on y (floorind)
	falloffpos=0
	nextind=len(ynew)-1
	while ynew[nextind] < halfdiff:
		nextind-=1
	falloffpos = xnew[nextind]
	#scale back up
	ybp = [yy*scale for yy in ybp]
	ynew = [yy*scale for yy in ynew]

	#ax1.plot( xbp,ybp,'' , xnew ,ynew )
	ax1.plot( xnew ,ynew )
	ax1.axvline(falloffpos, color='#999999', ls='--')

	return falloffpos,[xbp,ybp,'',nextind,xnew,ynew]

color_index = 0
def plotter(ax1,dataset,field,label=''):
	global color_index
	colors=plot.colors
	if 'dose' in field:
		x_axis = np.linspace(0,300,150)#300mm,2mm voxels
	elif 'iba' in field:
		x_axis = np.linspace(0,80,20)#250mm in 500 bins!!!!
	else: #ipnl
		x_axis = np.linspace(0,250,28)#250mm in 500 bins!!!!

	color_index+=1
	ax1.step(x_axis,dataset[field], label=field+label, color=colors[color_index],lw=0.5)

color_index = 0
def plotter2(ax1,dataset,field,label=''):
	global color_index
	colors=plot.colors
	if 'dose' in field:
		x_axis = np.linspace(0,300,150)#300mm,2mm voxels
	elif 'iba' in field:
		x_axis = np.linspace(0,80,20)#250mm in 500 bins!!!!
	else: #ipnl
		x_axis = np.linspace(0,250,28)#250mm in 500 bins!!!!

	color_index+=1
	ax1.step(x_axis,dataset, label=label, color=colors[color_index],lw=0.5)


def get_corr_factor(ax1,arr1,arr2,xarr):
	#resample
	arr1=signal.resample(arr1,1000)[50:950] #chop of wavy ends
	arr2=signal.resample(arr2,1000)[50:950]
	fitdat1=arr1
	xarr=signal.resample(xarr,1000)[50:950]
	fitdat2=arr2

	#get falloff and get y-axis of each fit.
	falloff1,fitplot1=fit(ax1,xarr,arr1)
	falloff2,fitplot2=fit(ax1,xarr,arr2)

	#get shift
	shift_mm = falloff2-falloff1

	# correlation at registration:

	#normalize
	fitdat1_norm = np.convolve(fitdat1,np.ones(len(fitdat1))/len(fitdat1),'same')
	fitdat2_norm = np.convolve(fitdat2,np.ones(len(fitdat2))/len(fitdat2),'same')
	
	#check corr for unshifted data
	corr_before=np.corrcoef(fitdat1_norm,fitdat2_norm)[0,1]
	print "Unshifted correlation:",corr_before

	#get shift in nr bins
	#binsize=fitplot1[-2][1]-fitplot1[-2][0] #one bin is binsize mm
	binsize=xarr[1]-xarr[0] #one bin is binsize mm
	shift = int(shift_mm/binsize)
	#shift = fitdat2[fitplot2[-3]]-fitdat1[fitplot1[-3]]
	#print shift

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
	corr_after=np.corrcoef(fitdat1_norm,fitdat2_norm)[0,1]
	print "Shifted correlation:",corr_after
	return shift_mm,corr_before,corr_after


def formatlabel(*argies):
	return "\nShift "+str(argies[0])+"\nCorr bef:"+str(argies[1])[2:7]+"%\nCorr af:"+str(argies[2])[2:7]+'%'


## start aplottin

## first barplot setup
barf, (barax1,barax2) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
N = len(data_singleton.keys())
ind = np.arange(N)                # the x locations for the groups
width = 0.25                      # the width of the bars
dosebar=[]
ipnlbar=[]
ibabar=[]
dosebar2=[]
ipnlbar2=[]
ibabar2=[]
labelbar=[]


#now dose-pg layer plots
for key, value in data_singleton.iteritems():
	print key,value['CMU']
	color_index=0
	f, (pl,pm,pr) = plt.subplots(nrows=1, ncols=3, sharex=False, sharey=False)

	dose_shift,dose_corr_bef,dose_corr_af = get_corr_factor(pl,value['orig']['dose'],value['replan']['dose'],np.linspace(0,300,150))
	ipnl_shift,ipnl_corr_bef,ipnl_corr_af = get_corr_factor(pm,value['orig']['ipnl'],value['replan']['ipnl'],np.linspace(0,250,28))
	iba_shift,iba_corr_bef,iba_corr_af = get_corr_factor(pr,value['orig']['iba'],value['replan']['iba'],np.linspace(0,80,20))

	dosebar.append(dose_shift)
	ipnlbar.append(ipnl_shift)
	ibabar.append(iba_shift)
	dosebar2.append(dose_corr_af)#-dose_corr_bef)
	ipnlbar2.append(ipnl_corr_af)#-ipnl_corr_bef)
	ibabar2.append(iba_corr_af)#-iba_corr_bef)
	labelbar.append(key+", CMU:"+value['CMU'])

	plotter(pl,value['orig'],'dose','orig')
	plotter(pl,value['replan'],'dose',formatlabel(dose_shift,dose_corr_bef,dose_corr_af))
	plotter(pm,value['orig'],'ipnl','orig')
	plotter(pm,value['replan'],'ipnl',formatlabel(ipnl_shift,ipnl_corr_bef,ipnl_corr_af))
	plotter(pr,value['orig'],'iba','orig')
	plotter(pr,value['replan'],'iba',formatlabel(iba_shift,iba_corr_bef,iba_corr_af))

	plot.texax(pl)
	plot.texax(pm)
	plot.texax(pr)

	pl.set_title("Dose")
	pm.set_title("PG IPNL")
	pr.set_title("PG IBA")
	# plo.set_ylim([1e-1,1.1e2])
	pl.set_ylabel('Dose [gy], PG Yield [counts]')
	pl.set_xlabel('Depth [mm]')
	#plo.xaxis.set_label_coords(1.1,-0.1)

	lgd = pl.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	lgd = pm.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	lgd = pr.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	#f.savefig(key+'.pdf', bbox_inches='tight')
	f.savefig(key+'.png', bbox_inches='tight',dpi=300)
	#plt.close('all')


## finish barplot
rects1 = barax1.bar(ind, dosebar, width, color='black')
rects2 = barax1.bar(ind+width, ipnlbar, width, color='red')
rects3 = barax1.bar(ind+2*width, ibabar, width, color='green')
rects4 = barax2.bar(ind, dosebar2, width, color='black')
rects5 = barax2.bar(ind+width, ipnlbar2, width, color='red')
rects6 = barax2.bar(ind+2*width, ibabar2, width, color='green')

# axes and labels
barax1.set_xlim(-width,len(ind)+width)
barax1.set_ylabel('Shift [mm]')
barax1.set_title('Shifts per layer')
xTickMarks = labelbar
barax1.set_xticks(ind+width)
xtickNames = barax1.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax1)

# axes and labels2
barax2.set_xlim(-width,len(ind)+width)
barax2.set_ylabel('Diff Corr factor')
barax2.set_title('Corr Factor')
#barax2.semilogy()
xTickMarks = labelbar
barax2.set_xticks(ind+width)
xtickNames = barax2.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax2)

## add a legend
barax1.legend( (rects1[0], rects2[0], rects3[0]), ('Dose', 'IPNL', 'IBA') )
barax2.legend( (rects4[0], rects5[0], rects6[0]), ('Dose', 'IPNL', 'IBA') )

barf.savefig('shifts.png', bbox_inches='tight',dpi=300)


## Now, vary number of prot


## first barplot setup
barf, (barax1,barax2) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
N = 3 #3 outputs
ind = np.arange(N)                # the x locations for the groups
width = 0.25                      # the width of the bars
shift0bar=[]
shift10bar=[]
shift100bar=[]
shift0bar2=[]
shift10bar2=[]
shift100bar2=[]
labelbar=['noreduc','0.1','0.01']


value = data_singleton['lay0']
for typ in ['dose','ipnl','iba']:
	f, (pl,pm,pr) = plt.subplots(nrows=1, ncols=3, sharex=False, sharey=False)
	color_index=0
	
	if 'dose' in typ:
		x_axis = np.linspace(0,300,150)#300mm,2mm voxels
	elif 'iba' in typ:
		x_axis = np.linspace(0,80,20)#250mm in 500 bins!!!!
	else: #ipnl
		x_axis = np.linspace(0,250,28)#250mm in 500 bins!!!!

	im=value['orig'][typ]
	reduc0 = im
	reduc10 = np.histogram(np.random.choice(range(len(im)),sum(im)*0.1,p=im/sum(im)),bins=len(im))[0]
	reduc100 = np.histogram(np.random.choice(range(len(im)),sum(im)*0.01,p=im/sum(im)),bins=len(im))[0]
	im2=value['replan'][typ]
	rpreduc0 = im2
	rpreduc10 = np.histogram(np.random.choice(range(len(im2)),sum(im2)*0.1,p=im2/sum(im2)),bins=len(im2))[0]
	rpreduc100 = np.histogram(np.random.choice(range(len(im2)),sum(im2)*0.01,p=im2/sum(im2)),bins=len(im2))[0]

	shift0,corr_bef0,corr_af0 = get_corr_factor(pl,reduc0,rpreduc0,x_axis)
	shift10,corr_bef10,corr_af10 = get_corr_factor(pm,reduc10,rpreduc10,x_axis)
	shift100,corr_bef100,corr_af100 = get_corr_factor(pr,reduc100,rpreduc100,x_axis)

	shift0bar.append(shift0)
	shift10bar.append(shift10)
	shift100bar.append(shift100)
	shift0bar2.append(corr_af0)#-corr_bef0)
	shift10bar2.append(corr_af10)#-corr_bef10)
	shift100bar2.append(corr_af100)#-corr_bef100)

	plotter2(pl,reduc0,typ,'noreduc')
	plotter2(pl,rpreduc0,typ,'noreduc')
	plotter2(pm,reduc10,typ,'0.1')
	plotter2(pm,rpreduc10,typ,'0.1')
	plotter2(pr,reduc100,typ,'0.01')
	plotter2(pr,rpreduc100,typ,'0.01')

	plot.texax(pl)
	plot.texax(pm)
	plot.texax(pr)

	pl.set_title("noreduc")
	pm.set_title("0.1")
	pr.set_title("0.01")
	# plo.set_ylim([1e-1,1.1e2])
	pl.set_ylabel('Dose [gy], PG Yield [counts]')
	pl.set_xlabel('Depth [mm]')
	#plo.xaxis.set_label_coords(1.1,-0.1)

	lgd = pl.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	lgd = pm.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	lgd = pr.legend(loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	#f.savefig(typ+'.pdf', bbox_inches='tight')
	f.savefig(typ+'.png', bbox_inches='tight',dpi=300)
	#plt.close('all')


## finish barplot
rects1 = barax1.bar(ind, shift0bar, width, color='black')
rects2 = barax1.bar(ind+width, shift10bar, width, color='red')
rects3 = barax1.bar(ind+2*width, shift100bar, width, color='green')
rects4 = barax2.bar(ind, shift0bar2, width, color='black')
rects5 = barax2.bar(ind+width, shift10bar2, width, color='red')
rects6 = barax2.bar(ind+2*width, shift100bar2, width, color='green')

# axes and labels
barax1.set_xlim(-width,len(ind)+width)
barax1.set_ylabel('Shift [mm]')
barax1.set_title('Shifts per layer')
xTickMarks = labelbar
barax1.set_xticks(ind+width)
xtickNames = barax1.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax1)

# axes and labels2
barax2.set_xlim(-width,len(ind)+width)
barax2.set_ylabel('Diff Corr factor')
barax2.set_title('Corr Factor')
xTickMarks = labelbar
barax2.set_xticks(ind+width)
xtickNames = barax2.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax2)

## add a legend
barax1.legend( (rects1[0], rects2[0], rects3[0]), ('dose','ipnl','iba') )
barax2.legend( (rects4[0], rects5[0], rects6[0]), ('dose','ipnl','iba') )

barf.savefig('shifts2.png', bbox_inches='tight',dpi=300)
