#!/usr/bin/env python
import image,sys,numpy as np,rtplan
from collections import Counter
from tableio import write

rtplan = rtplan.rtplan('../../data/plan.txt',MSW_to_protons=False)
newspots=[]
for spot in rtplan.spots:
	if spot[0] == 2:
		newspots.append(spot)
#write(newspots,'spots.txt')

outpostfix = ".3d"
crush = [0,0,0,1]

spotim = image.image("dosespotid.mhd")
layim = image.image("doselayerid.mhd")
layim = image.image("doselayerid.mhd")
mask = image.image("mask/absdiff.dose.fullplan.10000.skinmask.mhd")
mask.tomask_atthreshold(0.7) # cutoff in grey

print np.count_nonzero(mask.imdata)
mask.insert_block('x','-',100-35) #remove a noisy area not contributing to a few-mm shift
print np.count_nonzero(mask.imdata)
maskfname = mask.saveas('.thres.x')

spotim3d = spotim.save_crush_argmax(outpostfix, crush)
spotim3d = image.image(spotim3d)
spotim3dmsk = spotim3d.applymask_clitk("msk",maskfname)

layim3d = layim.save_crush_argmax(outpostfix, crush)
layim3d = image.image(layim3d)
layim3dmsk = layim3d.applymask_clitk("msk",maskfname)#clitk convert everything to float, so must cast back to int later

spt_hist = dict(Counter(spotim3dmsk.imdata.flatten().tolist()))
lay_hist = dict(Counter(layim3dmsk.imdata.flatten().tolist()))#.most_common(5)

print np.count_nonzero(spotim3dmsk.imdata)
print np.count_nonzero(layim3dmsk.imdata)
print spt_hist#.keys()
print lay_hist#.keys()

for spotid in spt_hist.keys():
	if spotid == 0.:
		continue
	print newspots[int(spotid)] #klopt!
