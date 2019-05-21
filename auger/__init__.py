import dump, numpy as np,glob2 as glob,copy,scipy
from .plt import *

def getctset(nprim,ct1,ct2,name,**kwargs):
	if 'manualshift' in kwargs:
		manualshift = kwargs['manualshift']
	else:
		manualshift = 0.

	if 'addnoise' not in kwargs:
		kwargs['addnoise'] = True

	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':nprim}
	ctset6['ct']['label'] = 'CT'
	ctset6['rpct']['label'] = 'RPCT'

	ctset6['ct']['path'] = ct1
	ctset6['rpct']['path'] = ct2
	ctset6['ct']['data'] = []
	ctset6['rpct']['data'] = []
	ctset6['ct']['x'] = []
	ctset6['rpct']['x'] = []

	ctset6['ct']['falloff'] = []
	ctset6['rpct']['falloff'] = []

	ctset6['ct']['fow'] = []
	ctset6['rpct']['fow'] = []

	ctset6['ct']['contrast'] = []
	ctset6['rpct']['contrast'] = []

	ctset6['ct']['av'] = []
	ctset6['rpct']['av'] = []
	ctset6['ct']['unc'] = []
	ctset6['rpct']['unc'] = []
	ctset6['ct']['uncm'] = []
	ctset6['rpct']['uncm'] = []
	ctset6['ct']['uncp'] = []
	ctset6['rpct']['uncp'] = []

	ctset6['ct']['files'] = glob.glob(ct1+"/**/"+name)
	ctset6['rpct']['files'] = glob.glob(ct2+"/**/"+name)

	print '==== Report ===='
	print ct1, len(ctset6['ct']['files'])
	print ct2, len(ctset6['rpct']['files'])
	if len(ctset6['ct']['files']) == 0:
		print ct1,name
	print '==== ====== ===='

	for ffilen in ctset6['ct']['files']:
		print 'opening',ffilen
		try:
			data = dump.thist_to_np_xy(ffilen,'reconstructedProfileHisto')
			ctset6['ct']['x'] = scale_bincenters(data[0],name,manualshift) #no need to append, is same for all. are bincenters
			ctset6['ct']['data'].append(addnoise(data[1],nprim,name,**kwargs)) #append 'onlynoise' to name for only noise
			ctset6['ct']['falloff'].append(get_fop(ctset6['ct']['x'],ctset6['ct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
		#break
	for ffilen in ctset6['rpct']['files']:
		print 'opening',ffilen
		try:
			data = dump.thist_to_np_xy(ffilen,'reconstructedProfileHisto')
			ctset6['rpct']['x'] = scale_bincenters(data[0],name,manualshift) #no need to append, is same for all. are bincenters
			ctset6['rpct']['data'].append(addnoise(data[1],nprim,name,**kwargs))
			ctset6['rpct']['falloff'].append(get_fop(ctset6['rpct']['x'],ctset6['rpct']['data'][-1]))
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

	ctset6['fodiff']=[]
	for i in range(len(ctset6['ct']['data'])):
		foct=ctset6['ct']['falloff'][i]
		for i in range(len(ctset6['rpct']['data'])):
			forpct=ctset6['rpct']['falloff'][i]
			ctset6['fodiff'].append(forpct-foct)

	ctset6['detyieldmu'] = np.mean([sum(real) for real in ctset6['ct']['data']+ctset6['rpct']['data']])/nprim
	ctset6['detyieldsigma'] = np.std([sum(real) for real in ctset6['ct']['data']+ctset6['rpct']['data']])/nprim

	ctset6['detcount'] = np.mean([sum(real) for real in ctset6['ct']['data']+ctset6['rpct']['data']])

	if 'precolli' in kwargs and kwargs['precolli']==True:
		precs=[]
		txtfiles = glob.glob(ct1+"/**/*pre.root.txt")
		for txtfile in txtfiles:
			precs.append(dump.readtxtnumber(txtfile))
		prec=np.mean(precs)
		ctset6['precollidetyieldmu'] = np.mean([sum(real) for real in ctset6['ct']['data']+ctset6['rpct']['data']])/prec
		ctset6['precollidetyieldsigma'] = np.std([sum(real) for real in ctset6['ct']['data']+ctset6['rpct']['data']])/prec

	ctset6['nreal'] = len(ctset6['ct']['data']+ctset6['rpct']['data'])
	ctset6['totnprim'] = len(ctset6['ct']['data']+ctset6['rpct']['data'])*nprim

	ctset6['ct']['fopmu'] = np.mean(ctset6['ct']['falloff'])
	ctset6['ct']['fopsigma'] = np.std(ctset6['ct']['falloff'])
	ctset6['rpct']['fopmu'] = np.mean(ctset6['rpct']['falloff'])
	ctset6['rpct']['fopsigma'] = np.std(ctset6['rpct']['falloff'])
	ctset6['fodiffmu'] = np.mean(ctset6['fodiff'])

	#ctset6['ct']['fowmu'] = np.mean(ctset6['ct']['fow'])
	#ctset6['ct']['fowsigma'] = np.std(ctset6['ct']['fow'])
	#ctset6['rpct']['fowmu'] = np.mean(ctset6['rpct']['fow'])
	#ctset6['rpct']['fowsigma'] = np.std(ctset6['rpct']['fow'])

	#ctset6['ct']['contrastmu'] = np.mean(ctset6['ct']['contrast'])
	#ctset6['ct']['contrastsigma'] = np.std(ctset6['ct']['contrast'])
	#ctset6['rpct']['contrastmu'] = np.mean(ctset6['rpct']['contrast'])
	#ctset6['rpct']['contrastsigma'] = np.std(ctset6['rpct']['contrast'])

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
		ctset6['ct']['falloff'].append(get_fop(ctset6['ct']['x'],dataset))

	for dataset in ctset6['rpct']['data']:
		ctset6['rpct']['falloff'].append(get_fop(ctset6['rpct']['x'],dataset))

	return ctset6


def addnoise(data,nprim,typ,**kwargs):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin               #>1MeV
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin                #3-6mev
	#IBA: \cite{Perali2014}: 2.651e-06 per prot per 4mm bin                     #1-8mev

	#the tof window is 4ns out of a 10ns period. So, to remove tof from IPNL multiple noise with 2.5, and divide IBA by 2.5 to fake a ToF measurement.
	if 'iba' in typ:
		#mu = 5e-7*nprim/2.5 #divided by 2.5 to simulate ToF measurement.
		#sigma = 0.5e-7*nprim/2.5
		mu = 2.651e-06*nprim/2.5 #divided by 2.5 to simulate ToF measurement.
		sigma = 2.651e-7*nprim/2.5
		data = data[::-1]
	elif 'ipnl' in typ:
		mu = 2.5e-7*nprim
		sigma = 0.25e-7*nprim
	if 'notof' in typ: #tof is always in typ...
		mu *= 2.5
		sigma *= 2.5
	retval = []
	for i in data:
		if kwargs['addnoise'] == 'onlynoise':
			#retval.append(np.random.poisson(np.random.normal(mu,sigma))) # does this mean anything, poisson from gauss?
			retval.append(np.random.poisson(mu))
		elif kwargs['addnoise'] == False:
			#retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
			retval.append(i)
		elif kwargs['addnoise'] == True: #normal situation
			#retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
			retval.append(i + np.random.poisson(mu))
		else:
			raise ValueError("addnoise setting does not match any known possiblity (True|False|'onlynoise')")
	return retval

def scale_bincenters(xax,typ,shift):
	xax = np.array(xax)+shift
	if 'iba' in typ:
		return [i/0.8 for i in xax]
	elif 'ipnl' in typ:
		return xax


def get_fop(x,y,**kwargs):
	plotten = False
	plottenname = ''
	label=''
	threshold = 0.5
	ax1 = ''
	smooth=True
	fitlines=False
	globmax=False
	if 'plot' in kwargs:
		plotten = True
		fitlines = True
		plottenname = str(kwargs['plot'])
		import plot
	if 'threshold' in kwargs:
		threshold = float(kwargs['threshold'])
	if 'globmax' in kwargs:
		globmax = float(kwargs['globmax'])
	if 'ax' in kwargs:
		if plotten == True:
			ax1 = kwargs['ax']
		else:
			return
	if 'smooth' in kwargs:
		smooth = kwargs['smooth']
	if 'label' in kwargs:
		label = kwargs['label']
	if 'fitlines' in kwargs:
		fitlines = kwargs['fitlines']

	y=np.array(y)

	#if plotten: import plot
	#if plotten: f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	if plotten: ax1.scatter( x,y, color='black',marker="x",clip_on=False) #bindata

	#smooth that shit out.
	#https://en.wikipedia.org/wiki/Smoothing_spline
	y2 = scipy.signal.cspline1d(y,lamb=2)
	y_intpol_f = scipy.interpolate.interp1d(x,y2,kind='cubic') #interpolate function
	x_intpol = np.linspace(x[0],x[-1],2048,endpoint=False)
	y_intpol = y_intpol_f(x_intpol) #interpolate for x_intpol
	y_intpol = y_intpol.clip(min=0) #set any possible negatives to zero

	#if plotten: ax1.step(x,y2,color='steelblue', where='mid')
	if plotten: ax1.plot(x_intpol,y_intpol,color='indianred')

	#get 25 percentile, and take mean as baseline.
	baseline = y_intpol[y_intpol < np.percentile(y_intpol, 25)].mean()

	maxind=0
	if globmax:
		maxind = np.where(y_intpol == y_intpol.max())[0][-1] #so that we find the LAST index where argmax(y)
	else:
		#global max
		globmaxind = np.where(y_intpol == y_intpol.max())[0][-1]
		globfalloff = y_intpol[globmaxind]-baseline

		#find distal local max within 30% of FO
		maxind = np.sort( scipy.signal.argrelextrema(y_intpol, np.greater)[0] )[::-1]
		for locmac in maxind[::-1]: #search from back
			if y_intpol[locmac] > (baseline+globfalloff*0.3):
				maxind = locmac
		#if fitlines: ax1.axhline(baseline+globfalloff*0.3,color='green')

	falloff = y_intpol[maxind]-baseline
	falloff_index=len(x_intpol)-1
	print falloff
	try:
		while y_intpol[falloff_index] < threshold*falloff+baseline: #default threshold is 0.5
			falloff_index-=1
	except ValueError:
		print y_intpol[falloff_index] < threshold*falloff+baseline
		print y_intpol[falloff_index]
		print threshold
		print falloff
		print baseline

	falloff_pos=x_intpol[falloff_index]

	if fitlines: ax1.axvline(falloff_pos,color='green')
	if fitlines: ax1.axhline(baseline,color='green')
	if fitlines: ax1.axhline(y_intpol[maxind],color='green')
	if fitlines: ax1.axvline(x_intpol[maxind],color='green')

	if plotten: plot.texax(ax1)
	if plotten: ax1.set_xlabel('Position [mm]', fontsize=8)
	if plotten: ax1.set_ylabel('PG yield [counts]', fontsize=8)
	if plotten: from matplotlib.ticker import MaxNLocator
	if plotten: ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
	if plotten: ax1.set_ylim(bottom=0)
	#if plotten: ax1.set_title('FOP = '+str(falloff_pos), fontsize=8)
	#if plotten: f.savefig(plottenname, bbox_inches='tight')
	#if plotten: print 'Plotted PG profile to',plottenname
	#if plotten: plot.close('all')
	if plotten: print 'FOP is',falloff_pos
	#if plotten: quit()
	return falloff_pos


def get_fop_fow_contrast(x,y,**kwargs):
	plotten = False
	plottenname = ''
	label=''
	threshold = 0.5
	ax1 = ''
	smooth=2
	fitlines=False
	globmax=False
	filename = ''
	nokillax3=True
	if 'filename' in kwargs:
		filename = kwargs['filename']
	if 'plot' in kwargs:
		plotten = True
		fitlines = True
		plottenname = str(kwargs['plot'])
		import plot
	if 'threshold' in kwargs:
		threshold = float(kwargs['threshold'])
	if 'globmax' in kwargs:
		globmax = float(kwargs['globmax'])
	if 'width' in kwargs:
		FOW = True
	if 'ax' in kwargs:
		if plotten == True:
			ax1 = kwargs['ax']
		else:
			return
	if 'ax2' in kwargs:
		if plotten == True:
			ax2 = kwargs['ax2']
		else:
			return
	if 'ax3' in kwargs:
		if plotten == True:
			ax3 = kwargs['ax3']
		else:
			nokillax3 = False
	else:
		nokillax3 = False
	if 'smooth' in kwargs:
		smooth = kwargs['smooth']
	if 'label' in kwargs:
		label = kwargs['label']
	if 'fitlines' in kwargs:
		fitlines = kwargs['fitlines']
	if 'nprim' in kwargs:
		nprim = kwargs['nprim']
	if 'contrast_divisor' in kwargs:
		contrast_divisor = kwargs['contrast_divisor']

	y=np.array(y)

	# if plotten: import plot
	# if plotten: f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	if plotten: ax1.scatter( x,y, color='black',marker="x",clip_on=False) #bindata

	#smooth that shit out.
	#https://en.wikipedia.org/wiki/Smoothing_spline
	y2 = scipy.signal.cspline1d(y,lamb=smooth)
	y_intpol_f = scipy.interpolate.interp1d(x,y2,kind='cubic') #interpolate function
	x_intpol = np.linspace(x[0],x[-1],2048,endpoint=False)
	y_intpol = y_intpol_f(x_intpol) #interpolate for x_intpol
	y_intpol = y_intpol.clip(min=0) #set any possible negatives to zero

	####################################################################### CURVE IS COMPLETE, NOW ANALYSIS

	#if plotten: ax1.step(x,y2,color='steelblue', where='mid')
	if plotten: ax1.plot(x_intpol,y_intpol,color='indianred')

	#get 25 percentile, and take mean as baseline.
	baseline = y_intpol[y_intpol < np.percentile(y_intpol, 25)].mean()

	maxind=0
	if globmax:
		maxind = np.where(y_intpol == y_intpol.max())[0][-1] #so that we find the LAST index where argmax(y)
	else:
		#global max
		globmaxind = np.where(y_intpol == y_intpol.max())[0][-1]
		globfalloff = y_intpol[globmaxind]-baseline

		#find distal local max within 30% of FO
		maxind = np.sort( scipy.signal.argrelextrema(y_intpol, np.greater)[0] )[::-1]
		for locmac in maxind[::-1]: #search from back
			if y_intpol[locmac] > (baseline+globfalloff*0.3):
				maxind = locmac
		#if fitlines: ax1.axhline(baseline+globfalloff*0.3,color='green')

	falloff = y_intpol[maxind]-baseline
	falloff_index=len(x_intpol)-1
	print falloff
	try:
		while y_intpol[falloff_index] < threshold*falloff+baseline: #default threshold is 0.5
			falloff_index-=1
	except ValueError:
		print y_intpol[falloff_index] < threshold*falloff+baseline
		print y_intpol[falloff_index]
		print threshold
		print falloff
		print baseline

	#contrast = (y_intpol[maxind]-baseline)/(y_intpol[maxind]+baseline)
	contrast = (y_intpol[maxind]-baseline)/contrast_divisor
	falloff_pos=x_intpol[falloff_index]

	if fitlines: ax1.axvline(falloff_pos,color='green')
	if fitlines: ax1.axhline(baseline,color='green')
	if fitlines: ax1.axhline(y_intpol[maxind],color='green')
	if fitlines: ax1.axvline(x_intpol[maxind],color='green')

	if plotten: plot.texax(ax1)
	if plotten: ax1.set_ylim(bottom=0)
	if plotten: ax1.set_xlabel('Position [mm]', fontsize=8)
	if plotten: ax1.set_ylabel('PG yield [counts]', fontsize=8)
	if plotten: from matplotlib.ticker import MaxNLocator
	if plotten: ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
	# if plotten: ax1.set_ylim(bottom=0)
	if fitlines: ax1.annotate('FOP: '+str(falloff_pos)[:4],xy=(falloff_pos,falloff/2.+baseline))
	if fitlines: ax1.annotate('Contrast: '+str(contrast)[:4],xy=(x_intpol[maxind],y_intpol[maxind]))
	if plotten: print 'FOP is',falloff_pos
	if plotten: print 'Contrast is',contrast

	################################################# FOW

	# first diff:
	y_intpol_diff = np.diff(y_intpol)

	# second diff:
	y_intpol_diff2 = np.diff(y_intpol_diff)

	# find inflex in second diff and plot
	# print "len y_intpol_diff2:", len(y_intpol_diff2)
	if nokillax3: ax3.plot(x_intpol[:-2],y_intpol_diff2,color='darkseagreen')
	diff2_zero_index = falloff_index
	while y_intpol_diff2[diff2_zero_index]*y_intpol_diff2[diff2_zero_index-1] >=0 or y_intpol_diff2[diff2_zero_index] > y_intpol_diff2[diff2_zero_index-1]:
		#zolang product positief, dan geen kruising van x as
		#zolang positieve kruising van xas ga dan verder
		diff2_zero_index+=1
	if nokillax3: ax3.axvline(x_intpol[diff2_zero_index],color='green')
	if nokillax3: ax3.annotate('Inflex: '+str(x_intpol[diff2_zero_index])[:4],xy=(x_intpol[diff2_zero_index],0 ) )

	# use inflex to set interval for gauss fit in first diff
	if plotten: ax2.plot(x_intpol[:-1],y_intpol_diff,color='steelblue')
	# fit_interval = x_intpol[maxind : falloff_index+(falloff_index-maxind)]
	fit_interval = x_intpol[maxind : diff2_zero_index]
	fit_points = y_intpol_diff[maxind : diff2_zero_index]

	#offset = y_intpol_diff[diff2_zero_index]
	offset = 0 #actually, lets remove this param

	if plotten: ax2.plot(fit_interval,fit_points,color='steelblue')
	try:
		popt,y_fitted = fitgauss_tuned(fit_interval,fit_points,falloff_pos,offset)
	except RuntimeError as e:
		raise RuntimeError("in scipy.optimize.curve_fit for filename: "+filename+'. '+e)
	#except ValueError as e:
		#raise ValueError("in scipy.optimize.curve_fit for filename: "+filename+'.')

	def guassianfunc(xVar, a, b, c):
		return a * np.exp(-(xVar - b) ** 2 / (2 * c ** 2)) + offset

	if plotten: ax2.plot(x_intpol[:-1], guassianfunc(x_intpol[:-1], *popt) ,color='grey',linestyle='--') #full function over full window
	if plotten: ax2.plot(fit_interval,y_fitted,color='black')

	if plotten: ax2.set_xlabel('Position [mm]', fontsize=8)
	if not nokillax3: ax2.set_ylabel('First Derivative', fontsize=8)

	g_fwhm = abs(popt[2]*2.35482) #can be neg?
	g_center = popt[1]#np.argmin(y_fitted)
	# print 'FWHM = ',g_fwhm
	# stride = np.diff(fit_interval)[0]
	# fwhm_ind_l = fit_interval[ g_center - int( (g_fwhm*0.5)/stride) ]
	# fwhm_ind_r = fit_interval[ g_center + int( (g_fwhm*0.5)/stride) ]
	fwhm_ind_l = g_center - (g_fwhm*0.5)
	fwhm_ind_r = g_center + (g_fwhm*0.5)
	# print g_center,g_fwhm,fwhm_ind_l, fwhm_ind_r
	if fitlines: ax2.axvline(fwhm_ind_l,color='green')
	if fitlines: ax2.axvline(fwhm_ind_r,color='green')
	if fitlines: ax2.annotate('FOW: '+str(g_fwhm)[:4],xy=(fwhm_ind_r,min(y_fitted)/2.) )#,xycoords='axes points')

	if plotten: print 'FOW is',g_fwhm

	return falloff_pos,g_fwhm,contrast


def testfit(filen,nprim,ax1):
	assert len(filen.split('/')) > 1
	for key,val in dump.thist_to_np_xy(filen).items():
		if key == 'reconstructedProfileHisto':
			x = scale_bincenters(val[0],filen.split('/')[-1]) #no need to append, is same for all. are bincenters
			y = addnoise(val[1],nprim,filen.split('/')[-1]) #append 'onlynoise' to name for only noise
		return get_fop(x,y,plot=True,ax=ax1,fitlines=True)#,label='Detected ')


def fitgauss(x, y, bounds=None,p0=None):
	if bounds == None:
		bounds = (
			(-np.inf,)*4,
			(+np.inf,)*4
		)
	if p0==None:
		mean = sum(x * y) / sum(y)
		sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
		p0 = [max(y), mean, sigma,0]

	def guassianfunc(xVar, a, b, c, d):
		return a * np.exp(-(xVar - b) ** 2 / (2 * c ** 2)) + d

	popt, _ = scipy.optimize.curve_fit(guassianfunc, x, y, p0=p0, bounds=bounds)
	return popt,guassianfunc(x, *popt)


def fitgauss_tuned(x, y, mean, fixed_offset):
	bounds = (
		(-np.inf,-np.inf,-np.inf),
		(np.inf,mean+10,np.inf)
	)
	sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
	p0 = [max(y), mean, sigma]

	def guassianfunc(xVar, a, b, c):
		return a * np.exp(-(xVar - b) ** 2 / (2 * c ** 2)) + fixed_offset

	popt, _ = scipy.optimize.curve_fit(guassianfunc, x, y, p0=p0, bounds=bounds)
	#print "popt",popt
	return (popt,guassianfunc(x, *popt))
