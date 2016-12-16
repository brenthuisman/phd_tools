#!/usr/bin/env python
import image,numpy as np,rtplan,auger
from collections import Counter
from tableio import write

#################################################################################

# PARAMS

rtpfile = 'data/plan.txt'
doseimage = 'results.vF3d/dosespotid.2gy.mhd'
field = 2
geolayer = slice(-2,None)

#################################################################################

# CODE

orirtp = rtplan.rtplan([rtpfile],noproc=True)#,MSWtoprotons=False)
MSW=[]
for spot in orirtp.spots:
	if spot[0] == 100+field:#
		MSW.append(spot)

spotim_ct = image.image(doseimage)#"results.vF3d/dosespotid.2gy.mhd")

ct = spotim_ct.imdata.reshape(spotim_ct.imdata.shape[::-1])

xhist = np.linspace(-150,150,76) #4mm voxels, endpoints
x = np.linspace(-148,148,75) #bincenters
#print x[0],x[1],x[-1],len(x)
#print xhist[0],xhist[1],xhist[-1],len(xhist)

falloffs = []

for spindex,spot in enumerate(ct):
	crush = [0,1,1] #x
	
	crush=crush[::-1]
	
	ax = [i for (i,j) in zip(range(len(crush)),crush) if j==1]
	spot = np.add.reduce(spot, axis=tuple(ax))

	spot = spot.reshape(spot.shape[::-1])
	
	fo=auger.ipnl_fit_range(x,spot)
	falloffs.append(fo)

indices = np.digitize(falloffs,x)
ind_counter = Counter(indices)
# falloffs and x[indices] are identical. Comprende?

fospotlist = []

for ind,x_val in enumerate(x):
	fospotlist.append([])
	for spotind,i in enumerate(indices):
		if ind == i:
			fospotlist[-1].append(spotind)
	if len(fospotlist[-1]) == 0:
		fospotlist.pop()

#sla plat
ll = sum(fospotlist[geolayer], [])
llname = str('0' if geolayer.start == None else geolayer.start) + str('-1' if geolayer.stop == None else geolayer.stop)
print ll, llname, field
rtplan.rtplan([rtpfile],noproc=True,spotlist=ll,fieldind=field,relayername=llname)
