#!/usr/bin/env python
import numpy as np,plot,auger

#np.random.seed(65983247)

#########################################################################################################

typ='ipnl-auger-tof-1.root'
#typ='iba-auger-notof-3.root'

#typ='ipnl-auger-notof-1.root'
#typ='iba-auger-tof-3.root'
#typ='ipnl-auger-tof-3.root'
#typ='iba-auger-tof-1.root'
#typ='ipnl-auger-notof-3.root'
#typ='iba-auger-notof-1.root'

#ipnl FFFF
#typ='ipnlf-auger-tof-1.root'
#typ='ipnlf-auger-notof-1.root'

#we dont know what the added or reduced noise level is when changing energy windows, so we cant compare performance for ipnl3 and iba1.
#we could study the signal only.

#nieuw
#ctset_int_6 = auger.getctset(1e6,'run.rFN5','run.jUPf',typ)
#ctset_int_7 = auger.getctset(1e7,'run.AE5G','run.gK11',typ)
#ctset_int_8 = auger.getctset(1e8,'run.lNkm','run.ztcV',typ)
#ctset_int_9 = auger.getctset(1e9,'run.A3vG','run.9950',typ)

#waterbox
ctset_int_6 = auger.getctset(1e6,'run.WbDj','run.f9cL',typ)
ctset_int_7 = auger.getctset(1e7,'run.ngMk','run.Ho8b',typ)
ctset_int_8 = auger.getctset(1e8,'run.cj4U','run.RWsd',typ)
ctset_int_9 = auger.getctset(1e9,'run.kVk7','run.iias',typ)

#########################################################################################################

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

auger.plot_all_ranges(ax1,ctset_int_9)
auger.plot_all_ranges(ax2,ctset_int_8)
auger.plot_all_ranges(ax3,ctset_int_7)
auger.plot_all_ranges(ax4,ctset_int_6)
f.subplots_adjust(hspace=.5)
ax1.set_xlabel('')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax4.set_ylabel('')
f.savefig(typ+'-spot-falloff.pdf', bbox_inches='tight')
plot.close('all')

#########################################################################################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodiffdist(ax1,ctset_int_9,0)
auger.plotfodiffdist(ax1,ctset_int_8,1)
auger.plotfodiffdist(ax1,ctset_int_7,2)
auger.plotfodiffdist(ax1,ctset_int_6,3)
#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
fig.savefig(typ+'-spot-falloffdiffdist.pdf')#, bbox_inches='tight')
plt.close('all')

#########################################################################################################

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodist(ax1,ctset_int_9,0)
auger.plotfodist(ax1,ctset_int_8,1)
auger.plotfodist(ax1,ctset_int_7,2)
auger.plotfodist(ax1,ctset_int_6,3)

#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
plt.savefig(typ+'-spot-falloffdist.pdf')#, bbox_inches='tight')
plt.close('all')
