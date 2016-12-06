import dump, numpy as np,plot,glob2 as glob,copy,matplotlib.pyplot as plt,scipy

rootn='-patient-spot-auger.root'

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
	
	ctset6['ct']['files'] = glob.glob(ct1+"/**/"+name+rootn)
	ctset6['rpct']['files'] = glob.glob(ct2+"/**/"+name+rootn)

	for ffilen in ctset6['ct']['files']:
		print 'opening',ffilen
		try:
			for key,val in dump.thist2np_xy(ffilen).items():
				if key == 'reconstructedProfileHisto':
					ctset6['ct']['x'] = val[0] #no need to append, is same for all
					if 'ipnl' == name:
						ctset6['ct']['data'].append(ipnlnoise(val[1],nprim))
					elif 'iba' == name: #reverse
						ctset6['ct']['data'].append(ibanoise(val[1][::-1],nprim))
			ctset6['ct']['falloff'].append(ipnl_fit_range(ctset6['ct']['x'],ctset6['ct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
	for ffilen in ctset6['rpct']['files']:
		print 'opening',ffilen
		try:
			for key,val in dump.thist2np_xy(ffilen).items():
				if key == 'reconstructedProfileHisto':
					ctset6['rpct']['x'] = val[0] #no need to append, is same for all
					if 'ipnl' == name:
						ctset6['rpct']['data'].append(ipnlnoise(val[1],nprim))
					elif 'iba' == name: #reverse
						ctset6['rpct']['data'].append(ibanoise(val[1][::-1],nprim))
			ctset6['rpct']['falloff'].append(ipnl_fit_range(ctset6['rpct']['x'],ctset6['rpct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
	
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
			(mu, sigma) = norm.fit(binn) #returns actually sigma, not var.
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
			(mu, sigma) = norm.fit(binn) #returns actually sigma, not var.
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


def ipnlnoise(data,nprim):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	mu = 2.5e-7*nprim
	sigma = 0.25e-7*nprim
	retval = []
	for i in data:
		retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def onlyipnlnoise(data,nprim):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	mu = 2.5e-7*nprim
	sigma = 0.25e-7*nprim
	retval = []
	for i in data:
		retval.append(np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def ibanoise(data,nprim):
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin
	mu = 5e-7*nprim
	sigma = 0.5e-7*nprim
	retval = []
	for i in data:
		retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def onlyibanoise(data,nprim):
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin
	mu = 5e-7*nprim
	sigma = 0.5e-7*nprim
	retval = []
	for i in data:
		retval.append(np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def ipnl_fit_range_oud(x,y):
	#take max
	y=np.array(y)
	#maxind = np.argmax(y)
	maxind = np.where(y == y.max())[0][-1] #so that we find the LAST index where argmax(y)
	#print maxind
	y = y.tolist()
	#go towards end and find 50% thrshold
	nextind=maxind+1
	while y[nextind] > 0.5*y[maxind]:
		nextind+=1
	# go x bins left and right and fit within
	hm_left=nextind-5
	hm_right=nextind+5
	xbp=x[hm_left:hm_right]
	ybp=y[hm_left:hm_right]
	#print maxind,xbp,ybp,y
	tck,u = scipy.interpolate.splprep( [xbp,ybp] ,k=3 )#cubic spline
	xnew,ynew = scipy.interpolate.splev(  np.linspace( 0, 1, 200 ), tck,der = 0)
	#take mean value in tail-window as minimum
	floor=np.mean(y[hm_right:])
	#take max val in BP window as max
	top=np.max(ybp)
	falloffval_50pc=(top-floor)*.5
	nextind=len(ynew)-1
	while ynew[nextind] < falloffval_50pc:
		nextind-=1
	falloffpos = xnew[nextind]
	#ax1.plot( xbp,ybp,'' , xnew ,ynew )
	return falloffpos,[xbp,ybp,'',xnew,ynew]


def ipnl_fit_range(x,y):
	y=np.array(y)
	
	#f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	#ax1.step( x,y, color='moccasin') #bindata
	
	#smooth that shit out.
	#https://en.wikipedia.org/wiki/Smoothing_spline
	y2 = scipy.signal.cspline1d(y,lamb=2)
	y_intpol_f = scipy.interpolate.interp1d(x,y2,kind='cubic') #interpolate function
	x_intpol = np.linspace(x[0],x[-1],1024,endpoint=False)
	y_intpol = y_intpol_f(x_intpol) #interpolate for x_intpol
	y_intpol = y_intpol.clip(min=0) #set any possible negatives to zero
	#ax1.step(x,y2,color='steelblue')
	#ax1.plot(x_intpol,y_intpol,color='indianred')
	
	#take max
	maxind = np.where(y_intpol == y_intpol.max())[0][-1] #so that we find the LAST index where argmax(y)
	#ax1.axvline(x_intpol[maxind],color='green')
	
	#get 25 percentile, and take mean as baseline.
	baseline = y_intpol[y_intpol < np.percentile(y_intpol, 25)].mean()
	#ax1.axhline(baseline,color='green')
	#ax1.axhline(y_intpol.max(),color='green')
	
	falloff = y_intpol[maxind]-baseline
	falloff_index=len(x_intpol)-1
	while y_intpol[falloff_index] < 0.5*falloff+baseline:
		falloff_index-=1
	falloff_pos=x_intpol[falloff_index]
	#ax1.axvline(falloff_pos,color='green')
	
	#f.savefig('recons.pdf', bbox_inches='tight')
	#plot.close('all')
	#quit()
	return falloff_pos


def gueth_fit_range(xs,profile,falloff=.5,window_width=80.,smooth=2):
    # x,y=xs,profile
    xs=np.array(xs)
    profile=np.array(profile)/sum(profile)
    assert(xs.shape==profile.shape)
    
    profile_falloff = profile.mean()*1.3
    index_max = profile.size-1
    assert(profile[index_max]<profile_falloff)
    while profile[index_max]<profile_falloff:
        index_max -= 1

    x_max = xs[index_max]
    x_res = xs[index_max+1]-xs[index_max]

    index_window = int(window_width/x_res)
    xs_window = xs[index_max-index_window:index_max+index_window]
    profile_window = profile[index_max-index_window:index_max+index_window]
    profile_window_spline = scipy.signal.cspline1d(profile_window,lamb=smooth)

    f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
    ax1.plot(xs,profile)
    ax1.plot(xs_window,profile_window,'o-')
    xs_window_interp = np.linspace(xs_window.min(),xs_window.max(),128,endpoint=False)
    profile_window_interp = scipy.signal.cspline1d_eval(profile_window_spline,xs_window_interp,dx=x_res,x0=xs_window_interp.min())
    ax1.plot(xs_window_interp,profile_window_interp,'*-')
    #f.savefig('testplot-falloff.pdf', bbox_inches='tight')
    #plot.close('all')
    #quit()
    
    def eval_profile_window_spline(position):
        #assert(type(position)==float64)
        assert(position>=xs_window.min() and position<=xs_window.max())
        value = scipy.signal.cspline1d_eval(profile_window_spline,[position],dx=x_res,x0=xs_window.min())
        return value[0]

    def maximum_profile_window_spline(position):
        #position = position[0]
        value = eval_profile_window_spline(position) 
        return -value

    x_max_spline = scipy.optimize.fminbound(maximum_profile_window_spline,xs_window.min(),xs_window.max(),disp=False)
    #x_max_spline = x_max_spline[0]
    profile_max_spline = eval_profile_window_spline(x_max_spline)
    
    ax1.axvline(x_max_spline)
    ax1.axhline(profile_max_spline)

    #print "x_max_spline",x_max_spline
    #print "profile_max_spline",profile_max_spline

    def dichotomy_profile_window_spline(bounds,bounds_level,level):
        assert(bounds_level[0]<level and bounds_level[1]>level)

        # if level diff become too small then linear intepolation for final step
        if (bounds_level[1]-bounds_level[0]) < 2e-3:
            alpha = (level-bounds_level[0])/(bounds_level[1]-bounds_level[0])
            assert(alpha>0 and alpha<1)
            return alpha*(bounds[1]-bounds[0])+bounds[0]

        middle = bounds[0]+bounds[1]
        middle /= 2.
        middle_level = eval_profile_window_spline(middle)

        if middle_level > level:
            return dichotomy_profile_window_spline((bounds[0],middle),(bounds_level[0],middle_level),level)
        else:
            return dichotomy_profile_window_spline((middle,bounds[1]),(middle_level,bounds_level[1]),level)

    def find_level_profile_window_spline(level,bounds):
        return dichotomy_profile_window_spline(bounds,(eval_profile_window_spline(bounds[0]),eval_profile_window_spline(bounds[1])),level)

    profile_falloff_spline = profile_max_spline * falloff
    ax1.axhline(profile_falloff_spline)
    x_falloff_spline = find_level_profile_window_spline(profile_falloff_spline,(xs_window.max(),x_max_spline))

    ax1.axvline(x_max,color='indianred')
    ax1.axvline(x_max_spline,color='steelblue')
    ax1.axhline(profile_max_spline)
    ax1.axvline(x_falloff_spline,color='mediumseagreen')
    ax1.axhline(profile_falloff_spline)
    #ax1.xlim(x_max-1.5*window_width,x_max+1.5*window_width)
    f.savefig('testplot-falloff.pdf', bbox_inches='tight')
    plot.close('all')
    quit()

    return x_falloff_spline


def plotrange(ax1,ct):
	x = ct['ct']['x']
	y = ct['ct']['av']
	um = ct['ct']['uncm']
	up = ct['ct']['uncp']
	ymax = max(y)
	
	if len(um)>0:
		ymax = max(ymax,max(up))
		plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='steelblue', lw=0.5,clip_on=False) #doesnt support where=mid
	else:
		ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False)
	
	x = ct['rpct']['x']
	y = ct['rpct']['av']
	um = ct['rpct']['uncm']
	up = ct['rpct']['uncp']
	ymax = max(ymax,max(y))
	
	if len(um)>0:
		ymax = max(ymax,max(up))
		plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='indianred', lw=0.5,clip_on=False)
	else:
		ax1.step(x, y, label=ct['name']+'rpct', color='indianred', lw=1, where='mid',clip_on=False)
	ax1.set_xlabel('Depth [mm]', fontsize=8)
	ax1.set_ylabel('PG detected [counts]', fontsize=8)
	ax1.set_ylim(bottom=0,top=ymax)
	#ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+'primaries', fontsize=8)
	plot.texax(ax1)


def plot_all_ranges(ax1,ct):
	for i in range(len(ct['ct']['data'])):
		x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
		ax1.step(x, y, label=ct['name']+'ct', color='indianred', lw=1, where='mid',clip_on=False, alpha=0.5)
		ax1.axvline(fo, color='indianred', ls='-',lw=1, alpha=0.5)
	
	ax1.set_xlabel('Depth [mm]', fontsize=8)
	ax1.set_ylabel('PG detected [counts]', fontsize=8)
	ax1.set_title(plot.sn(ct['nprim'],0)+' primaries', fontsize=8)
	plot.texax(ax1)

	for i in range(len(ct['rpct']['data'])):
		x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
		ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False, alpha=0.5)
		ax1.axvline(fo, color='steelblue', ls='-',lw=1, alpha=0.5)
	
	ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+'primaries', fontsize=8)
	ax1.set_ylim(bottom=0)
	plot.texax(ax1)


def plotfodiffdist(ax1,ct,zs):
	fodiff=[]
	for i in range(len(ct['ct']['data'])):
		foct=ct['ct']['falloff'][i]
		for i in range(len(ct['rpct']['data'])):
			forpct=ct['rpct']['falloff'][i]
			fodiff.append(forpct-foct)
	(mu, sigma) = norm.fit(fodiff)
	
	y,bins=np.histogram(fodiff, np.arange(-120,120,1))
	#print mu, sigma
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['grey']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y',label=plot.sn_mag(ct['nprim'])+' primaries')
	
	ax1.set_xlim3d(-10,20)
	
	ax1.set_xlabel('Detected Shifts [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	ax1.locator_params(axis='y',nbins=4)
	labels = ["$10^9$","$10^8$","$10^7$","$10^6$"]
	ax1.set_yticklabels(labels, fontsize=8, va='baseline', ha='left')
	ax1.set_ylabel('Primaries [nr]', fontsize=8)
	#zs/10.
	plt.figtext(0.05, 0.9-zs/400.,plot.sn_mag(ct['nprim'])+": $\mu$ = "+str(mu)[:3]+", $\sigma$ = "+str(sigma)[:3], ha='left', va='center', fontsize=6, transform=ax1.transAxes)


def plotfodist(ax1,ct,zs):
	fo_ct=[]
	fo_rpct=[]
	
	for i in range(len(ct['ct']['data'])):
		x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
		fo_ct.append(fo)
	
	for i in range(len(ct['rpct']['data'])):
		x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
		fo_rpct.append(fo)
	
	y,bins=np.histogram(fo_ct, np.arange(-120,120,1))
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['indianred']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=plot.sn_mag(ct['nprim'])+' primaries')
	
	y,bins=np.histogram(fo_rpct, np.arange(-120,120,1))
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['steelblue']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=plot.sn_mag(ct['nprim'])+' primaries')
	
	ax1.set_xlim3d(-10,20)
	
	ax1.set_xlabel('Falloff Position [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	ax1.locator_params(axis='y',nbins=4)
	labels = ["$10^9$","$10^8$","$10^7$","$10^6$"]
	ax1.set_yticklabels(labels, fontsize=8, va='baseline', ha='left')
	ax1.set_ylabel('Primaries [nr]', fontsize=8)
