#!/usr/bin/env python
import dump, numpy as np,plot,sys,glob2 as glob,os
from scipy.stats import chisquare,norm

clrs=plot.colors
np.random.seed(659873247)

rootn='ipnl-patient-spot-auger.root'
#rootn='iba-patient-spot-auger.root'

#glob.glob("/home/brent/phd/scratch/doseactortest-stage2/**/ipnl-patient-spot-auger.root")

def getctset(nprim,ct1,ct2,name):
	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':nprim}
	ctset6['ct']['path'] = ct1
	ctset6['rpct']['path'] = ct2
	ctset6['ct']['data'] = []
	ctset6['rpct']['data'] = []
	ctset6['ct']['av'] = []
	ctset6['rpct']['av'] = []
	ctset6['ct']['unc'] = []
	ctset6['rpct']['unc'] = []
	ctset6['ct']['uncm'] = []
	ctset6['rpct']['uncm'] = []
	ctset6['ct']['uncp'] = []
	ctset6['rpct']['uncp'] = []
	ctset6['ct']['x'] = []
	ctset6['rpct']['x'] = []
	
	#ctset6['ct']['files'] = [glob.glob(ct1+"/**/"+rootn)[0]]
	#ctset6['rpct']['files'] = [glob.glob(ct2+"/**/"+rootn)[0]]
	ctset6['ct']['files'] = glob.glob(ct1+"/**/"+rootn)
	ctset6['rpct']['files'] = glob.glob(ct2+"/**/"+rootn)

	for ffilen in ctset6['ct']['files']:
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			if key == 'reconstructedProfileHisto':
				ctset6['ct']['x'] = val[0] #no need to append, is same for all
				ctset6['ct']['data'].append(plot.ipnlnoise(val[1],nprim))
				#ctset6['ct']['data'].append(plot.ibanoise(val[1],nprim))
	for ffilen in ctset6['rpct']['files']:
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			if key == 'reconstructedProfileHisto':
				ctset6['rpct']['x'] = val[0] #no need to append, is same for all
				ctset6['rpct']['data'].append(plot.ipnlnoise(val[1],nprim))
				#ctset6['rpct']['data'].append(plot.ibanoise(val[1],nprim))
	
	if len(ctset6['ct']['data']) > 1:
		#we can average
		ndata = np.array(ctset6['ct']['data'])
		ndata = np.rollaxis(ndata,1)
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
	else:
		ctset6['rpct']['av'] = ctset6['rpct']['data'][0]
		
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
	
	ax1.set_xlabel('Depth [mm]', fontsize=8)
	ax1.set_ylabel('PG detected [counts]', fontsize=8)
	ax1.set_ylim(bottom=0,top=ymax)
	ax1.set_title(plot.sn(ct['nprim'],0)+' primaries', fontsize=8)
	plot.texax(ax1)

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
	ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+'primaries', fontsize=8)
	plot.texax(ax1)

###################################

#############gate_run_submit_cluster_nomove.sh mac/main-int9ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int9rpct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int8ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int8rpct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int7ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int7rpct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int6ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int6rpct.mac 10
#############xTcG
#############b2Aj
#############bfrX
#############rOx1
#############41VE
#############NE7B
#############yjzw
#############wfmx

ctset_int_6 = getctset(1e6,'fromcluster/nprims/run.yjzw','fromcluster/nprims/run.wfmx','')
ctset_int_7 = getctset(1e7,'fromcluster/nprims/run.41VE','fromcluster/nprims/run.NE7B','')
ctset_int_8 = getctset(1e8,'fromcluster/nprims/run.bfrX','fromcluster/nprims/run.rOx1','')
ctset_int_9 = getctset(1e9,'fromcluster/nprims/run.xTcG','fromcluster/nprims/run.b2Aj','')

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
f.savefig(rootn.split('-')[0]+'-spot-nprims.pdf', bbox_inches='tight')
plot.close('all')

print '====== chisq CT w RPCT ====='
print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['rpct']['av'])
print '8,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_8['rpct']['av'])
print '7,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_7['rpct']['av'])
print '6,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_6['rpct']['av'])
	
print '====== chisq CT w CT ====='
print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['ct']['av'])
print '9,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_9['ct']['av'])
print '9,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_9['ct']['av'])
print '9,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_9['ct']['av'])

print '====== chisq RPCT w RPCT ====='
print '9,9', chisquare(ctset_int_9['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
print '9,8', chisquare(ctset_int_8['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
print '9,7', chisquare(ctset_int_7['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
print '9,6', chisquare(ctset_int_6['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
