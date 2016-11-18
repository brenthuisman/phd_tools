#!/usr/bin/env python
import dump, numpy as np,plot,sys,glob2 as glob,matplotlib.pyplot as plt

rootn='ipnl-patient-spot-auger.root'
#rootn='iba-patient-spot-auger.root'

filelist = glob.glob("./**/ipnl-patient-spot-auger.root")
data=[]
x=[]

for ffilen in filelist:
	print 'opening',ffilen
	for key,val in dump.thist2np_xy(ffilen).items():
		#print key
		if key == 'reconstructedProfileHisto':
			#print val
			x = val[0] #no need to append, is same for all
			data.append([i/max(val[1]) for i in val[1]])

#print len(x)
a = np.vstack(data)
a = np.rollaxis(a,1)

#plt.imshow(a, cmap='hot', interpolation='nearest')
#plt.show()
#quit()

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

#for abin in a:
	#ax1.step(range(len(abin)), abin, label='', color='steelblue', lw=1)

ax1.step(range(len(a[0])), a[0], label='', color='steelblue', lw=1)

ax1.set_xlabel('Depth [mm]')
ax1.set_ylabel('PG detected [counts]')
#ax1.set_xlim(-0.5,5.5)
ax1.set_ylim(bottom=0)
ax1.set_title('PG detection')
plot.texax(ax1)
f.savefig('poisontest.pdf', bbox_inches='tight')
plot.close('all')
