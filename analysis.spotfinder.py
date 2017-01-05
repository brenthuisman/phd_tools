#!/usr/bin/env python
import image,sys,numpy as np,rtplan,auger,plot
from collections import Counter
from tableio import write

rtplan = rtplan.rtplan(['data/plan.txt'],norm2nprim=False)#,noproc=True)

#print rtplan.ConvertMuToProtons(4.73,148.78)
#print rtplan.ConvertMuToProtons(62.05-48.74,134.68)
#print rtplan.ConvertMuToProtons(162.35-151.15,116.66)
#quit()

MSW=[]
for spot in rtplan.spots:
	if spot[0] == 102:#
		MSW.append(spot)

spotim_ct = image.image("results.vF3d/dosespotid.2gy.mhd")
spotim_ct3d = image.image("results.vF3d/dosespotid.3d.2gy.mhd")
#spotim_ct3d.to90pcmask
spotim_ct3d.toprojection(".x", [0,1,1,1])

################################################################################

ct = spotim_ct.imdata.reshape(spotim_ct.imdata.shape[::-1])

xhist = np.linspace(-150,150,76) #4mm voxels, endpoints
x = np.linspace(-148,148,75) #bincenters
#print x[0],x[1],x[-1],len(x)
#print xhist[0],xhist[1],xhist[-1],len(xhist)

falloffs = []

#f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
for spindex,spot in enumerate(ct):
	#from __crush
	#print spot.shape
	crush = [0,1,1] #x
	
	crush=crush[::-1]
	#spot = spot.reshape(spot.shape[::-1])
	
	ax = [i for (i,j) in zip(range(len(crush)),crush) if j==1]
	spot = np.add.reduce(spot, axis=tuple(ax))

	spot = spot.reshape(spot.shape[::-1])
	#print spot.shape
	#print spot
	
	fo=auger.ipnl_fit_range(x,spot)
	falloffs.append(fo)
	
	#if spindex in [4, 7, 10, 32, 43]:
		##print spot
		#ax1.step( x ,spot, color='moccasin')
		
		#ax1.axvline(fo,color='green',alpha=0.5)
		#print len(newspots)
		#print newspots[spindex]

#f.savefig('dose-ranges.pdf', bbox_inches='tight')
#plot.close('all')

################################################################################

#bin spots and get spotcount.
indices = np.digitize(falloffs,x)
ind_counter = Counter(indices)
# falloffs and x[indices] are identical. Comprende?
y,bins=np.histogram(falloffs,xhist)
#y,bins=np.histogram(x[indices],xhist)

y_msw = []
for ind,x_val in enumerate(x):
	binmsw = 0.
	if ind_counter[ind] > 0:
		print x_val,',', ind_counter[ind],',', 
		for spotind,i in enumerate(indices):
			if ind == i:
				binmsw += MSW[spotind][-1]
				#print spotind#,':',MSW[spotind][-1],',',
				#print MSW[spotind]
		#if newMSW > 0:
			#print plot.sn(newMSW/ind_counter[ind]),
			#print plot.sn(newMSW),
		#print ''
	y_msw.append(binmsw)


print y_msw


f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
ax1.step(x,y, color='indianred',lw=1., label='Geometric layers')
ax1.step(x,spotim_ct3d.imdata/spotim_ct3d.imdata.max()*float(y.max()), color='steelblue',lw=1., label='Integral dose (scaled)')
ax1.set_xlabel('FOP [mm]')
ax1.set_ylabel('Number of spots')
ax1.set_xlim(-60,25)
ax1.set_ylim(0,140)

ax1.legend(frameon = False)#,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'upper right')
plot.texax(ax1)

ax2.semilogy()
ax2.step(x,y_msw, color='forestgreen',lw=1., label='Protons')
ax2.set_xlim(-60,25)
ax2.set_ylim(5e7,5e9)
ax2.set_xlabel('FOP [mm]')
ax2.set_ylabel('Number of Protons')
ax2.legend(frameon = False)#,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'upper right')
#ax2.hist(x,bins=len(x)*10,weights=y_msw,bottom=min(x)/100.,histtype='bar',color='black')


plot.texax(ax2)

f.savefig('spotfinder.pdf', bbox_inches='tight')
plot.close('all')

################################################################################
