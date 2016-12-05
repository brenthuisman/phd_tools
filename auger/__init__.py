import dump, numpy as np,plot,glob2 as glob,copy,matplotlib.pyplot as plt
from scipy.stats import norm

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
						ctset6['ct']['data'].append(plot.ipnlnoise(val[1],nprim))
					elif 'iba' == name: #reverse
						ctset6['ct']['data'].append(plot.ipnlnoise(val[1][::-1],nprim))
			ctset6['ct']['falloff'].append(plot.ipnl_fit_range(ctset6['ct']['x'],ctset6['ct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
	for ffilen in ctset6['rpct']['files']:
		print 'opening',ffilen
		try:
			for key,val in dump.thist2np_xy(ffilen).items():
				if key == 'reconstructedProfileHisto':
					ctset6['rpct']['x'] = val[0] #no need to append, is same for all
					if 'ipnl' == name:
						ctset6['rpct']['data'].append(plot.ipnlnoise(val[1],nprim))
					elif 'iba' == name: #reverse
						ctset6['rpct']['data'].append(plot.ipnlnoise(val[1][::-1],nprim))
			ctset6['rpct']['falloff'].append(plot.ipnl_fit_range(ctset6['rpct']['x'],ctset6['rpct']['data'][-1]))
		except IndexError:
			print "Empty file detected, skipping"
	
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
	
	return ctset6


def sumctset(name,*cts):
	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':0}
	for ctset in cts:
		ctset6['nprim'] += ctset['nprim']
	
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
		ctset6['ct']['falloff'].append(plot.ipnl_fit_range(ctset6['ct']['x'],dataset))
	
	for dataset in ctset6['rpct']['data']:
		ctset6['rpct']['falloff'].append(plot.ipnl_fit_range(ctset6['rpct']['x'],dataset))
		
	return ctset6


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
	y,bins=np.histogram(fodiff, np.arange(-120,120,1))
	(mu, sigma) = norm.fit(fodiff)
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
