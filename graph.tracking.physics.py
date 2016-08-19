#!/usr/bin/env python
import numpy as np,matplotlib as mpl,matplotlib.pyplot as plt,plot,sys
from collections import Counter
clrs=plot.colors

#plot the physicsprocesses per step in a Gate log
f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

hist=[]
sourcefile = open(sys.argv[-1],'r')
for line in sourcefile:
	newline = line.strip()
	if '_phys' in newline:
		hist.append(newline.split()[9])
#cntr = dict(Counter(hist).most_common(8))
cntr = Counter(hist)

ind = np.arange(len(cntr))
margin = 0.2
width = (1.-2.*margin)
xdata = ind - width/2.

ax1.bar(xdata, cntr.values(), width, color=clrs[0],lw=0)
ax1.xaxis.set_major_locator(mpl.ticker.FixedLocator(range(len(cntr))))
ax1.set_xticklabels(cntr.keys(), fontsize=8, rotation=30, ha='center')
#ax1.set_xticklabels(['']+cntr.keys(), fontsize=8, rotation=15, ha='center')

ax1.set_ylabel('Counts')
ax1.set_title('Physics processes in Geant4')
ax1.set_yscale('log')
#ax1.set_ylim([5e3,5e8])
plot.texax(ax1)
f.savefig('physicstracking.pdf', bbox_inches='tight')
f.savefig('physicstracking.png', bbox_inches='tight',dpi=300)
plt.close('all')

