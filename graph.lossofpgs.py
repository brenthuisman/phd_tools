#!/usr/bin/env python
import sys,plot,numpy as np,matplotlib.pyplot as plt

### plot loss of PGs
f, ax = plt.subplots(nrows=1, ncols=1)

# numbers = [4.00E+10,2.00E+08,4.60E+07,1.80E+06,3.40E+04,1.60E+04,4E+03]
protons = [2.00E+08,0,0,0,0,0]
pgs = [0,4.60E+07,1.80E+06,3.40E+04,1.60E+04,8E+03]
pgs = [0,4.60E+07,1.80E+06,3.40E+04,3.40E+04*.66,3.40E+04*.66*.66]
ax.set_ylim([5e3,5e8])
ind = np.arange(len(pgs))
margin = 0.2
width = (1.-2.*margin)
xdata = ind- width/2.
labels = ["Primaries","PGs Exiting patient","Solid angle detector","Post-collimator","Detector Efficiency ?","Reconstruction Eff. ?"]

p1 = ax.bar(xdata, protons, width, color='k',lw=0)
p2 = ax.bar(xdata, pgs, width, color='r',bottom=protons,lw=0)

#ax.set_xticklabels(labels, fontsize=8, rotation=15, ha='left')
ax.set_xticklabels(['']+labels, fontsize=8, rotation=15, ha='center')
ax.legend((p1[0], p2[0]), ('Protons', 'Prompt Gammas'),frameon=False)

ax.set_ylabel('Counts')
#ax.set_title('Progressive loss of Prompt Gammas')
ax.set_yscale('log')
ax.set_ylim([5e3,5e8])
plot.texax(ax)
f.savefig('lossofpgs.pdf', bbox_inches='tight')
f.savefig('lossofpgs.png', bbox_inches='tight',dpi=300)
plt.close('all')

