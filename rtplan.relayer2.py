#!/usr/bin/env python
import image,numpy as np,rtplan,auger
from collections import Counter
from tableio import write

#################################################################################

# PARAMS

rtpfile = 'data/plan.txt'
doseimage = 'output/new_dosespotid-ct.mhd'
field = 2
minnprim = 5e8 #find spots in either elayers or geolayers starting from the back.
shifttolerance = 4
shifttolerance = False

#################################################################################

orirtp = rtplan.rtplan([rtpfile],norm2nprim=False)#,MSWtoprotons=False)
MSW=[]
for spot in orirtp.spots:
	if spot[0] == 100+field:#
		MSW.append(spot)

# make e-layer grouping, simply start from beginning and start adding spots until total nprim sum is 5e8.
elay_fospotlist = []
elay_sum=0.
for ind,spot in enumerate(MSW):
	if elay_sum > minnprim:
		break
	elay_sum += spot[-1]
	elay_fospotlist.append(ind)
	
rtplan.rtplan([rtpfile],noproc=True,spotlist=elay_fospotlist,fieldind=field,relayername='elay5e8')

print 'Relayering complete based on elayers. Nprim:',elay_sum

# now, find fops, loop over from distal end until 5e8 reached

im = image.image(doseimage)
ct = im.imdata.reshape(im.imdata.shape[::-1]).squeeze()

xhist = np.linspace(-150,150,301) #1mm voxels, endpoints
x = np.linspace(-149.5,149.5,300) #bincenters

falloffs = []
falloffs_valid = []

for spindex,spot in enumerate(ct):
	
	fop = auger.get_fop(x,spot)
	falloffs.append(fop)
	
	if shifttolerance:
		# ensure a shift calculated at 20% and 80% height within 1mm of shift computed at default 50%
		fop2 = auger.get_fop(x,spot,threshold=0.2)
		fop8 = auger.get_fop(x,spot,threshold=0.8)
		
		if np.isclose([fop2,fop8],fop,atol=float(shifttolerance)).all():
			# all values in *ctfops are within 1.0 (mm) of *ctfop. it is a front shift
			falloffs_valid.append(True)
		else:
			falloffs_valid.append(False)
	else:
		falloffs_valid.append(True)
		
	print 'Spot', spindex, 'analyzed!'
	
	#lets save some time!
	if spindex > int(minnprim/1e7):
		break

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

print fospotlist

#sla plat
ll = sum(fospotlist, [])

geolay_fospotlist = []
geolay_sum=0.
for spot in ll[::-1]: #now we must start from the back
	if geolay_sum > minnprim:
		break
	geolay_sum += MSW[spot][-1]
	geolay_fospotlist.append(spot)
	
geolay_fospotlist.sort()

print 'Relayering complete based on geolayers. Nprim:',geolay_sum

rtplan.rtplan([rtpfile],noproc=True,spotlist=geolay_fospotlist,fieldind=field,relayername='geolay5e8')
