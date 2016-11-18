#!/usr/bin/env python
import image,sys,numpy as np,rtplan,plot
from dta import gamma_evaluation 

infile = 'dosespotid.2gy.reldiff.mhd'

rtplan = rtplan.rtplan('data/plan.txt')
newspots=[]
for spot in rtplan.spots:
	if spot[0] == 2:
		newspots.append(spot)

#plastimatch gamma --dose-tolerance 0.02 --dta-tolerance 4 --output gammaindex.mhd results.vF3d/dosespotid.3d.2gy.mhd results.7Dee/dosespotid.3d.2gy.mhd
#usual criterium: percentage of voxel with index =< 1 is measure of sameness (many values over 1 is dissimilar)
#mean gamma value can also be used.

dose3dCT = image.image('results.vF3d/dosespotid.3d.2gy.mhd')
dose3dCT.to90pcmask()
dose3dRPCT = image.image('results.7Dee/dosespotid.3d.2gy.mhd')
dose3dRPCT.to90pcmask()

dose3dCT.unionmask(dose3dRPCT)
mask = dose3dCT.imdata.reshape(dose3dCT.imdata.shape[::-1])

spotim = image.image(infile)
#data = spotim.imdata
#data = np.rollaxis(spotim.imdata,3)
data = spotim.imdata.reshape(spotim.imdata.shape[::-1])
rmse = []
nprim = []
E = []

for i,spot in enumerate(data):
	#if i == 61:
		#dose3dCT.imdata = spot*mask
		#dose3dCT.imdata = dose3dCT.imdata.astype(np.float32,copy=False)
		#dose3dCT.saveas('TEST')
	rmse.append(np.sqrt(np.mean(np.square(spot*mask))))
	#rmse.append(np.sqrt(np.mean(np.square(spot))))
	nprim.append(newspots[i][4])
	E.append(newspots[i][1])

Eh, Ehbin = np.histogram(E,bins=30)
nprimh, nprimhbin = plot.getloghist(nprim,30)

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

ax1.set_title('Dose Diff (nprim)')
ax1.set_xlabel('Number of Primaries')
ax1.set_ylabel('Dose Diff [RMSE]')
plot.texax(ax1)

ax2.set_title('Dose Diff (E)')
ax2.set_xlabel('Energy [MeV]')
ax2.set_ylabel('Dose Diff [RMSE]')
plot.texax(ax2)

ax3.set_title('Dose Diff (nprim)')
ax3.set_xlabel('Number of Primaries')
ax3.set_ylabel('Dose Diff [RMSE]')
plot.texax(ax3)

ax4.set_title('Dose Diff (E)')
ax4.set_xlabel('Energy [MeV]')
ax4.set_ylabel('Dose Diff [RMSE]')
plot.texax(ax4)

ax1.scatter(nprim,rmse,marker='x',alpha=0.1,c='black',clip_on=False)
ax1.semilogx()
ax1.semilogy()
ax1.set_xlim(min(nprim),max(nprim))
ax1.set_ylim(min(rmse),max(rmse))

ax2.scatter(E,rmse,marker='x',alpha=0.1,c='black',clip_on=False)
ax2.semilogy()
ax2.set_xlim(min(E),max(E))
ax2.set_ylim(min(rmse),max(rmse))

ax3.step(nprimh, nprimhbin,c='black')
ax3.semilogx()
ax3.set_xlim(min(nprim),max(nprim))
#ax3.set_ylim(min(rmse),max(rmse))

ax4.hist(E,19,color='black')
ax4.set_xlim(min(E),max(E))
#ax4.set_ylim(min(rmse),max(rmse))








f.savefig(infile.replace('.','-')+'-plot.pdf', bbox_inches='tight')
plot.close('all')
