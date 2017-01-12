#!/usr/bin/env python
import image,numpy as np,rtplan,auger,plot,argparse
from collections import Counter
from tableio import write
import argparse

parser = argparse.ArgumentParser(description='launch multiple params.')
parser.add_argument('--plotspot')
args = parser.parse_args()

################################################################################

rtplan = rtplan.rtplan(['data/plan.txt'],norm2nprim=False)#,noproc=True)
MSW=[]
for spot in rtplan.spots:
	if spot[0] == 102:#
		MSW.append(spot)

images = [image.image('output/new_dosespotid-ct.mhd'),
		  image.image('output/new_dosespotid-rpct.mhd'),
		  image.image('output/new-source-ct.mhd'),
		  image.image('output/new-source-rpct.mhd')]

images = [im.imdata.reshape(im.imdata.shape[::-1]).squeeze() for im in images] #squeeze to remove dims with len()==1

xhist = np.linspace(-150,150,301) #1mm voxels, endpoints
x = np.linspace(-148,148,300) #bincenters

shifts = []
pgshifts = []

for spindex, (ct,rpct,pg,rppg) in enumerate( zip( *images ) ):
	#if args.plotspot:
		#shift = auger.get_fop(x,ctspot) - auger.get_fop(x,rpctspot)
	
	#if args.shifttolerance:
		## ensure a shift calculated at 20% and 80% height within 1mm of shift computed at default 50%
		#shift2 = auger.get_fop(x,rpctspotx,threshold=0.2) - auger.get_fop(x,ctspotx,threshold=0.2)
		#shift8 = auger.get_fop(x,rpctspotx,threshold=0.8) - auger.get_fop(x,ctspotx,threshold=0.8)
		
		#if np.isclose([shift2,shift8],shift,atol=float(args.shifttolerance)).all():
			## all values in *ctfops are within 1.0 (mm) of *ctfop. it is a front shift
			#shifts.append(shift)
		#else:
			#shifts.append(np.nan)
	#else:
		#shifts.append(shift)
		
	if args.plotspot is not None and spindex == int(args.plotspot):
		#spotimages = [im.flatten() for im in spotimages] #flatten, because theres no other axes anyway
		#ct = spotimages[0]
		#print len(ct)
		#rpct = spotimages[1]
		#pg = spotimages[2]
		#rppg = spotimages[3]
		
		shift = auger.get_fop(x,ct) - auger.get_fop(x,rpct)
		pgshift = auger.get_fop(x,pg) - auger.get_fop(x,rppg)
		
		f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
		ax1.step(x,ct, color='steelblue',lw=1., label='')
		ax1.step(x,rpct, color='indianred',lw=1., label='')
		ax1.set_xlabel('FOP [mm]')
		ax1.set_ylabel('Integrated Dose [a.u.]')
		ax1.set_title('Integrated Dose Profile (along x)'+', shift '+str(shift)[:4], fontsize=8)
		
		ax2.step(x,pg, color='steelblue',lw=1., label='')
		ax2.step(x,rppg, color='indianred',lw=1., label='')
		ax2.set_xlabel('FOP [mm]')
		ax2.set_ylabel('Integrated Dose [a.u.]')
		ax2.set_title('Integrated PG Profile (along x)'+', shift '+str(pgshift)[:4], fontsize=8)
		
		f.suptitle('spotid '+str(spindex)+', weight '+plot.sn(MSW[spindex][-1]), fontsize=8)
		plot.texax(ax1)
		plot.texax(ax2)
		f.savefig('new-fop'+str(args.plotspot)+'.pdf', bbox_inches='tight')
		plot.close('all')
