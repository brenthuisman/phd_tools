#!/usr/bin/env python
import plot,numpy as np

### plot loss of PGs
f, ax = plot.subplots(nrows=1, ncols=1)

photons = [1e9,1.27e8,0]
dosehits = [0,0,19476749]
#ax.set_ylim([5e3,5e8])
ind = np.arange(len(dosehits))
margin = 0.2
width = (1.-2.*margin)
xdata = ind- width/2.
labels = ["Primaries","Entering panel","Dose events"]

p1 = ax.bar(xdata, photons, width, color='k',lw=0)
p2 = ax.bar(xdata, dosehits, width, color='r',bottom=photons,lw=0)

#ax.set_xticklabels(labels, fontsize=8, rotation=15, ha='left')
ax.set_xticklabels(['']+labels, fontsize=8, rotation=15, ha='center')
#ax.legend((p1[0], p2[0]), ('Photons', 'Prompt Gammas'),frameon=False)

ax.set_ylabel('Counts')
#ax.set_title('Progressive loss of Prompt Gammas')
ax.set_yscale('log')
ax.set_ylim([5e3,5e8])
#f.savefig('lossofpgs.pdf', bbox_inches='tight')
f.savefig('lossofpgs.png', bbox_inches='tight',dpi=300)
plot.close('all')

