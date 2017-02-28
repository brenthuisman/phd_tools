#!/usr/bin/env python
import dump,plot
from collections import Counter

clrs=plot.colors

#plot depth dose of some particles.

files = {
'Electron (20 MeV)':'output/dose-e--20-Dose.root',
'Photon (6 MeV)':'output/dose-gamma-6-Dose.root',
'Helium (700 MeV)':'output/dose-alpha-700-Dose.root',
'Proton (177 MeV)':'output/dose-proton-177-Dose.root',
'Pion^{+} (84 MeV)':'output/dose-pi+-84-Dose.root',
'Carbon (4 Gev)':'output/dose-ion-4000-Dose.root'
}

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

for index,(key,val) in enumerate(files.iteritems()):
	data = dump.thist2np(val)['histo']
	maxi=max(data)
	plot.plot([x/maxi for x in data], label=key)

ax1.set_ylabel('Dose (normalized)')
ax1.set_xlabel('Depth (mm)')
ax1.set_title('Dose as function of depth for some particles')
plot.texax(ax1)
ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.),frameon=False)
f.savefig('depthdose.pdf', bbox_inches='tight')
plot.close('all')

