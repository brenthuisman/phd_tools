#!/usr/bin/env python
import numpy as np,plot,auger

#np.random.seed(65983247)

#########################################################################################################

#typ='ipnl'
typ='ipnlf'
#typ='iba'

typ+='-auger-tof-1.root'
#typ+='-auger-tof-3.root'
#typ+='-auger-notof-1.root'
#typ+='-auger-notof-3.root'

#ctset_int_9 = auger.getctset(1e9,'run.xTcG','run.b2Aj',typ)
#ctset_int_6 = auger.getctset(1e6,'run.yjzw','run.wfmx',typ)
#ctset_int_7 = auger.getctset(1e7,'run.41VE','run.NE7B',typ)
#ctset_int_8 = auger.getctset(1e8,'run.bfrX','run.rOx1',typ)

#nieuw, per ongeluk ook /params gelaunched
#ctset_int_6 = auger.getctset(1e6,'run.Wi8r','run.EWkk',typ)#Chmd0kbq
#ctset_int_7 = auger.getctset(1e7,'run.p8Ka','run.R0Vm',typ)#eZUoFdCA
#ctset_int_8 = auger.getctset(1e8,'run.thhg','run.pYMB',typ)#MXDeqfA3
#ctset_int_9 = auger.getctset(1e9,'run.mJ3k','run.E8EC',typ)#M0YetFT6
#ipnlf, per ongeluk ook /params gelaunched
ctset_int_6 = auger.getctset(1e6,'run.K4XZ','run.rYCr',typ)#ftvabsYW
ctset_int_7 = auger.getctset(1e7,'run.z6KS','run.YCOL',typ)#9cynNgPF
ctset_int_8 = auger.getctset(1e8,'run.Urwi','run.Ghea',typ)#ruRlYegH
ctset_int_9 = auger.getctset(1e9,'run.LsBG','run.pPs7',typ)#2gFE6CuZ

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
auger.plotfodiffdist(ax1,ctset_int_8,10)
auger.plotfodiffdist(ax1,ctset_int_7,20)
auger.plotfodiffdist(ax1,ctset_int_6,30)
#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
fig.savefig(typ+'-spot-falloffdiffdist.pdf')#, bbox_inches='tight')
plt.close('all')

#########################################################################################################

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodist(ax1,ctset_int_9,0)
auger.plotfodist(ax1,ctset_int_8,10)
auger.plotfodist(ax1,ctset_int_7,20)
auger.plotfodist(ax1,ctset_int_6,30)

#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
plt.savefig(typ+'-spot-falloffdist.pdf')#, bbox_inches='tight')
plt.close('all')
