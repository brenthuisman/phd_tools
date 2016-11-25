#!/usr/bin/env python
import dump, numpy as np,plot,sys,glob2 as glob,os
from scipy.stats import chisquare,norm

clrs=plot.colors
np.random.seed(65983247)

rootn='ipnl-patient-spot-auger.root'
#rootn='iba-patient-spot-auger.root'

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
	
	ctset6['ct']['files'] = glob.glob(ct1+"/**/"+rootn)
	ctset6['rpct']['files'] = glob.glob(ct2+"/**/"+rootn)

	for ffilen in ctset6['ct']['files']:
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			if key == 'reconstructedProfileHisto':
				ctset6['ct']['x'] = val[0] #no need to append, is same for all
				ctset6['ct']['data'].append(plot.ipnlnoise(val[1],nprim))
				#ctset6['ct']['data'].append(plot.ibanoise(val[1],nprim))
		ctset6['ct']['falloff'].append(plot.ipnl_fit_range(ctset6['ct']['x'],ctset6['ct']['data'][-1]))
	for ffilen in ctset6['rpct']['files']:
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			if key == 'reconstructedProfileHisto':
				ctset6['rpct']['x'] = val[0] #no need to append, is same for all
				ctset6['rpct']['data'].append(plot.ipnlnoise(val[1],nprim))
				#ctset6['rpct']['data'].append(plot.ibanoise(val[1],nprim))
		ctset6['rpct']['falloff'].append(plot.ipnl_fit_range(ctset6['rpct']['x'],ctset6['rpct']['data'][-1]))
	
	return ctset6

def plotrange(ax1,ct):
	
	for i in range(len(ct['ct']['data'])):
		x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i][0]
		ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False)
		ax1.axvline(fo, color='#999999', ls='--')
	
	ax1.set_xlabel('Depth [mm]', fontsize=8)
	ax1.set_ylabel('PG detected [counts]', fontsize=8)
	#ax1.set_ylim(bottom=0,top=ymax)
	ax1.set_title(plot.sn(ct['nprim'],0)+' primaries', fontsize=8)
	plot.texax(ax1)

	for i in range(len(ct['rpct']['data'])):
		x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i][0]
		ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False)
		ax1.axvline(fo, color='#999999', ls='--')
	
	ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+'primaries', fontsize=8)
	plot.texax(ax1)

color_index=0
def plotfodist(ax1,ct,zs):
	global color_index
	fodiff=[]
	for i in range(len(ct['ct']['data'])):
		foct=ct['ct']['falloff'][i][0]
		for i in range(len(ct['rpct']['data'])):
			forpct=ct['rpct']['falloff'][i][0]
			fodiff.append(forpct-foct)
	#ax1.hist(fodiff, 20, facecolor='steelblue', alpha=0.75)
	#ax1.hist(fodiff, 20, facecolor=plot.colors[color_index], alpha=0.75,label=plot.sn_mag(ct['nprim'])+' primaries')
	y,bins=np.histogram(fodiff, np.arange(-120,120,10))
	bincenters = 0.5*(bins[1:]+bins[:-1])
	c = [plot.colors[color_index]]*len(y)
	ax1.bar(bincenters,y, color=c, zs=zs, zdir='y', alpha=0.75,label=plot.sn_mag(ct['nprim'])+' primaries')
	color_index+=1
	
	ax1.set_xlabel('Detected Shifts [mm]', fontsize=8)
	ax1.set_zlabel('[counts]', fontsize=8)
	#ax1.set_ylim(bottom=0,top=ymax)
	
	ax1.set_title('PG detection shifts', fontsize=8)
	#plot.texax(ax1)

###################################

ctset_int_6 = getctset(1e6,'fromcluster/nprims/run.yjzw','fromcluster/nprims/run.wfmx','')
ctset_int_7 = getctset(1e7,'fromcluster/nprims/run.41VE','fromcluster/nprims/run.NE7B','')
ctset_int_8 = getctset(1e8,'fromcluster/nprims/run.bfrX','fromcluster/nprims/run.rOx1','')
ctset_int_9 = getctset(1e9,'fromcluster/nprims/run.xTcG','fromcluster/nprims/run.b2Aj','')

#f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

#plotrange(ax1,ctset_int_9)
#plotrange(ax2,ctset_int_8)
#plotrange(ax3,ctset_int_7)
#plotrange(ax4,ctset_int_6)
#f.subplots_adjust(hspace=.5)
#ax1.set_xlabel('')
#ax2.set_xlabel('')
#ax2.set_ylabel('')
#ax4.set_ylabel('')
#f.savefig(rootn.split('-')[0]+'-spot-falloff.pdf', bbox_inches='tight')
#plot.close('all')

#########################################################################################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

#f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False, projection='3d')

plotfodist(ax1,ctset_int_9,0)
plotfodist(ax1,ctset_int_8,10)
plotfodist(ax1,ctset_int_7,20)
plotfodist(ax1,ctset_int_6,30)
#ax1.legend(loc='upper right',frameon=False)#, bbox_to_anchor=(1.2, 1.))
fig.savefig(rootn.split('-')[0]+'-spot-falloffdist.pdf', bbox_inches='tight')
plot.close('all')
