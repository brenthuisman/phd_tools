#!/usr/bin/env python
import image,numpy as np,rtplan,auger,pickle

rtplan = rtplan.rtplan(['data/plan.txt'],norm2nprim=False)#,noproc=True)

doseimage = 'output/new_dosespotid-ct.mhd'

shifttolerance = 8

################################################################################

im = image.image(doseimage)
ct = im.imdata.reshape(im.imdata.shape[::-1]).squeeze()

ct_xhist = np.linspace(-150,150,301) #2mm voxels, endpoints
ct_x = np.linspace(-149.5,149.5,300) #bincenters

falloffs = []
falloffs_valid = []

for spindex,spot in enumerate(ct):
	
	fop = auger.get_fop(ct_x,spot)
	falloffs.append(fop)
	
	#if shifttolerance:
		# ensure a shift calculated at 20% and 80% height within 1mm of shift computed at default 50%
	fop2 = auger.get_fop(ct_x,spot,threshold=0.2)
	fop8 = auger.get_fop(ct_x,spot,threshold=0.8)
	
	if np.isclose([fop2,fop8],fop,atol=float(shifttolerance)).all():
		# all values in *ctfops are within 8 (mm) of *ctfop. it is a front shift
		falloffs_valid.append(True)
	else:
		falloffs_valid.append(False)
	#else:
		#falloffs_valid.append(True)
		
	print 'Spot', spindex, 'analyzed!', "Pass",falloffs_valid[-1]
	#lets save some time!
	#if spindex > int(minnprim/1e7):
		#break

print 'discarded spots:',falloffs_valid.count(False)

todisk=[]
for fop,foppass in zip(falloffs,falloffs_valid):
	todisk.append([fop,foppass])
with open('spotfinder_results.pickle','w') as thefile:
	pickle.dump(todisk, thefile)
