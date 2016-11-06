#!/usr/bin/env python
import dump, numpy as np,matplotlib.pyplot as plt,plot,sys,glob2 as glob
from scipy.stats import chisquare,norm

clrs=plot.colors
np.random.seed(9873247)

rootn='ipnl-patient-spot-auger.root'

def ipnlnoise(data,nprim):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	mu = 2.5e-7*nprim
	sigma = 0.25e-7*nprim
	retval = []
	for i in data:
		retval.append(i + np.random.normal(mu,sigma))
	return retval
		
def ibanoise(data,nprim):
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin
	mu = 5e-7*nprim
	sigma = 0.5e-7*nprim
	retval = []
	for i in data:
		retval.append(i + np.random.normal(mu,sigma))
	return retval
	
def getctset(nprim,ct1,ct2,unc=5,prefix=''):
	ctset6 = {'ct':{},'rpct':{},'name':prefix,'nprim':nprim}
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
	
	if unc > 1:
		ctset6['ct']['files'] = [prefix+str(x) for x in range(1,6)]
		ctset6['rpct']['files'] = [prefix+str(x) for x in range(1,6)]
	else:
		ctset6['ct']['files'] = [prefix]
		ctset6['rpct']['files'] = [prefix]

	for filen in ctset6['ct']['files']:
		ffilen = ctset6['ct']['path']+'/'+filen+'/'+rootn
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			#print key
			if key == 'reconstructedProfileHisto':
				#print val
				ctset6['ct']['x'] = val[0] #no need to append, is same for all
				ctset6['ct']['data'].append(ipnlnoise(val[1],nprim))
	for filen in ctset6['rpct']['files']:
		ffilen = ctset6['rpct']['path']+'/'+filen+'/'+rootn
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			#print key
			if key == 'reconstructedProfileHisto':
				#print val[1]
				ctset6['rpct']['x'] = val[0] #no need to append, is same for all
				ctset6['rpct']['data'].append(ipnlnoise(val[1],nprim))
	
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


def sumctset(nprim,name,*cts):
	ctset6 = {'ct':{},'rpct':{},'name':name,'nprim':nprim}
	ctset6['ct']['data'] = cts[0]['ct']['data'][:] #copy first data
	ctset6['rpct']['data'] = cts[0]['rpct']['data'][:] #copy first data
	ctset6['ct']['av'] = []
	ctset6['rpct']['av'] = []
	ctset6['ct']['unc'] = []
	ctset6['rpct']['unc'] = []
	ctset6['ct']['uncm'] = []
	ctset6['rpct']['uncm'] = []
	ctset6['ct']['uncp'] = []
	ctset6['rpct']['uncp'] = []
	ctset6['ct']['x'] = cts[0]['ct']['x'][:]
	ctset6['rpct']['x'] = cts[0]['rpct']['x'][:]
	
	for ctset in cts[1:]: #skip first
		for dindex,dataset in enumerate(ctset6['ct']['data']): #only works if number of unc sets are same
			for bindex,binn in enumerate(dataset):
				ctset6['ct']['data'][dindex][bindex] += ctset['ct']['data'][dindex][bindex]

	for ctset in cts[1:]: #skip first
		for dindex,dataset in enumerate(ctset6['rpct']['data']): #only works if number of unc sets are same
			for bindex,binn in enumerate(dataset):
				ctset6['rpct']['data'][dindex][bindex] += ctset['rpct']['data'][dindex][bindex]

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


def plotrange(ax1,ct):
	x = ct['ct']['x']
	y = ct['ct']['av']
	um = ct['ct']['uncm']
	up = ct['ct']['uncp']
	
	ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1)
	if len(um)>0:
		plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='steelblue', lw=0.5)
	
	ax1.set_xlabel('Depth [mm]')
	ax1.set_ylabel('PG detected [counts]')
	#ax1.set_xlim(-0.5,5.5)
	ax1.set_title('PG detection')
	plot.texax(ax1)

	x = ct['rpct']['x']
	y = ct['rpct']['av']
	um = ct['rpct']['uncm']
	up = ct['rpct']['uncp']
	
	ax1.step(x, y, label=ct['name']+'rpct', color='indianred', lw=1)
	if len(um)>0:
		plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='indianred', lw=0.5)
	#ax1.plot(x,y, label='9', color='yellow', lw=1,drawstyle='steps-mid')#,where='mid')
	ax1.set_xlabel('Depth [mm]')
	ax1.set_ylabel('PG detected [counts]')
	#ax1.set_xlim(-0.5,5.5)
	ax1.set_title('PG detection')
	plot.texax(ax1)

ctset_61 = getctset(68442219,'outputct61','outputrpct61',5,'')
ctset_99 = getctset(113485124,'outputct99','outputrpct99',5,'')
ctset_101 = getctset(107739042,'outputct101','outputrpct101',5,'')
ctset_sum = sumctset(68442219+113485124+107739042,'sum',ctset_61,ctset_99,ctset_101)


#glob.glob("/home/brent/phd/scratch/doseactortest-stage2/**/ipnl-patient-spot-auger.root")


f, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

plotrange(ax1,ctset_61)
plotrange(ax2,ctset_99)
plotrange(ax3,ctset_101)
plotrange(ax4,ctset_sum)

#print '====== chisq CT w RPCT ====='
#print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '8,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_8['rpct']['av'])
#print '7,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_7['rpct']['av'])
#print '6,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_6['rpct']['av'])
	
#print '====== chisq CT w CT ====='
#print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['ct']['av'])
#print '9,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_9['ct']['av'])
#print '9,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_9['ct']['av'])
#print '9,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_9['ct']['av'])

#print '====== chisq RPCT w RPCT ====='
#print '9,9', chisquare(ctset_int_9['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '9,8', chisquare(ctset_int_8['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '9,7', chisquare(ctset_int_7['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '9,6', chisquare(ctset_int_6['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
	
f.savefig('spotsumplot.pdf', bbox_inches='tight')
plt.close('all')
