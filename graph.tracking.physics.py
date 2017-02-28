#!/usr/bin/env python
import numpy as np,matplotlib as mpl,plot,sys,re
from collections import Counter
clrs=plot.colors

#plot the physicsprocesses per step in a Gate log

hist=[]
sourcefile = open(sys.argv[-1],'r')
for line in sourcefile:
	newline = line.strip()
	if '_phys' in newline:
		hist.append(newline.split()[9])
#cntr = dict(Counter(hist).most_common(8))
cntr = Counter(hist)
labels = '-'.join(cntr.keys())

d = {
'nCapture':'Neutron Capture',
'hIoni':'Hadron Ionisation',
'Transportation':'Transportation',
'StepLimiter':'StepLimiter',
'ionIoni':'Ion Ionisation',
'phot':'Photo Electric Effect',
'initStep':'Initial Step',
'neutronInelastic':'Neutron Inelastic',
'hadElastic':'Hadron Elastic',
'compt':'Compton Scattering',
'Rayl':'Rayleigh Scattering',
'protonInelastic':'Proton Inelastic'
}

pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
labels = pattern.sub(lambda x: d[x.group()], labels)
labels = labels.split('-')


ind = np.arange(len(cntr))
margin = 0.2
width = (1.-2.*margin)
xdata = ind - width/2.


f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

ax1.bar(xdata, cntr.values(), width, color=clrs[0],lw=0)
ax1.xaxis.set_major_locator(mpl.ticker.FixedLocator(range(len(cntr))))
ax1.set_xticklabels(labels, fontsize=8, rotation=30, ha='center')
#ax1.set_xticklabels(['']+cntr.keys(), fontsize=8, rotation=15, ha='center')

ax1.set_ylabel('Counts')
ax1.set_title('Physics processes in Geant4')
ax1.set_yscale('log')
ax1.set_ylim(bottom=0.9)
plot.texax(ax1)
f.savefig('physicstracking.pdf', bbox_inches='tight')
#f.savefig('physicstracking.png', bbox_inches='tight',dpi=300)
plot.close('all')

