#!/usr/bin/env python
import image,numpy as np,rtplan,pickle,plot
from collections import Counter
from operator import add

doseimage = 'output/new_dosespotid-ct.mhd'

rtpfile = 'data/plan.txt'
rtplan1 = rtplan.rtplan([rtpfile],norm2nprim=False)#,noproc=True)
field = 2

fopandpass = pickle.load(open('spotfinder_results.pickle'))
falloffs = [x[0] for x in fopandpass]
falloffs_valid = [x[1] for x in fopandpass]
falloffs_pass = [x[0] for x in fopandpass if x[1] is True]

MSW=[]
for spot in rtplan1.spots:
	if spot[0] == 100+field:#
		MSW.append(spot)

print len(fopandpass)-len(falloffs_pass), 'spots discarded.'

################################################################################

#diff size for plot
geo_xhist = np.linspace(-150,150,76) #4mm voxels, endpoints
geo_x = np.linspace(-148,148,75) #bincenters

#bin spots and get spotcount.
indices = np.digitize(falloffs_pass,geo_x)
ind_counter = Counter(indices)
# falloffs and geo_x[indices] are identical. Comprende?
y,bins=np.histogram(falloffs_pass,geo_xhist)
#y,bins=np.histogram(geo_x[indices],geo_xhist)

y_msw = []
for ind,x_val in enumerate(geo_x):
	binmsw = 0.
	if ind_counter[ind] > 0:
		print x_val,',', ind_counter[ind],',', 
		for spotind,i in enumerate(indices):
			if ind == i:
				binmsw += MSW[spotind][-1]
				#print spotind#,':',MSW[spotind][-1],',',
				#print MSW[spotind]
		#if newMSW > 0:
			#print plot.sn(newMSW/ind_counter[ind]),
			#print plot.sn(newMSW),
		#print ''
	y_msw.append(binmsw)


#print y_msw

im = image.image(doseimage)
ct = im.imdata.reshape(im.imdata.shape[::-1]).squeeze()
ct1d=np.add.reduce(ct)
ct_xhist = np.linspace(-150,150,301) #2mm voxels, endpoints
ct_x = np.linspace(-149.5,149.5,300) #bincenters


f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
geo_spot, = ax1.step(geo_x,y, color='indianred',lw=1., label='Spot count', where='mid')
dose, = ax1.step(ct_x,ct1d/ct1d.max()*float(y.max()), color='steelblue',lw=1., label='Integral dose (scaled)', where='mid')
ax1.set_xlabel('Position [mm]')
ax1.set_ylabel('Number of spots')
ax1.set_xlim(-60,16)
ax1.set_ylim(0,110)
plot.texax(ax1)

ax2=ax1.twinx()
ax2.semilogy()
geo_prot, = ax2.step(geo_x,y_msw, color='forestgreen',lw=1., label='Protons', where='mid')
ax2.set_xlim(-58,18)
ax2.set_ylim(5e7,5e9)
ax2.set_ylabel('Number of Protons')
plot.texax(ax2,'twinx')

#ax1.axvline(falloffs[61],color='green') #plot FOP of spot 61

f.legend([geo_spot,dose,geo_prot],['Spot count','Dose (scaled)','Proton count'],frameon = False)#,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'upper right')

f.savefig('rtplan.geolayers.pdf', bbox_inches='tight')
plot.close('all')

################################################################################

#SPOTID_GROUPAROUND = 61
#SPOTID_GROUPAROUND = 40
SPOTID_GROUPAROUND = 29

print 'energy 61',MSW[61]
print 'energy 40',MSW[40]
print 'energy 29',MSW[29]

elay2 = [x for x in rtplan1.layers if x[0]==102]
E61 = MSW[SPOTID_GROUPAROUND][1]
elay2_upto61 = [x for x in elay2 if x[1] == E61]
lay61_prots = elay2_upto61[0][2]
print lay61_prots

#print elay2

fop61=falloffs[SPOTID_GROUPAROUND]
geo_spot_list = [SPOTID_GROUPAROUND]
new_spot_prot_sum = MSW[SPOTID_GROUPAROUND][4]
print new_spot_prot_sum

limit = 9

for spindex,(plan,foppass) in enumerate(zip(MSW,fopandpass)):
	if spindex == SPOTID_GROUPAROUND: #already added
		continue
	if foppass[1] == True:
		if abs(foppass[0] - fop61) <= limit :#and abs(plan[2] - MSW[61][2]) <= limit and abs(plan[3] - MSW[61][3]) <= limit:
			#print plan
			new_spot_prot_sum+=plan[4]
			#print new_spot_prot_sum
			geo_spot_list.append(spindex)
			if new_spot_prot_sum > lay61_prots:
				break

print geo_spot_list,new_spot_prot_sum
print MSW[SPOTID_GROUPAROUND]
#print MSW[21]

print '================================='
sameelaycount = 0
for spind in geo_spot_list:
	if MSW[spind][1] == MSW[SPOTID_GROUPAROUND][1]:
		sameelaycount += 1
print sameelaycount / float(len(geo_spot_list))
print '================================='

################################################################################

ct61_geo = [0]*len(ct[0])

for spindex in geo_spot_list:
	ct61_geo = map(add, ct61_geo, ct[spindex])

#for spindex,(dosespot,spotid) in enumerate(zip(ct,MSW)):
	#if spotid[1]==E61: #in the right elayer
		#e_spot_list.append(spindex)
		#ct61_geo = map(add, ct61_geo, dosespot)

ct61_elay = [0]*len(ct[0])
e_spot_list = []
for spindex,(dosespot,spotid) in enumerate(zip(ct,MSW)):
	if spotid[1]==E61: #in the right elayer
		e_spot_list.append(spindex)
		ct61_elay = map(add, ct61_elay, dosespot)

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
ax1.step(ct_x,ct61_geo/max(ct61_geo), color='indianred',lw=1., label='Geometric layer '+plot.sn(new_spot_prot_sum)+' protons', where='mid')
ax1.step(ct_x,ct61_elay/max(ct61_elay), color='steelblue',lw=1., label='Energy Layer'+plot.sn(lay61_prots)+' protons', where='mid')
ax1.set_xlabel('Position [mm]')
ax1.set_ylabel('Number of spots')
#ax1.set_xlim(-60,16)
#ax1.set_ylim(0,110)
plot.texax(ax1)

ax1.legend(frameon = False,loc = 'upper right')#,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'upper right')

f.savefig('rtplan.geogroup.pdf', bbox_inches='tight')
plot.close('all')

print 'geoplan protcount',new_spot_prot_sum
print 'eplan protcount',lay61_prots
rtplan.rtplan([rtpfile],noproc=True,spotlist=e_spot_list,fieldind=field,relayername='elayspot'+str(SPOTID_GROUPAROUND))
rtplan.rtplan([rtpfile],noproc=True,spotlist=geo_spot_list,fieldind=field,relayername='geolayspot'+str(SPOTID_GROUPAROUND))

