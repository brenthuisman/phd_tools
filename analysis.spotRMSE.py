#!/usr/bin/env python
import image,sys,numpy as np,rtplan,matplotlib.pyplot as plt,plot
from collections import Counter

rtplan = rtplan.rtplan('data/plan.txt')
newspots=[]
for spot in rtplan.spots:
	if spot[0] == 2:
		newspots.append(spot)


spotim = image.image(sys.argv[-1])
data = np.rollaxis(spotim.imdata,3)
rmse = []
nprim = []
E = []
for i,spot in enumerate(data):
	rmse.append(np.sqrt(np.mean(np.square(spot))))
	nprim.append(newspots[i][4])
	E.append(newspots[i][1])


Eh, Ehbin = np.histogram(E,bins=30)
nprimh, nprimhbin = plot.getloghist(nprim,30)

f, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

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








f.savefig(sys.argv[-1].replace('.','-')+'-plot.pdf', bbox_inches='tight')
plt.close('all')
