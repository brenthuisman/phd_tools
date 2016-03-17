#!/usr/bin/env python
import sys,subprocess,image,tle,plot,numpy as np,matplotlib.pyplot as plt,matplotlib as mpl

print >> sys.stderr, 'Processing'

### params
ppsan1 = (72.0856+71.8095)/2
ppstle1 = (69.2312+67.7542)/2
ppsan2 = (72.2114+71.9978)/2
ppstle2 = (68.1091+69.5367)/2
ppsan5 = (72.2351+74.2769)/2
ppstle5 = (68.3652+69.5583)/2
# yn = 'mean3d.mhd' #yieldname
# vn = 'var3d.mhd' #varname
yn4d = 'mean4d.mhd' #yieldname
vn4d = 'var4d.mhd' #varname

### helpers, masks
# TODO make mask90pc for 1,5mm voxels
maskspect1 = image.image("vox/1mm1-8msk.mhd")
maskspect2 = image.image("mask-spect1-8/finalmask.mhd")
maskspect5 = image.image("vox/5mm1-8msk.mhd")
mask901 = image.image("vox/90pcmask1.mhd")
mask902 = image.image("analog1B/mean.90pcmask.mhd")
mask905 = image.image("vox/90pcmask5.mhd")

### init
tle1mm = tle.load_tledata(['vox/tle1mm'],[1e4],[mask901,maskspect1],ppstle1,yn4d,vn4d)
tle2mm = tle.load_tledata(['tle10k'],[1e4],[mask902,maskspect2],ppstle2,yn4d,vn4d)
tle5mm = tle.load_tledata(['vox/tle5mm'],[1e4],[mask905,maskspect5],ppstle5,yn4d,vn4d)
an1mm = tle.load_tledata(['vox/an1mm'],[1e7],[mask901,maskspect1],ppsan1,yn4d,vn4d)
an2mm = tle.load_tledata(['analog10M'],[1e7],[mask902,maskspect2],ppsan2,yn4d,vn4d)
an5mm = tle.load_tledata(['vox/an5mm'],[1e7],[mask905,maskspect5],ppsan5,yn4d,vn4d)

# to 3d
tle.to3d(tle1mm)
tle.to3d(tle2mm)
tle.to3d(tle5mm)
tle.to3d(an1mm)
tle.to3d(an2mm)
tle.to3d(an5mm)

# to eff, ratio
tle.seteff(tle1mm)
tle.seteff(tle2mm)
tle.seteff(tle5mm)
tle.seteff(an1mm)
tle.seteff(an2mm)
tle.seteff(an5mm)
tle.seteffratio(tle1mm,an1mm[1e7]['var'])
tle.seteffratio(tle2mm,an2mm[1e7]['var'])
tle.seteffratio(tle5mm,an5mm[1e7]['var'])


### speedup histo plot!
f, tl = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False)

#tle1mm[1e4]['var'].imdata = tle1mm[1e4]['var'].imdata*10.
a=tle.get_effhist(tl,tle1mm[1e4]['var'],r'$1^3$ mm$^3$ voxel')
b=tle.get_effhist(tl,tle2mm[1e4]['var'],r'$2^3$ mm$^3$ voxel')
c=tle.get_effhist(tl,tle5mm[1e4]['var'],r'$5^3$ mm$^3$ voxel')
print [a[1],b[1],c[1]]
#lmed2 = np.average([a[1],b[1],c[1]])
tl.axvline(a[1], color='#999999', ls='--')
tl.axvline(b[1], color='#999999', ls='--')
tl.axvline(c[1], color='#999999', ls='--')
tl.set_ylim([0,1.05])
tl.set_xlim([3e3,2e6])
#tl.set_title("Speedup distribution as function of voxelsize")
tl.legend(bbox_to_anchor=(1,1),frameon=False,prop={'size':6})
tl.set_ylabel('Number of voxels (scaled)')
tl.set_xlabel('Gain factor w.r.t. analog MC $10^7$ primaries')
f.savefig('voxelsizes.pdf', bbox_inches='tight')
f.savefig('voxelsizes.png', bbox_inches='tight',dpi=300)
plt.close('all')
