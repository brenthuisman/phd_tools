#!/usr/bin/env python
import sys,copy,image,tle,plot,numpy as np,matplotlib.pyplot as plt,matplotlib as mpl

print >> sys.stderr, 'Processing'

### params
ppsan = (72.2114+71.9978)/2
ppstle = (68.1091+69.5367)/2
yn = 'mean3d.mhd' #yieldname
vn = 'var3d.mhd' #varname
yn4d = 'mean4d.mhd' #yieldname
vn4d = 'var4d.mhd' #varname

### tledata
tleprims = [1e3,1e4,1e5,1e6]
tledirs = ['tle1k','tle10k','tle100k','tle1M']
# tleprims = [1e3,1e4,1e5,1e6,1e7]
# tledirs = ['tle1k','tle10k','tle100k','tle1M','tle10M']

### analog
anprims = [1e6,1e7,1e8,1e9]
andirs = ['analog1M','analog10M','analog100M','analog1B']

### helpers, masks
mask90pc = image.image("analog1B/mean3d.mhd")
mask90pc.to90pcmask()
#mask90pc.save90pcmask()
maskspect = image.image("mask-spect1-8/finalmask.mhd")
# labelim = image.image("labelim/labelimage.mhd")
patient = image.image("patient/pattest.mhd")
# patient.applymask(mask90pc)

### init
tle3d = tle.load_tledata(tledirs,tleprims,[mask90pc],ppstle,yn,vn)
an3d = tle.load_tledata(andirs,anprims,[mask90pc],ppsan,yn,vn)

tle4d = tle.load_tledata(tledirs,tleprims,[mask90pc,maskspect],ppstle,yn4d,vn4d)
an4d = tle.load_tledata(andirs,anprims,[mask90pc,maskspect],ppsan,yn4d,vn4d)


### plot relunc convergence
tlerelunc = copy.deepcopy(tle3d)
anrelunc = copy.deepcopy(an3d)
tle.setrelunc(tlerelunc)
tle.setrelunc(anrelunc)

tleeff = copy.deepcopy(tle3d)
aneff = copy.deepcopy(an3d)
tle.seteff(tleeff)
tle.seteff(aneff)
tle.seteffratio(tleeff,aneff[max(aneff.keys())]['var'])

f, (tr,tl) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
#swapped

#Relative uncertainties 90pc region
x_tle = np.array(tlerelunc.keys())
# y_tle = [np.nansum(value['var'].imdata/np.sum(mask90pc.imdata)) for key, value in tlerelunc.iteritems()]
y_tle = [np.median(value['var'].imdata[~np.isnan(value['var'].imdata)]) for key, value in tlerelunc.iteritems()]
tle_2pc = tle.get_reluncconv(tl,x_tle/ppstle,y_tle)

x_an = np.array(anrelunc.keys())
# y_an = [np.nansum(value['var'].imdata/np.sum(mask90pc.imdata)) for key, value in anrelunc.iteritems()]
y_an = [np.median(value['var'].imdata[~np.isnan(value['var'].imdata)]) for key, value in anrelunc.iteritems()]
an_2pc = tle.get_reluncconv(tl,x_an/ppsan,y_an)

tl.set_title('Median relative uncertainty\nGain: '+plot.sn(an_2pc/tle_2pc))
tl.set_ylabel('Relative Uncertainty [\%]')
tl.set_xlabel('Runtime t [s]')
tl.semilogx()
tl.legend(bbox_to_anchor=(1.1, 1),frameon=False,prop={'size':6})

#efficiencies + speedups
a=tle.get_effhist(tr,tleeff[1e3]['var'])
b=tle.get_effhist(tr,tleeff[1e4]['var'])
c=tle.get_effhist(tr,tleeff[1e5]['var'])
d=tle.get_effhist(tr,tleeff[1e6]['var'])
lmin = min([a[0],b[0],c[0],d[0]])
lmed = np.average([a[1],b[1],c[1],d[1]])
lmax = max([a[2],b[2],c[2],d[2]])
lmean = np.average([a[3],b[3],c[3],d[3]])
print 'Glob mean/median:',lmean,lmed

tr.set_title('vpgTLE gain distribution\nMedian gain: '+plot.sn(lmed))
tr.set_ylabel('Number of voxels (scaled)')
tr.set_xlabel('Gain factor w.r.t. Reference')
tr.set_ylim([0,1.1])
tr.set_xlim([5e1,2e4])
tr.axvline(lmed, color='#999999', ls='--')
tr.legend(bbox_to_anchor=(1.2,1),frameon=False,prop={'size':6})

f.subplots_adjust(wspace=0.5)
f.savefig('reluncconv-effhisto.pdf', bbox_inches='tight')
f.savefig('reluncconv-effhisto.png', bbox_inches='tight',dpi=300)
plt.close('all')


### Yield + reldiff plot
tle_yrd = tle4d #no deepcopy of 4D images
an_yrd = an4d
# tle_yrd_beam = tle4dbeam
# an_yrd_beam = an4dbeam
tle.setprojectiondata(tle_yrd,an_yrd[max(an_yrd.keys())],'head')
# tle.setprojectiondata(tle_yrd_beam,an_yrd_beam[max(an_yrd_beam.keys())],'head')

