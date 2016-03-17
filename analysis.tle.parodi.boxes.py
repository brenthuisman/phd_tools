#!/usr/bin/env python
import sys,copy,image,tle,plot,numpy as np,matplotlib.pyplot as plt,matplotlib as mpl

print >> sys.stderr, 'Processing'

### params
ppsan = (211.926+211.511)/2
ppstle = (199.421+200.71)/2
yn = 'mean3d.mhd' #yieldname
vn = 'var3d.mhd' #varname
yn4d = 'mean4d.mhd' #yieldname
vn4d = 'var4d.mhd' #varname

### tledata
tleprims = [1e3,1e4,1e5,1e6]
# tledirs = ['run.wzd0','run.Ex3U','run.NSYS','tle1M']
tledirs = ['tle1k','tle10k','tle100k','tle1M']

### analog
anprims = [1e6,1e7,1e8,1e9]
andirs = ['analog1M','analog10M','analog100M','analog1B']

### helpers, masks
mask90pc = image.image("analog1B/mean3d.mhd")
mask90pc.to90pcmask()
#mask90pc.save90pcmask()
maskbeam = image.image("mask-beamline/maskfile.mhd")
maskspect = image.image("mask-spect1-8/finalmask.mhd")
maskbox2 = image.image("mask-box2/phantom_Parodi_TNS_2005_52_3_modified.maskfile2.mhd")
maskbox8 = image.image("mask-box8/phantom_Parodi_TNS_2005_52_3_modified.maskfile8.mhd")
#worstcaseim = image.image("analog1B/var.mhd",pps=ppsanalog,nprim=1e9,type='var')

### init
tle4dbox2 = tle.load_tledata(tledirs,tleprims,[mask90pc,maskspect,maskbox2],ppstle,yn4d,vn4d)
an4dbox2 = tle.load_tledata(andirs,anprims,[mask90pc,maskspect,maskbox2],ppsan,yn4d,vn4d)
tle4dbox8 = tle.load_tledata(tledirs,tleprims,[mask90pc,maskspect,maskbox8],ppstle,yn4d,vn4d)
an4dbox8 = tle.load_tledata(andirs,anprims,[mask90pc,maskspect,maskbox8],ppsan,yn4d,vn4d)

tlebox2 = tle.load_tledata(tledirs,tleprims,[mask90pc,maskbox2],ppstle,yn,vn)
anbox2 = tle.load_tledata(andirs,anprims,[mask90pc,maskbox2],ppsan,yn,vn)
tlebox8 = tle.load_tledata(tledirs,tleprims,[mask90pc,maskbox8],ppstle,yn,vn)
anbox8 = tle.load_tledata(andirs,anprims,[mask90pc,maskbox8],ppsan,yn,vn)


### Eff histos
tle.seteff(tlebox2)
tle.seteff(anbox2)
tle.seteff(tlebox8)
tle.seteff(anbox8)

tle.seteffratio(tlebox2,anbox2[max(anbox2.keys())]['var'])
tle.seteffratio(tlebox8,anbox8[max(anbox8.keys())]['var'])

f, ((tl,tr)) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=False)

a=tle.get_effhist(tl,tlebox2[1e3]['var'])
b=tle.get_effhist(tl,tlebox2[1e4]['var'])
c=tle.get_effhist(tl,tlebox2[1e5]['var'])
d=tle.get_effhist(tl,tlebox2[1e6]['var'])
# print [a[1],b[1],c[1],d[1]]
lmed2 = np.average([a[1],b[1],c[1],d[1]])
tl.set_title("Medium 2 (Bone)")
tl.text(0.05, 0.9,"Median gain: "+plot.sn(lmed2), ha='left', va='center', transform=tl.transAxes, fontsize=6)
a=tle.get_effhist(tr,tlebox8[1e3]['var'])
b=tle.get_effhist(tr,tlebox8[1e4]['var'])
c=tle.get_effhist(tr,tlebox8[1e5]['var'])
d=tle.get_effhist(tr,tlebox8[1e6]['var'])
# print [a[1],b[1],c[1],d[1]]
lmed8 = np.average([a[1],b[1],c[1],d[1]])
tr.set_title("Medium 8 (Muscle)")
tr.text(0.05, 0.9,"Median gain: "+plot.sn(lmed8), ha='left', va='center', transform=tr.transAxes, fontsize=6)

f.savefig('boxes-eff.pdf', bbox_inches='tight')
plt.close('all')


### Reldiff of two boxes.
tle_2 = tle4dbox2 #no deepcopy of 4D images
tle_8 = tle4dbox8
an_2 = an4dbox2
an_8 = an4dbox8
tle.setprojectiondata(tle_2,an_2[max(an_2.keys())])
tle.setprojectiondata(tle_8,an_8[max(an_8.keys())])

f, (ll,lr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
tl = ll.twinx()
tr = lr.twinx()

tle.get_relunc(tl,tle_2,an_2[max(an_2.keys())],'E')
tle.get_relunc(tr,tle_8,an_8[max(an_8.keys())],'E')
tle.get_yield(ll,tle_2,an_2[max(an_2.keys())],'E')
tle.get_yield(lr,tle_8,an_8[max(an_8.keys())],'E')

#tl.set_ylim([1,5e2])
#tr.set_ylim([1,5e2])

ll.yaxis.set_label_position("right")
lr.yaxis.set_label_position("right")
tl.yaxis.set_label_position("left")
tr.yaxis.set_label_position("left")

tl.set_title("Medium 2 (Bone)\nMedian gain: "+plot.sn(lmed2))
tr.set_title("Medium 8 (Muscle)\nMedian gain: "+plot.sn(lmed8))
tl.set_ylim([6e-3,1.2])
tr.set_ylim([6e-3,1.2])
# tl.set_ylim([1e-2,5])
# tr.set_ylim([1e-2,5])

ll.yaxis.set_visible(False)
lr.yaxis.set_visible(False)
# tr.yaxis.set_visible(False)

tr.plot([0],[0],color='#cccccc',linewidth=0,label='Yield (not to scale)')
for child in ll.get_children() + lr.get_children():
	if isinstance(child, mpl.lines.Line2D) or isinstance(child, mpl.collections.PolyCollection):
		child.set_color('#cccccc')

tl.set_ylabel('Relative Uncertainty [\%]')
ll.set_xlabel('PG energy [MeV]')
ll.xaxis.set_label_coords(1.1,-0.1)

lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.savefig('relunc-boxes.pdf', bbox_inches='tight')
plt.close('all')
