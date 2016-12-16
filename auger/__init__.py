import dump, numpy as np,glob2 as glob,copy,scipy
from .plt import *

def getctset(nprim,ct1,ct2,name):
	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':nprim}
	ctset6['ct']['path'] = ct1
	ctset6['rpct']['path'] = ct2
	ctset6['ct']['data'] = []
	ctset6['rpct']['data'] = []
	ctset6['ct']['x'] = []
	ctset6['rpct']['x'] = []
	
	ctset6['ct']['falloff'] = []
	ctset6['rpct']['falloff'] = []
	
	ctset6['ct']['av'] = []
	ctset6['rpct']['av'] = []
	ctset6['ct']['unc'] = []
	ctset6['rpct']['unc'] = []
	ctset6['ct']['uncm'] = []
	ctset6['rpct']['uncm'] = []
	ctset6['ct']['uncp'] = []
	ctset6['rpct']['uncp'] = []
	
	ctset6['ct']['files'] = glob.glob(ct1+"/**/"+name)#+rootn)
	ctset6['rpct']['files'] = glob.glob(ct2+"/**/"+name)#+rootn)

	for ffilen in ctset6['ct']['files']:
		print 'opening',ffilen
		try:
			for key,val in dump.thist2np_xy(ffilen).items():
				if key == 'reconstructedProfileHisto':
					ctset6['ct']['x'] = val[0] #no need to append, is same for all
					ctset6['ct']['data'].append(addnoise(val[1],nprim,name)) #append 'onlynoise' to name for only noise
			#uncomment for plot of fit procedure
			#ctset6['ct']['falloff'].append(ipnl_fit_range(ctset6['ct']['x'],ctset6['ct']['data'][-1],True))
			ctset6['ct']['falloff'].append(ipnl_fit_range(ctset6['ct']['x'],ctset6['ct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
		#break
	for ffilen in ctset6['rpct']['files']:
		print 'opening',ffilen
		try:
			for key,val in dump.thist2np_xy(ffilen).items():
				if key == 'reconstructedProfileHisto':
					ctset6['rpct']['x'] = val[0] #no need to append, is same for all
					ctset6['rpct']['data'].append(addnoise(val[1],nprim,name))
			ctset6['rpct']['falloff'].append(ipnl_fit_range(ctset6['rpct']['x'],ctset6['rpct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
		#break
	
	if len(ctset6['ct']['data']) > 1:
		#we can average
		ndata = np.array(ctset6['ct']['data'])
		ndata = np.rollaxis(ndata,1)
		for binn in ndata:
			(mu, sigma) = scipy.stats.norm.fit(binn) #returns actually sigma, not var.
			ctset6['ct']['av'].append(mu)
			ctset6['ct']['unc'].append(sigma)
			ctset6['ct']['uncm'].append(mu-sigma)
			ctset6['ct']['uncp'].append(mu+sigma)
	else:
		ctset6['ct']['av'] = ctset6['ct']['data'][0]
	if len(ctset6['rpct']['data']) > 1:
		#we can average
		ndata = np.array(ctset6['rpct']['data'])
		ndata = np.rollaxis(ndata,1)
		for binn in ndata:
			(mu, sigma) = scipy.stats.norm.fit(binn) #returns actually sigma, not var.
			ctset6['rpct']['av'].append(mu)
			ctset6['rpct']['unc'].append(sigma)
			ctset6['rpct']['uncm'].append(mu-sigma)
			ctset6['rpct']['uncp'].append(mu+sigma)
			#print (mu, sigma) 
	else:
		ctset6['rpct']['av'] = ctset6['rpct']['data'][0]
	
	return ctset6


def sumctset(name,*cts):
	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':0}
	nrrealisations = len(cts[0]['ct']['data'])
	
	for ctset in cts:
		ctset6['nprim'] += ctset['nprim']
		
		if len(ctset['ct']['data']) != nrrealisations:
			print nrrealisations, 'realizations expected,', len(ctset['ct']['data']), 'encountered. First file in run:', ctset['ct']['files'][0]
			print 'Exiting...'
			quit()
	
	ctset6['ct']['data'] = copy.deepcopy(cts[0]['ct']['data']) #copy first data
	ctset6['rpct']['data'] = copy.deepcopy(cts[0]['rpct']['data'])
	ctset6['ct']['x'] = copy.deepcopy(cts[0]['ct']['x'][:])
	ctset6['rpct']['x'] = copy.deepcopy(cts[0]['rpct']['x'][:])
	
	ctset6['ct']['av'] = []
	ctset6['rpct']['av'] = []
	ctset6['ct']['unc'] = []
	ctset6['rpct']['unc'] = []
	ctset6['ct']['uncm'] = []
	ctset6['rpct']['uncm'] = []
	ctset6['ct']['uncp'] = []
	ctset6['rpct']['uncp'] = []
	ctset6['ct']['falloff'] = []
	ctset6['rpct']['falloff'] = []
	
	for ctset in cts[1:]: #skip first
		for dindex,dataset in enumerate(ctset6['ct']['data']): #only works if number of unc sets are same
			for bindex,binn in enumerate(dataset):
				ctset6['ct']['data'][dindex][bindex] += ctset['ct']['data'][dindex][bindex]

	for ctset in cts[1:]: #skip first
		for dindex,dataset in enumerate(ctset6['rpct']['data']): #only works if number of unc sets are same
			for bindex,binn in enumerate(dataset):
				ctset6['rpct']['data'][dindex][bindex] += ctset['rpct']['data'][dindex][bindex]

	#must remake the avs,uncs,falloffs
	if len(ctset6['ct']['data']) > 1:
		#we can average
		ndata = np.array(ctset6['ct']['data'])
		ndata = np.rollaxis(ndata,1)
		#print ndata.shape
		for binn in ndata:
			(mu, sigma) = scipy.stats.norm.fit(binn) #returns actually sigma, not var.
			ctset6['ct']['av'].append(mu)
			ctset6['ct']['unc'].append(sigma)
			ctset6['ct']['uncm'].append(mu-sigma)
			ctset6['ct']['uncp'].append(mu+sigma)
	else:
		ctset6['ct']['av'] = ctset6['ct']['data'][0]
	if len(ctset6['rpct']['data']) > 1:
		#we can average
		ndata = np.array(ctset6['rpct']['data'])
		ndata = np.rollaxis(ndata,1)
		for binn in ndata:
			(mu, sigma) = scipy.stats.norm.fit(binn) #returns actually sigma, not var.
			ctset6['rpct']['av'].append(mu)
			ctset6['rpct']['unc'].append(sigma)
			ctset6['rpct']['uncm'].append(mu-sigma)
			ctset6['rpct']['uncp'].append(mu+sigma)
			#print (mu, sigma) 
	else:
		ctset6['rpct']['av'] = ctset6['rpct']['data'][0]
		
	for dataset in ctset6['ct']['data']:
		ctset6['ct']['falloff'].append(ipnl_fit_range(ctset6['ct']['x'],dataset))
	
	for dataset in ctset6['rpct']['data']:
		ctset6['rpct']['falloff'].append(ipnl_fit_range(ctset6['rpct']['x'],dataset))
		
	return ctset6


def addnoise(data,nprim,typ):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin               #3-6MeV
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin                #1-8mev
	
	#the tof window is 4ns out of a 10ns period. So, to remove tof from IPNL multiple noise with 2.5, and divide IBA by 2.5 to fake a ToF measurement.
	if 'iba' in typ:
		mu = 5e-7*nprim/2.5 #divided by 2.5 to simulate ToF measurement.
		sigma = 0.5e-7*nprim/2.5
		data = data[::-1]
	elif 'ipnl' in typ:
		mu = 2.5e-7*nprim
		sigma = 0.25e-7*nprim
	if 'notof' in typ: #tof is always in typ...
		mu *= 2.5
		sigma *= 2.5
	retval = []
	for i in data:
		if 'onlynoise' in typ:
			#retval.append(np.random.poisson(np.random.normal(mu,sigma))) # does this mean anything, poisson from gauss?
			retval.append(np.random.poisson(mu))
		else:
			#retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
			retval.append(i + np.random.poisson(mu))
	return retval


def ipnl_fit_range(x,y,plotten=False):
	y=np.array(y)
	
	if plotten: import plot
	if plotten: f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	if plotten: ax1.scatter( x,y, color='black',marker="x",clip_on=False) #bindata
	
	#smooth that shit out.
	#https://en.wikipedia.org/wiki/Smoothing_spline
	y2 = scipy.signal.cspline1d(y,lamb=2)
	y_intpol_f = scipy.interpolate.interp1d(x,y2,kind='cubic') #interpolate function
	x_intpol = np.linspace(x[0],x[-1],1024,endpoint=False)
	y_intpol = y_intpol_f(x_intpol) #interpolate for x_intpol
	y_intpol = y_intpol.clip(min=0) #set any possible negatives to zero
	
	#if plotten: ax1.step(x,y2,color='steelblue', where='mid')
	if plotten: ax1.plot(x_intpol,y_intpol,color='indianred')
	
	#take max
	maxind = np.where(y_intpol == y_intpol.max())[0][-1] #so that we find the LAST index where argmax(y)
	
	if plotten: ax1.axvline(x_intpol[maxind],color='green')
	
	#get 25 percentile, and take mean as baseline.
	baseline = y_intpol[y_intpol < np.percentile(y_intpol, 25)].mean()
	
	if plotten: ax1.axhline(baseline,color='green')
	if plotten: ax1.axhline(y_intpol.max(),color='green')
	
	falloff = y_intpol[maxind]-baseline
	falloff_index=len(x_intpol)-1
	while y_intpol[falloff_index] < 0.5*falloff+baseline:
		falloff_index-=1
	falloff_pos=x_intpol[falloff_index]
	
	if plotten: ax1.axvline(falloff_pos,color='green')
	if plotten: plot.texax(ax1)
	if plotten: ax1.set_xlabel('Depth [mm]', fontsize=8)
	if plotten: ax1.set_ylabel('PG detected [counts]', fontsize=8)
	if plotten: from matplotlib.ticker import MaxNLocator
	if plotten: ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
	if plotten: ax1.set_ylim(bottom=0)
	if plotten: f.savefig('recons.pdf', bbox_inches='tight')
	if plotten: plot.close('all')
	if plotten: quit()
	return falloff_pos