f, ((tl,tr), (ml,mr)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

tle.get_yield(tl,tle_yrd,an_yrd[max(an_yrd.keys())],'Y','head')
tle.get_yield(tr,tle_yrd,an_yrd[max(an_yrd.keys())],'E','head')
tle.get_reldiff(ml,tle_yrd,'Y','head')
tle.get_reldiff(mr,tle_yrd,'E','head')

# tl.xaxis.set_visible(False)
# tr.xaxis.set_visible(False)
# tr.yaxis.set_visible(False)
# mr.yaxis.set_visible(False)

tl.axvline(16, color='#999999', ls='--')
ml.axvline(16, color='#999999', ls='--')

tl.set_ylim([0,2.1e-3])
tr.set_ylim([0,2.1e-3])
ml.set_ylim([-2.5,2.5])
mr.set_ylim([-2.5,2.5])
# bl.set_ylim([-5,5])
# br.set_ylim([-5,5])

tl.set_ylabel('Integrated Yield\n[PG/proton/voxel]')
tl.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.set_ylabel('Integrated\nRel. Diff.[\%]')
ml.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.set_xlabel('Depth [mm]')
mr.set_xlabel('PG energy [MeV]')

lgd=tr.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.subplots_adjust(hspace=0.3)
f.savefig('yield-reldiff.pdf', bbox_inches='tight')
f.savefig('yield-reldiff.png', bbox_inches='tight',dpi=300)
plt.close('all')


### Speedup slice + material slice

speedim = tleeff[1e6]['var'].getslice('z',21)
ctim = patient.getslice('z',21)
# ctim[ctim == 0] = np.nan
f, (tl,tr) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
# tleeff[1e6]['var'].saveas('speedup.mhd')
tl.imshow(speedim,interpolation='nearest',origin='lower',norm = mpl.colors.LogNorm(),cmap="hot",clim=[500,5000])
pica=tr.imshow(speedim,interpolation='nearest',origin='lower',norm = mpl.colors.LogNorm(),cmap="hot",clim=[500,5000])
tr.imshow(ctim,interpolation='nearest', origin='lower',cmap="gray",alpha=0.5)
tl.set_ylim([5,75])
tr.set_ylim([5,75])
tl.set_xlim([5,30])
tr.set_xlim([5,30])
tr.yaxis.set_visible(False)
tl.set_ylabel('Depth [mm]')
tl.set_xlabel('Width [mm]')
tr.set_xlabel('Width [mm]')
tl.set_title(r'Gain vpgTLE $10^6$'+'\n w.r.t. Reference')
tr.set_title('CT Image')
plot.texax(tl)
plot.texax(tr)
f.colorbar(pica)

# f.colorbar(tl,shrink=.92)
f.savefig('slice1.pdf', bbox_inches='tight')
plt.close('all')


### Speedup slice + material slice

speedim = tleeff[1e6]['var'].getslice('x',14)
ctim = patient.getslice('x',14)
#ctim[ctim == 0] = np.nan
f, (tl,tr) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
pica=tl.imshow(speedim,interpolation='nearest',origin='lower',norm = mpl.colors.LogNorm(),cmap="hot")
tr.imshow(ctim,interpolation='nearest', origin='lower',cmap="gray")
tl.set_ylim([0,30])
tr.set_ylim([0,30])
# tl.set_xlim([5,30])
# tr.set_xlim([5,30])
tl.xaxis.set_visible(False)
tl.set_ylabel('Depth [mm]')
tr.set_ylabel('Depth [mm]')
tr.set_xlabel('Heigth [mm]')
tl.set_title(r'Gain vpgTLE $10^6$'+'\n w.r.t. Reference')
tr.set_title('CT Image')
plot.texax(tl)
plot.texax(tr)
f.colorbar(pica)

# f.colorbar(tl,shrink=.92)
f.savefig('slice2.pdf', bbox_inches='tight')
plt.close('all')


### range-energy plot
ranegy = tle4d[1e6]['yield']
outpostfix = ".2dyekine"
crush = [1,0,1,0]
ranegy.toprojection(outpostfix, crush)
ranegy.imdata = ranegy.imdata.reshape(ranegy.imdata.shape[::-1])
print "Set axes to",(0,ranegy.imdata.shape[0]/2.,0,10)
f, tl = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
pica=tl.imshow(ranegy.imdata.T,interpolation='nearest',origin='lower',cmap="hot",aspect='auto',extent=(0,10,0,ranegy.imdata.shape[0]/2.))
#tl.set_ylim([0,30])
#tl.xaxis.set_visible(False)
tl.set_ylabel('Depth [mm]')
tl.set_xlabel('PG energy [MeV]')
#tl.set_title('CT Image')
plot.texax(tl)

cb = f.colorbar(pica)
cb.set_label("PG yield (PG/proton)")

# f.colorbar(tl,shrink=.92)
f.savefig('range-energy.pdf', bbox_inches='tight')
plt.close('all')