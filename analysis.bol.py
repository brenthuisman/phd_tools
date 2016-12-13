#!/usr/bin/env python
import numpy as np,plot,auger
from scipy.stats import chisquare

#np.random.seed(659873247)

ctset_ipnl = auger.getctset(610322581,'run.rTWI','run.7C9Z','ipnl')

ctset_iba = auger.getctset(610322581,'run.rTWI','run.7C9Z','iba')

f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)

auger.plotrange(ax1,ctset_ipnl)
auger.plotrange(ax2,ctset_iba)

ax1.set_title('IPNL '+plot.sn(610322581)+'prims')
ax2.set_title('IBA '+plot.sn(610322581)+'prims')

f.savefig('layer-sphere.pdf', bbox_inches='tight')
plot.close('all')

#########################################################################################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodiffdist(ax1,ctset_ipnl,0)
auger.plotfodiffdist(ax1,ctset_iba,10)
#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
fig.savefig('layer-sphere-falloffdiffdist.pdf')#, bbox_inches='tight')
plt.close('all')

#########################################################################################################

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.view_init(30, -50)

auger.plotfodist(ax1,ctset_ipnl,0)
auger.plotfodist(ax1,ctset_iba,10)

#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
plt.savefig('layer-sphere-falloffdist.pdf')#, bbox_inches='tight')
plt.close('all')
