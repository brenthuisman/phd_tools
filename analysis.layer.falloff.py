#!/usr/bin/env python
import numpy as np,plot,auger

#np.random.seed(65983247)

#########################################################################################################

#typ='ipnl-auger-notof-1.root'
#typ='ipnlf-auger-tof-1.root'
#typ='ipnlf-auger-notof-1.root'
#typ='iba-auger-tof-3.root'

typ='ipnl-auger-tof-1.root'
typ='iba-auger-notof-3.root'

#we dont know what the added or reduced noise level is when changing energy windows, so we cant compare performance for ipnl3 and iba1.
#we could study the signal only.

#geolayaers
geolabels = ["mid","75\%","dist 2","dist"]
ctset_dist = auger.getctset(197149701,'run.YKEk','run.pwy4',typ) #-1
ctset_dist2 = auger.getctset(395650000,'run.C8rL','run.r0LF',typ) # -1-2
ctset_75 = auger.getctset(1381819491,'run.oVKm','run.dltw',typ) # -6
ctset_mid = auger.getctset(1428709464,'run.LqMK','run.WZUT',typ) # -12

#elayers
elabels = ["mid","75\%","dist"]
ctset_dist_e = auger.getctset(488628830,'run.Mwtv','run.EKMm',typ) # 0
ctset_75_e = auger.getctset(1285014551,'run.gFh9','run.q4DU',typ) # 10
ctset_mid_e = auger.getctset(976598251,'run.G8o6','run.UQ32',typ) # 24


#########################################################################################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodiffdist(ax1,ctset_mid,0,geolabels)
auger.plotfodiffdist(ax1,ctset_75,1,geolabels)
auger.plotfodiffdist(ax1,ctset_dist2,2,geolabels)
auger.plotfodiffdist(ax1,ctset_dist,3,geolabels)

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
fig.savefig(typ+'-spot-falloffdiffdist-geo.pdf')#, bbox_inches='tight')
plt.close('all')

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodiffdist(ax1,ctset_mid_e,0,elabels)
auger.plotfodiffdist(ax1,ctset_75_e,1,elabels)
auger.plotfodiffdist(ax1,ctset_dist_e,2,elabels)

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
fig.savefig(typ+'-spot-falloffdiffdist-E.pdf')#, bbox_inches='tight')
plt.close('all')

#########################################################################################################

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodist(ax1,ctset_mid,0,geolabels)
auger.plotfodist(ax1,ctset_75,1,geolabels)
auger.plotfodist(ax1,ctset_dist2,2,geolabels)
auger.plotfodist(ax1,ctset_dist,3,geolabels)

#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
plt.savefig(typ+'-spot-falloffdist-geo.pdf')#, bbox_inches='tight')
plt.close('all')

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodist(ax1,ctset_mid_e,0,elabels)
auger.plotfodist(ax1,ctset_75_e,1,elabels)
auger.plotfodist(ax1,ctset_dist_e,2,elabels)

#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
plt.savefig(typ+'-spot-falloffdist-E.pdf')#, bbox_inches='tight')
plt.close('all')
