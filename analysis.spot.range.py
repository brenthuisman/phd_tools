#!/usr/bin/env python
import dump, numpy as np,plot,sys,glob2 as glob,os
from scipy.stats import chisquare,norm

#np.random.seed(65983247)

rootn='-patient-spot-auger.root'

def getctset(nprim,ct1,ct2,name):
	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':nprim}
	ctset6['ct']['path'] = ct1
	ctset6['rpct']['path'] = ct2
	ctset6['ct']['data'] = []
	ctset6['rpct']['data'] = []
	ctset6['ct']['falloff'] = []
	ctset6['rpct']['falloff'] = []
	ctset6['ct']['x'] = []
	ctset6['rpct']['x'] = []
	
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
	
	return ctset6

def plotrange(ax1,ct):
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

#########################################################################################################

typ='ipnl'
#typ='iba'
ctset_int_6 = getctset(1e6,'fromcluster/nprims/run.yjzw','fromcluster/nprims/run.wfmx',typ)
ctset_int_7 = getctset(1e7,'fromcluster/nprims/run.41VE','fromcluster/nprims/run.NE7B',typ)
ctset_int_8 = getctset(1e8,'fromcluster/nprims/run.bfrX','fromcluster/nprims/run.rOx1',typ)
ctset_int_9 = getctset(1e9,'fromcluster/nprims/run.xTcG','fromcluster/nprims/run.b2Aj',typ)

#########################################################################################################

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

plotrange(ax1,ctset_int_9)
plotrange(ax2,ctset_int_8)
plotrange(ax3,ctset_int_7)
plotrange(ax4,ctset_int_6)
f.subplots_adjust(hspace=.5)
ax1.set_xlabel('')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax4.set_ylabel('')
f.savefig(typ+'-spot-falloff.pdf', bbox_inches='tight')
plot.close('all')

#########################################################################################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

plotfodiffdist(ax1,ctset_int_9,0)
plotfodiffdist(ax1,ctset_int_8,10)
plotfodiffdist(ax1,ctset_int_7,20)
plotfodiffdist(ax1,ctset_int_6,30)
#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
fig.savefig(typ+'-spot-falloffdiffdist.pdf')#, bbox_inches='tight')
plt.close('all')

#########################################################################################################

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

plotfodist(ax1,ctset_int_9,0)
plotfodist(ax1,ctset_int_8,10)
plotfodist(ax1,ctset_int_7,20)
plotfodist(ax1,ctset_int_6,30)

#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
plt.savefig(typ+'-spot-falloffdist.pdf')#, bbox_inches='tight')
plt.close('all')
