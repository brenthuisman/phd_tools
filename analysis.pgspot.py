#!/usr/bin/env python
import dump, numpy as np,matplotlib.pyplot as plt,plot,sys
from scipy.stats.mstats import chisquare

clrs=plot.colors

rootn='ipnl-patient-spot-auger.root'

#glob.glob("/home/brent/phd/scratch/doseactortest-stage2/**/ipnl-patient-spot-auger.root")

def getctset(ct1,ct2,unc=5,prefix=''):
	ctset6 = {'ct':{},'rpct':{}}
	ctset6['ct']['path'] = ct1
	ctset6['rpct']['path'] = ct2
	ctset6['ct']['data'] = []
	ctset6['rpct']['data'] = []
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
				ctset6['ct']['data'].append(val)
	for filen in ctset6['rpct']['files']:
		ffilen = ctset6['rpct']['path']+'/'+filen+'/'+rootn
		print 'opening',ffilen
		for key,val in dump.thist2np_xy(ffilen).items():
			#print key
			if key == 'reconstructedProfileHisto':
				#print val
				ctset6['rpct']['data'].append(val)
	return ctset6



#ctset_int_6 = getctset('test61ct','test61rpct',5,'6-')
#ctset_int_7 = getctset('test61ct','test61rpct',5,'7-')
#ctset_int_8 = getctset('test61ct','test61rpct',5,'8-')
ctset_int_9 = getctset('test61ct','test61rpct',1,'9')

#f, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)
f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

for sset in ctset_int_9['ct']['data']:
	ax1.plot(sset[0], sset[1], label='9', color='steelblue', lw=1)
	ax1.set_xlabel('Depth [mm]')
	ax1.set_ylabel('PG detected [counts]')
	#ax1.set_xlim(-0.5,5.5)
	ax1.set_title('PG detection')
	plot.texax(ax1)
for sset in ctset_int_9['rpct']['data']:
	ax1.plot(sset[0], sset[1], label='9', color='yellow', lw=1)
	ax1.set_xlabel('Depth [mm]')
	ax1.set_ylabel('PG detected [counts]')
	#ax1.set_xlim(-0.5,5.5)
	ax1.set_title('PG detection')
	plot.texax(ax1)
	
	
print len(ctset_int_9['ct']['data'][0][1]),len(ctset_int_9['rpct']['data'][0][1])
print chisquare(ctset_int_9['ct']['data'][0][1],ctset_int_9['rpct']['data'][0][1])
	
f.savefig('spotplot.pdf', bbox_inches='tight')
plt.close('all')








sys.exit()

### mfp
for key,val in dump.thist2np_xy("output/mfp.root").items():
    f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
    x = [val[0][0]] + val[0] + [val[0][-1]]
    y = [val[1][0]] + val[1] + [val[1][-1]]
    #ax1.plot(x,y, label=key, color='steelblue',fillstyle='full',lw=0.5,drawstyle='steps-mid')#,where='mid')
    ax1.bar(x, y, width=1, align='center', label=key, color='steelblue', lw=0)
    #ax1.hist(y, histtype='stepfilled', color='steelblue')
    if key == 'PG per NI':
        ax1.set_xlabel('Number of Prompt Gammas')
        ax1.set_ylabel('Number of Nuclear Interactions')
        ax1.set_xlim(-0.5,5.5)
        ax1.set_title('PG/NI for $10^5$ protons')
    plot.texax(ax1)
    f.savefig(key+'.pdf', bbox_inches='tight')
    plt.close('all')

### tracklengths plot
#f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

#y_data = image.image("output/source-debugtrackl.mhd").imdata.flatten()
#x_axis=np.linspace(0,200,250)

#ax1.step(x_axis,y_data, label='Tracklengths', color=clrs[0],lw=0.5)
##ax1.set_xlim(0,30)
#ax1.set_ylabel('Tracklength [mm]')
#ax1.set_xlabel('$E_p$ [MeV]')
#ax1.set_title('Cumulative tracklength distribution')
#plot.texax(ax1)
##lgd = ax1.legend(loc='upper right',frameon=False, bbox_to_anchor=(1.2, 1.))
#f.savefig('trackl.pdf', bbox_inches='tight')
#plt.close('all')
