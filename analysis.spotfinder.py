#!/usr/bin/env python
import image,sys,numpy as np
from collections import Counter

infile = sys.argv[-1] #in goes mhd
outpostfix = ".3d"
crush = [0,0,0,1]

print >> sys.stderr, 'Processing', infile

spotim = image.image("dosespotid.mhd")
layim = image.image("doselayerid.mhd")
mask = "mask/absdiff.dose.fullplan.10000.skinmask.masked.mhd" #0.6Grey cutoff

spotim3d = spotim.save_crush_argmax(outpostfix, crush)
spotim3d = image.image(spotim3d)
spotim3dmsk = spotim3d#.applymask_clitk("msk",mask)

layim3d = layim.save_crush_argmax(outpostfix, crush)
layim3d = image.image(layim3d)
layim3dmsk = layim3d#.applymask_clitk("msk",mask)#clitk convert everything to float, so must cast back to int later

spt_hist = dict(Counter(spotim3dmsk.imdata.flatten().tolist()))
lay_hist = dict(Counter(layim3dmsk.imdata.flatten().tolist()))

print np.count_nonzero(spotim3dmsk.imdata)
print np.count_nonzero(layim3dmsk.imdata)
print len(spt_hist)
print len(lay_hist)

#outpostfix = ".2dfront"
#crush = [1,0,0]
#img = image.image(im3d)
#img.save_crush_argmax(outpostfix, crush)

#outpostfix = ".2dside"
#crush = [0,0,1]
#img = image.image(im3d)
#img.save_crush_argmax(outpostfix, crush)
