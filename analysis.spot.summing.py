#!/usr/bin/env python
import dump, numpy as np,matplotlib.pyplot as plt,plot,sys,glob2 as glob,copy
from scipy.stats import chisquare,norm

#np.random.seed(65983247)

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
	dat1 = ct['ct']['data'][0]
	um = ct['ct']['uncm']
	up = ct['ct']['uncp']
	
	if len(um)>0:
		plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='steelblue', lw=0.5,clip_on=False)
	else:
		ax1.step(x, dat1, label=ct['name']+'ct', color='steelblue', lw=1,clip_on=False)
	
	x = ct['rpct']['x']
	y = ct['rpct']['av']
	dat1 = ct['rpct']['data'][0]
	um = ct['rpct']['uncm']
	up = ct['rpct']['uncp']
	
	if len(um)>0:
		plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='indianred', lw=0.5,clip_on=False)
	else:
		ax1.step(x, dat1, label=ct['name']+'ct', color='indianred', lw=1,clip_on=False)
	#ax1.plot(x,y, label='9', color='yellow', lw=1,drawstyle='steps-mid')#,where='mid')
	ax1.set_xlabel('Depth [mm]')
	ax1.set_ylabel('PG detected [counts]')
	#ax1.set_xlim(-0.5,5.5)
	#ax1.set_title('PG detection')
	ax1.set_ylim(bottom=0)
	plot.texax(ax1)

################################################################################

#oude sums.

#typ='ipnl'
#ctset_61 = getctset(68442219,'outputct61','outputrpct61',typ)
#ctset_99 = getctset(113485124,'outputct99','outputrpct99',typ)
#ctset_101 = getctset(107739042,'outputct101','outputrpct101',typ)

#f, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

#plotrange(ax1,ctset_61)
#plotrange(ax2,ctset_99)
#plotrange(ax3,ctset_101)

#ctset_sum = sumctset('sum',ctset_61,ctset_99,ctset_101) #we appear to modift ctset_61 if unc = 1
#plotrange(ax4,ctset_sum)

##print '====== chisq CT w RPCT ====='
##print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '8,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_8['rpct']['av'])
##print '7,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_7['rpct']['av'])
##print '6,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_6['rpct']['av'])
	
##print '====== chisq CT w CT ====='
##print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['ct']['av'])
##print '9,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_9['ct']['av'])
##print '9,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_9['ct']['av'])
##print '9,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_9['ct']['av'])

##print '====== chisq RPCT w RPCT ====='
##print '9,9', chisquare(ctset_int_9['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '9,8', chisquare(ctset_int_8['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '9,7', chisquare(ctset_int_7['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '9,6', chisquare(ctset_int_6['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
	
#f.savefig('spotplot-sums.pdf', bbox_inches='tight')
#plt.close('all')

################################################################################

typ='ipnl'
typ='iba'
#nieuwe sums. distal layer
#22 , 4 ,
#4 : 65802598.6018 , 7 : 88235302.6706 , 10 : 67298112.2064 , 43 : 64073566.2641 , 

ctset_4 = getctset(65802598,'run.Zz8R','run.1yzX',typ)
ctset_7 = getctset(88235302,'run.EUR3','run.p5iV',typ)
ctset_10 = getctset(67298112,'run.VeCV','run.8hHW',typ)
ctset_43 = getctset(64073566,'run.v7Bm','run.fxhV',typ)

ctset_sum_0 = sumctset('sum',ctset_4,ctset_7,ctset_10,ctset_43)

f, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(nrows=2, ncols=3, sharex=False, sharey=False)

plotrange(ax1,ctset_4)
plotrange(ax2,ctset_7)
plotrange(ax3,ctset_10)
plotrange(ax4,ctset_43)
ax5.axis('off')
plotrange(ax6,ctset_sum_0)

f.savefig(typ+'-spotsums-0.pdf', bbox_inches='tight')
plt.close('all')

#nieuwe sums. distal-1 layer
#18 , 5 , 
#6 : 58325030.5789 , 9 : 65802598.6018 , 28 : 54600663.4 , 32 : 66406212.2432 , 39 : 42230305.0377 , 

ctset_6 = getctset(68442219,'run.4Squ','run.QT1Z',typ)
ctset_9 = getctset(113485124,'run.HJWo','run.U2eT',typ)
ctset_28 = getctset(107739042,'run.XZJh','run.Z7sc',typ)
ctset_32 = getctset(113485124,'run.uwDg','run.Qjze',typ)
ctset_39 = getctset(113485124,'run.v6Nd','run.KCMn',typ)

ctset_sum_1 = sumctset('sum',ctset_6,ctset_9,ctset_28,ctset_32,ctset_39)

f, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(nrows=2, ncols=3, sharex=False, sharey=False)

plotrange(ax1,ctset_6)
plotrange(ax2,ctset_9)
plotrange(ax3,ctset_28)
plotrange(ax4,ctset_32)
plotrange(ax5,ctset_39)
plotrange(ax6,ctset_sum_1)

f.savefig(typ+'-spotsums-1.pdf', bbox_inches='tight')
plt.close('all')
