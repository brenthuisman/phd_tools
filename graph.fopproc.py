#!/usr/bin/env python
import image,numpy as np,auger,plot,dump
from scipy.ndimage.filters import gaussian_filter

np.random.seed(65983146)

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

#spot 29 CT

filen = 'run.pMSA/output.2391740/ipnl-auger-tof-1.root'
auger.testfit(filen,1e9,ax1)

filen = 'run.EPjL/output.2391621/ipnl-auger-tof-1.root'
auger.testfit(filen,1e7,ax2)

filen = 'run.pMSA/output.2391740/iba-auger-notof-3.root'
auger.testfit(filen,1e9,ax3)

filen = 'run.EPjL/output.2391621/iba-auger-notof-3.root'
auger.testfit(filen,1e7,ax4)


#ax1.set_title(labels[0])
#ax2.set_title(labels[1])
#ax3.set_title(labels[2])
#ax4.set_title(labels[3])
#f.subplots_adjust(hspace=.5)
ax1.set_xlabel('')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax4.set_ylabel('')
f.savefig('fopproc.pdf', bbox_inches='tight')
plot.close('all')

