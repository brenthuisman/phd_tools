#!/usr/bin/env python
import dump, numpy as np,matplotlib.pyplot as plt,plot,image,scipy.ndimage,sys,collections

clrs=plot.colors

rootn='ipnl-patient-spot-auger.root'

#glob.glob("/home/brent/phd/scratch/doseactortest-stage2/**/ipnl-patient-spot-auger.root")

#CtSet = collections.namedtuple('CtSet', 'ct rpct')

#ctset6 = CtSet('test61ct','test61rpct')

#print ctset6.ct #= []

ctset6 = {'ct':{},'rpct':{}}
ctset6['ct']['path'] = 'test61ct'
ctset6['ct']['files'] = ['6','6-2','6-3','6-4','6-5']
ctset6['rpct']['path'] = 'test61rpct'
ctset6['rpct']['files'] = ['6','6-2','6-3','6-4','6-5']

for filen in ctset6['ct']['files']:
	ffilen = ctset6['ct']['path']+'/'+filen+'/'+rootn
	print 'opening',ffilen
	for key,val in dump.thist2np_xy(ffilen).items():
		print key
		if key == 'reconstructedProfileHisto':
			print val


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
