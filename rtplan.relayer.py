#!/usr/bin/env python
import image,numpy as np,rtplan,auger,argparse
from collections import Counter
from tableio import write

parser = argparse.ArgumentParser(description='RTPlanstructure relayerer. It takes an input rtplan, and input dose per-spot image and outputs new rtplans, each with only the spots that have their fall-off in a certain depth-bin.')
parser.add_argument("-rt", "--rtplan", type=str, help="input rtplan (dumped by Gate)")
parser.add_argument("-di", "--doseimage", type=str, help="mhd image with dose per spot (4D)")
parser.add_argument("-f", "--field", type=int, default=102, help="limit rtplan parsing to this field.")
args = parser.parse_args()

rtplan = rtplan.rtplan([args.rt],norm2nprim=False)
MSW=[]
for spot in rtplan.spots:
	if spot[0] == 102:#
		MSW.append(spot)

spotim_ct = image.image("results.vF3d/dosespotid.2gy.mhd")
spotim_ct3d = image.image("results.vF3d/dosespotid.3d.2gy.mhd")
spotim_ct3d.to90pcmask
spotim_ct3d.toprojection(".x", [0,1,1,1])

new_procedure = True

################################################################################

if new_procedure == False:
	#layim = image.image("doselayerid.mhd")
	#mask = image.image("mask/absdiff.dose.fullplan.10000.skinmask.mhd")
	outpostfix = ".3d"
	crush = [0,0,0,1]

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
		print spotid, newspots[int(spotid)] #klopt!

	#print rtplan.ConvertMuToProtons(1,140) #about 10^8
	#print rtplan.ConvertMuToProtons(0.1,140) #about 10^7
	#print rtplan.ConvertMuToProtons(0.01,140) #about 10^6

	#find spot of 1e8,1e7,1e6
	for spotid,spot in enumerate(newspots):
		if 0.95e6 < spot[-1] < 1.20e6:
			print '1e6', spotid, spot
		if 0.98e7 < spot[-1] < 1.02e7:
			print '1e7', spotid, spot
		if 0.98e8 < spot[-1] < 1.02e8:
			print '1e8', spotid, spot

################################################################################

ct = spotim_ct.imdata.reshape(spotim_ct.imdata.shape[::-1])

xhist = np.linspace(-150,150,76) #4mm voxels, endpoints
x = np.linspace(-148,148,75) #bincenters
#print x[0],x[1],x[-1],len(x)
#print xhist[0],xhist[1],xhist[-1],len(xhist)

falloffs = []

#f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
for spindex,spot in enumerate(ct):
	#from __crush
	#print spot.shape
	crush = [0,1,1] #x
	
	crush=crush[::-1]
	#spot = spot.reshape(spot.shape[::-1])
	
	ax = [i for (i,j) in zip(range(len(crush)),crush) if j==1]
	spot = np.add.reduce(spot, axis=tuple(ax))

	spot = spot.reshape(spot.shape[::-1])
	#print spot.shape
	#print spot
	
	fo=auger.ipnl_fit_range(x,spot)
	falloffs.append(fo)
	
	#if spindex in [4, 7, 10, 32, 43]:
		##print spot
		#ax1.step( x ,spot, color='moccasin')
		
		#ax1.axvline(fo,color='green',alpha=0.5)
		#print len(newspots)
		#print newspots[spindex]

#f.savefig('dose-ranges.pdf', bbox_inches='tight')
#plot.close('all')

################################################################################


indices = np.digitize(falloffs,x)
ind_counter = Counter(indices)
# falloffs and x[indices] are identical. Comprende?

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
#y,bins=np.histogram(falloffs,xhist)
y,bins=np.histogram(x[indices],xhist)
ax1.step(x,y, color='indianred',lw=1., label='Spot counts')
ax1.step(x,spotim_ct3d.imdata/spotim_ct3d.imdata.max()*float(y.max()), color='steelblue',lw=1., label='Dose (normalized)')
ax1.set_xlabel('Depth [mm]')
ax1.set_ylabel('Counts')
plot.legend(frameon = False)#,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'upper right')

plot.texax(ax1)
f.savefig('dose-ranges.pdf', bbox_inches='tight')
plot.close('all')

################################################################################

for ind,x_val in enumerate(x):
	if ind_counter[ind] > 0:
		print x_val,',', ind_counter[ind],',', 
		newMSW = 0.
		for spotind,i in enumerate(indices):
			if ind == i:
				newMSW += MSW[spotind][-1]
				print spotind,#':',MSW[spotind][-1],',',
		#if newMSW > 0:
			#print plot.sn(newMSW/ind_counter[ind]),
			#print plot.sn(newMSW),
		print ''
