#!/usr/bin/env python
import image,numpy as np,rtplan,auger,plot,argparse
from collections import Counter
from tableio import write
import argparse

parser = argparse.ArgumentParser(description='launch multiple params.')
parser.add_argument('--plotspot')
parser.add_argument('--printbin')
parser.add_argument('--dosepg')
parser.add_argument('--shifttolerance')
args = parser.parse_args()


if args.dosepg:
	#spotim_ct = image.image('output/source-ct-'+str(int(args.dosepg))+'.mhd')
	#spotim_rpct = image.image('output/source-rpct-'+str(int(args.dosepg))+'.mhd')
	spotim_ct = image.image('source-139.mhd')
	spotim_rpct = image.image('source-144.mhd')
	#spotim_ct = image.image("output/source-ct-61.mhd")
	#spotim_ct = image.image("output/dosedist-ct-61-Dose.mhd")
	spotim_ct.toprojection(".x", [0,1,1,1])
	#spotim_rpct = image.image("output/source-rpct-61.mhd")
	#spotim_rpct = image.image("output/dosedist-rpct-61-Dose.mhd")
	spotim_rpct.toprojection(".x", [0,1,1,1])
	xhist = np.linspace(-150,150,151) #4mm voxels, endpoints
	x = np.linspace(-148,148,150) #bincenters
	spot = spotim_ct.imdata
	spot2 = spotim_rpct.imdata
	ctfo=auger.get_fop(x,spot)
	rpctfo=auger.get_fop(x,spot2)

	# '####################'

	print ctfo,rpctfo
	print '####################'
	print rpctfo-ctfo

	f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

	ax1.step(x,spot, color='steelblue',lw=1., label='CT FOP: '+str(ctfo))
	ax1.step(x,spot2, color='indianred',lw=1., label='RPCT FOP: '+str(rpctfo))

	ax1.set_xlabel('FOP [mm], shift: '+str(rpctfo-ctfo) )
	#ax1.set_ylabel('Number of spots')
	#ax1.set_xlim(-60,25)
	#ax1.set_ylim(0,140)

	ax1.legend(frameon = False)
	plot.texax(ax1)

	f.savefig('fop-pg'+str(int(args.dosepg))+'.pdf', bbox_inches='tight')
	plot.close('all')
	quit()

################################################################################

rtplan = rtplan.rtplan(['data/plan.txt'],norm2nprim=False)#,noproc=True)
MSW=[]
for spot in rtplan.spots:
	if spot[0] == 102:#
		MSW.append(spot)

spotim_ct = image.image("results.vF3d/dosespotid.2gy.mhd")
spotim_rpct = image.image("results.7Dee/dosespotid.2gy.mhd")

ct = spotim_ct.imdata.reshape(spotim_ct.imdata.shape[::-1])
rpct = spotim_rpct.imdata.reshape(spotim_rpct.imdata.shape[::-1])

xhist = np.linspace(-150,150,76) #4mm voxels, endpoints
x = np.linspace(-148,148,75) #bincenters

shifts = []
for spindex, (ctspot,rpctspot) in enumerate(zip(ct,rpct)):
	crush = [0,1,1] #x
	crush=crush[::-1]
	ax = [i for (i,j) in zip(range(len(crush)),crush) if j==1]
	
	ctspotx = np.add.reduce(ctspot, axis=tuple(ax))
	rpctspotx = np.add.reduce(rpctspot, axis=tuple(ax))
	#ctspotx = ctspotx.reshape(ctspotx.shape[::-1]) #geen effect op 1D prof. wut?
	#rpctspotx = rpctspotx.reshape(rpctspotx.shape[::-1])
	
	shift = auger.get_fop(x,rpctspotx) - auger.get_fop(x,ctspotx)
	
	if args.shifttolerance:
		# ensure a shift calculated at 20% and 80% height within 1mm of shift computed at default 50%
		shift2 = auger.get_fop(x,rpctspotx,threshold=0.2) - auger.get_fop(x,ctspotx,threshold=0.2)
		shift8 = auger.get_fop(x,rpctspotx,threshold=0.8) - auger.get_fop(x,ctspotx,threshold=0.8)
		
		if np.isclose([shift2,shift8],shift,atol=float(args.shifttolerance)).all():
			# all values in *ctfops are within 1.0 (mm) of *ctfop. it is a front shift
			shifts.append(shift)
		else:
			shifts.append(np.nan)
	else:
		shifts.append(shift)
	
	if args.plotspot is not None and spindex == int(args.plotspot):
		#2dtop crush
		crush = [0,1,0]
		crush=crush[::-1]
		ax = [i for (i,j) in zip(range(len(crush)),crush) if j==1]
		
		rpctspot2d = np.add.reduce(rpctspot, axis=tuple(ax))
		#rpctspot2d = rpctspot2d.reshape(rpctspot2d.shape[::-1])
		ctspot2d = np.add.reduce(ctspot, axis=tuple(ax))
		#ctspot2d = ctspot2d.reshape(ctspot2d.shape[::-1])
		
		f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
		ax1.step(x,ctspotx, color='steelblue',lw=1., label='')
		ax1.step(x,rpctspotx, color='indianred',lw=1., label='')
		ax1.set_xlabel('FOP [mm]')
		ax1.set_ylabel('Integrated Dose [a.u.]')
		ax1.set_title('Integrated Dose Profile (along x)', fontsize=8)
		ax2.imshow(rpctspot2d-ctspot2d,cmap = plot.get_cmap('gray'))
		ax2.set_xlabel('x [mm]')
		ax2.set_ylabel('z [mm]')
		ax2.set_title('Integrated Dose Diff (top-view)', fontsize=8)
		f.suptitle('spotid '+str(spindex)+', weight '+plot.sn(MSW[spindex][-1])+', shift '+str(shift)[:4], fontsize=8)
		plot.texax(ax1)
		plot.texax(ax2)
		f.savefig('fop'+str(args.plotspot)+'.pdf', bbox_inches='tight')
		plot.close('all')
		

if args.printbin is not None:
	for spotn,shift in enumerate(shifts):
		if float(args.printbin)-0.5 < shift < float(args.printbin)+0.5:
			print spotn, shift

#get rid of nans, order is no longer spotid
shifts = np.array(shifts)
shifts = shifts[~np.isnan(shifts)]

xhist = np.linspace(-150,150,301) #4mm voxels, endpoints
x = np.linspace(-148,148,300) #bincenters, mm bins
indices = np.digitize(shifts,x)
ind_counter = Counter(indices)
y,bins=np.histogram(shifts,xhist)
#y,bins=np.histogram(x[indices],xhist)

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
ax1.step(x,y, color='indianred',lw=1., label='Geometric layers')
ax1.set_xlabel('FOP shift [mm]')
ax1.set_ylabel('Number of spots')
ax1.set_xlim(-5,32)

plot.texax(ax1)

f.savefig('fopdiffs.pdf', bbox_inches='tight')
plot.close('all')
