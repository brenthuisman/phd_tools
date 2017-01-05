import numpy as np,plot,matplotlib.pyplot as plt,scipy


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
		#ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid')
	
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
		#ax1.step(x, y, label=ct['name']+'rpct', color='indianred', lw=1, where='mid')
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


def plotfodiffdist(ax1,ct,zs,labels=None):
	if labels == None:
		#assume int study
		labels=["$10^9$","$10^8$","$10^7$","$10^6$"]
		ax1.set_ylabel('Primaries [nr]', fontsize=8)
		def printprim(N):
			return plot.sn_mag(N)
	else:
		#assume layer study
		ax1.set_ylabel('Layer Position', fontsize=8)
		def printprim(N):
			return labels[zs]+': '+plot.sn(N)
	
	fodiff=[]
	for i in range(len(ct['ct']['data'])):
		foct=ct['ct']['falloff'][i]
		for i in range(len(ct['rpct']['data'])):
			forpct=ct['rpct']['falloff'][i]
			fodiff.append(forpct-foct)
	(mu, sigma) = scipy.stats.norm.fit(fodiff)
	
	y,bins=np.histogram(fodiff, np.arange(-120,120,1))
	#print mu, sigma
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['grey']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y',label=printprim(ct['nprim'])+' primaries')
	
	ax1.set_xlim3d(-10,20)
	
	ax1.set_xlabel('Detected Shifts [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	ax1.locator_params(axis='y',nbins=len(labels))
	ax1.set_yticklabels(labels, fontsize=8, va='baseline', ha='left')
	#zs/10.
	plt.figtext(0.05, 0.9-zs/40.,printprim(ct['nprim'])+": $\mu$ = "+str(mu)[:3]+", $\sigma$ = "+str(sigma)[:3], ha='left', va='center', fontsize=6, transform=ax1.transAxes)


def plotfodist(ax1,ct,zs,labels=None):
	if labels == None:
		#assume int study
		labels=["$10^9$","$10^8$","$10^7$","$10^6$"]
		ax1.set_ylabel('Primaries [nr]', fontsize=8)
		def printprim(N):
			return plot.sn_mag(N)
	else:
		#assume layer study
		ax1.set_ylabel('Layer Position', fontsize=8)
		def printprim(N):
			return labels[zs]+': '+plot.sn(N)
	
	fo_ct=[]
	fo_rpct=[]
	
	for i in range(len(ct['ct']['data'])):
		x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
		fo_ct.append(fo)
	(ctmu, ctsigma) = scipy.stats.norm.fit(fo_ct)
	
	for i in range(len(ct['rpct']['data'])):
		x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
		fo_rpct.append(fo)
	(rpctmu, rpctsigma) = scipy.stats.norm.fit(fo_rpct)
	
	y,bins=np.histogram(fo_ct, np.arange(-120,120,1))
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['indianred']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=printprim(ct['nprim'])+' primaries')
	
	y,bins=np.histogram(fo_rpct, np.arange(-120,120,1))
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['steelblue']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=printprim(ct['nprim'])+' primaries')
	
	ax1.set_xlim3d(-10,20)
	
	ax1.set_xlabel('Falloff Position [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	ax1.locator_params(axis='y',nbins=len(labels))
	ax1.set_yticklabels(labels, fontsize=8, va='baseline', ha='left')
	ax1.set_ylabel('Primaries [nr]', fontsize=8)
	
	plt.figtext(0.05, 0.9-zs/20.,printprim(ct['nprim'])+"CT: $\mu$ = "+str(ctmu)[:3]+", $\sigma$ = "+str(ctsigma)[:3], ha='left', va='center', fontsize=6, transform=ax1.transAxes)
	plt.figtext(0.05, 0.875-zs/20.,printprim(ct['nprim'])+"RPCT: $\mu$ = "+str(rpctmu)[:3]+", $\sigma$ = "+str(rpctsigma)[:3], ha='left', va='center', fontsize=6, transform=ax1.transAxes)
