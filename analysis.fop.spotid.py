#!/usr/bin/env python
import image,numpy as np,rtplan,auger,plot,argparse
#from collections import Counter
#from tableio import write

parser = argparse.ArgumentParser(description='launch multiple params.')
parser.add_argument('--plotspot')
parser.add_argument('--ctonly', action='store_true')
parser.add_argument('--tolerance')
args = parser.parse_args()
volume_offset=-142.097+7.96
#-142.097 komt uit mhd header source images, en is centrum van eerste voxel (bin).
#Dit is in MHD coords systeem, en dat verschilt van het met isocenter
#NOOT: offset in spotid images is ANDERS dan in overige simulaties (voxels in x direction zijn 1mm, elders 2mm (met MHD offset -141.597)
#NOOT2: in dit geval is pgsource_offset ook geldig voor dosespotid image, immers zelfde subvolume

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

x = np.linspace(-149.5,149.5,300) #bincenters
xhist = np.linspace(-150,150,301) #1mm voxels, endpoints
x = x+(volume_offset-x[0])   #offset for pg source image
xhist = xhist+(volume_offset-xhist[0]) #same

shifts = []
pgshifts = []
diffshifts = []

for spindex, (ct,rpct,pg,rppg) in enumerate( zip( *images ) ):
	if args.plotspot is not None and spindex != int(args.plotspot):
		continue
	
	shift = auger.get_fop(x,rpct) - auger.get_fop(x,ct)
	pgshift = auger.get_fop(x,rppg) - auger.get_fop(x,pg)
	diffshift = pgshift-shift
	
	if args.tolerance:
		# ensure that distance from 50%fop to 20%fop and 80%fop are similar to within $tolerance mm, AT CT DOSE IMAGE ONLY
		# this way slope does not matter, and because computed at CT only its clinically usable.
		fop20 = auger.get_fop(x,ct,threshold=0.2)
		fop50 = auger.get_fop(x,ct,threshold=0.5)
		fop80 = auger.get_fop(x,ct,threshold=0.8)
		diff20 = abs(fop50-fop20)
		diff80 = abs(fop80-fop50)
		
		if abs(diff80-diff20) < args.tolerance:
			# both conditions met
			shifts.append(shift)
			pgshifts.append(pgshift)
			diffshifts.append(diffshift)
		else:
			shifts.append(np.nan)
			pgshifts.append(np.nan)
			diffshifts.append(np.nan)
	else:
		shifts.append(shift)
		pgshifts.append(pgshift)
		diffshifts.append(diffshift)
		
	if args.plotspot is not None and spindex == int(args.plotspot):
		
		if args.ctonly:
			f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
			ax1.step(x,ct/ct.max(), color='steelblue',lw=1., label='Dose,\nFOP: '+str(auger.get_fop(x,ct))[:4]+' mm')
			ax1.step(x,pg/pg.max(), color='indianred',lw=1., label='PG production,\nFOP: '+str(auger.get_fop(x,pg))[:4]+' mm')
			ax1.set_xlabel('Position w.r.t. isocenter [mm]')
			ax1.set_ylabel('Dose/PG production, rescaled [a.u.]')
			ax1.legend(frameon = False)
			ax1.set_xlim(-75,75)
			f.suptitle('Spotid '+str(spindex)+', '+plot.sn(MSW[spindex][-1])+' protons', fontsize=8)
			plot.texax(ax1)
			f.savefig('CT-dose-pg-'+str(args.plotspot)+'.pdf', bbox_inches='tight')
			plot.close('all')
			quit()
		else:
			f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
			ax1.step(x,ct, color='steelblue',lw=1., label='FOP: '+str(auger.get_fop(x,ct))[:5])
			ax1.step(x,rpct, color='indianred',lw=1., label='FOP: '+str(auger.get_fop(x,rpct))[:5])
			ax1.set_xlabel('FOP [mm]')
			ax1.set_ylabel('Integrated Dose [a.u.]')
			ax1.set_title('Integrated Dose Profile (along x)'+', shift '+str(shift)[:4], fontsize=8)
			ax1.legend(prop={'size':6},loc='best',frameon = False)
			
			#from scipy.ndimage.filters import gaussian_filter

			ax2.step(x,pg, color='steelblue',lw=1., label='FOP: '+str(auger.get_fop(x,pg))[:5])
			ax2.step(x,rppg, color='indianred',lw=1., label='FOP: '+str(auger.get_fop(x,rppg))[:5])
			#ax2.step(x,gaussian_filter(pg, sigma=15), color='blue',lw=1., label='FOP: '+str(auger.get_fop(x,gaussian_filter(pg, sigma=10)))[:5])
			#ax2.step(x,gaussian_filter(rppg, sigma=15), color='red',lw=1., label='FOP: '+str(auger.get_fop(x,gaussian_filter(rppg, sigma=10)))[:5])
			ax2.set_xlabel('FOP [mm]')
			ax2.set_ylabel('Integrated Dose [a.u.]')
			ax2.set_title('Integrated PG Profile (along x)'+', shift '+str(pgshift)[:4], fontsize=8)
			ax2.legend(prop={'size':6},loc='best',frameon = False)
			
			ax1.set_xlim(-75,75)
			ax2.set_xlim(-75,75)
			
			f.suptitle('spotid '+str(spindex)+', weight '+plot.sn(MSW[spindex][-1]), fontsize=8)
			plot.texax(ax1)
			plot.texax(ax2)
			f.savefig('fop_v5-'+str(args.plotspot)+'.pdf', bbox_inches='tight')
			plot.close('all')
			quit()
	
	print 'Spot', spindex, 'analyzed!'


#get rid of nans, order is no longer spotid
suppressed = np.isnan(shifts).sum() #should be same in all arrays.

shifts = np.array(shifts)
diffshifts = np.array(diffshifts)
pgshifts = np.array(pgshifts)
shifts = shifts[~np.isnan(shifts)]
pgshifts = pgshifts[~np.isnan(pgshifts)]
diffshifts = diffshifts[~np.isnan(diffshifts)]

#xhist = np.linspace(-150,150,301) #1mm voxels, endpoints
#x = np.linspace(-149.5,149.5,300) #bincenters, mm bins

#indices = np.digitize(shifts,x)
y,bins=np.histogram(shifts,xhist)
#y,bins=np.histogram(x[indices],xhist)
pgy,pgbins=np.histogram(pgshifts,xhist)
diffy,diffbins=np.histogram(diffshifts,xhist)

f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
ax1.step(x,y, color='steelblue',lw=1., label='Dose Shifts')
ax1.step(x,pgy, color='indianred',lw=1., label='PG Shifts')
ax1.set_xlabel('FOP shift [mm]')
ax1.set_ylabel('Number of spots')
#ax1.set_xlim(-5,32)

ax2.step(x,diffy, color='forestgreen',lw=1., label='Diff in shift\n$\mu='+str(np.mean(diffshifts))[:5]+'$\n$\sigma='+str(np.std(diffshifts))[:4]+'$')
ax2.set_xlabel('PG-Dose shift [mm]')
ax2.set_ylabel('Number of spots')
#ax2.set_xlim(-25,25)

plot.texax(ax1)
plot.texax(ax2)
ax1.legend(frameon = False)
ax2.legend(frameon = False)

f.suptitle('Nr. of spots: '+str(len(shifts))+'{d}'.format(d=', with '+str(args.tolerance)+' mm tolerance' if args.tolerance is not None else '.'), fontsize=8)
f.savefig('shift-diffs-v3-'+str(args.tolerance)+'.pdf', bbox_inches='tight')
plot.close('all')
