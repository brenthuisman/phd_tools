import numpy as np,plot,scipy


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


def plotfodiffdist(ax1,ct,zs,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]'):
	ax1.set_ylabel(axlabel, fontsize=8)
	
	fodiff=[]
	for i in range(len(ct['ct']['data'])):
		foct=ct['ct']['falloff'][i]
		for i in range(len(ct['rpct']['data'])):
			forpct=ct['rpct']['falloff'][i]
			fodiff.append(forpct-foct)
	(mu, sigma) = scipy.stats.norm.fit(fodiff)
	
	if not emisfops == None:
		fopshifts=[]
		for fopset in emisfops:
			fopshifts.append( fopset[-1]-fopset[0] )
		ax1.set_xlim3d(np.mean(fopshifts)-20,np.mean(fopshifts)+20)
	elif zs==0:
		ax1.set_xlim3d(mu-20,mu+20)
	
	y,bins=np.histogram(fodiff, np.arange(-120,120,1))
	#print mu, sigma
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['grey']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y',label=labels[zs]+' primaries')
	
	ax1.set_xlabel('Detected Shifts [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	ax1.locator_params(axis='y',nbins=len(labels)-1)
	ax1.set_yticklabels(labels, fontsize=8, va='baseline', ha='left')
	#ax1.tick_params(axis='y',which='minor',bottom='off')
	#zs/10.
	
	label_extra=''
	if len(emisfops) == len(labels):
		label_extra=', $Shift_{em}$ = '+str(emisfops[zs][1]-emisfops[zs][0])
	plot.figtext(0.05, 0.9-zs/40.,labels[zs]+": $\mu_{shift}$ = "+str(mu)[:4]+", $\sigma_{shift}$ = "+str(sigma)[:4]+label_extra, ha='left', va='center', fontsize=6, transform=ax1.transAxes)


def plotfodist(ax1,ct,zs,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]'):
	ax1.set_ylabel(axlabel, fontsize=8)
	
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
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=labels[zs]+' primaries')
	
	y,bins=np.histogram(fo_rpct, np.arange(-120,120,1))
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = ['steelblue']*len(y)
	ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=labels[zs]+' primaries')
	
	if zs==0:
		centr = (ctmu+rpctmu)/2.
		ax1.set_xlim3d(centr-20,centr+20)
	
	ax1.set_xlabel('Falloff Position [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	ax1.locator_params(axis='y',nbins=len(labels))
	ax1.set_yticklabels(labels, fontsize=8, va='baseline', ha='left')
	ax1.set_ylabel('Primaries [nr]', fontsize=8)
	
	labelCT_extra=''
	labelRPCT_extra=''
	if len(emisfops) == len(labels):
		labelCT_extra=', $FOP_{em}$ = '+str(emisfops[zs][0])
		labelRPCT_extra=', $FOP_{em}$ = '+str(emisfops[zs][1])
	#elif len(emisfops) == 1:
		#labelCT_extra=', $FOP_{em}$ = '+str(emisfops[0][0])
		#labelRPCT_extra=', $FOP_{em}$ = '+str(emisfops[0][1])
	
	plot.figtext(0.05, 0.9-zs/20.,labels[zs]+ct['ct']['label']+": $\mu_{FOP}$ = "+str(ctmu)[:4]+", $\sigma_{FOP}$ = "+str(ctsigma)[:4]+labelCT_extra, ha='left', va='center', fontsize=6, transform=ax1.transAxes)
	plot.figtext(0.05, 0.875-zs/20.,labels[zs]+ct['rpct']['label']+": $\mu_{FOP}$ = "+str(rpctmu)[:4]+", $\sigma_{FOP}$ = "+str(rpctsigma)[:4]+labelRPCT_extra, ha='left', va='center', fontsize=6, transform=ax1.transAxes)
