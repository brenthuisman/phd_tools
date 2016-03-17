#!/usr/bin/env python
import sys,copy,image,tle,plot,numpy as np,matplotlib.pyplot as plt,matplotlib as mpl

print >> sys.stderr, 'Processing'

### params
# ppsan = 314.248
# ppstle = 292.8
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
tle3d = tle.load_tledata(tledirs,tleprims,[mask90pc],ppstle,yn,vn)
an3d = tle.load_tledata(andirs,anprims,[mask90pc],ppsan,yn,vn)

tle4d = tle.load_tledata(tledirs,tleprims,[mask90pc,maskspect],ppstle,yn4d,vn4d)
an4d = tle.load_tledata(andirs,anprims,[mask90pc,maskspect],ppsan,yn4d,vn4d)
tle4dbeam = tle.load_tledata(tledirs,tleprims,[mask90pc,maskbeam,maskspect],ppstle,yn4d,vn4d)
an4dbeam = tle.load_tledata(andirs,anprims,[mask90pc,maskbeam,maskspect],ppsan,yn4d,vn4d)


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
#swapped left and right!!!!!!

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
tr.set_ylim([0,1.05])
tr.set_xlim([7e1,3e4])
tr.axvline(lmed, color='#999999', ls='--')
tr.legend(bbox_to_anchor=(1.2,1),frameon=False,prop={'size':6})

f.subplots_adjust(wspace=0.5)
f.savefig('reluncconv-effhisto.pdf', bbox_inches='tight')
plt.close('all')


### TMP check relunc dist
f, (tl,tr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
tle.get_effhist(tl,tlerelunc[1e6]['var'])
tle.get_effhist(tr,anrelunc[1e9]['var'])
f.savefig('relunc-dist.pdf', bbox_inches='tight')
plt.close('all')


### Make efficiency histo
tleeff = copy.deepcopy(tle3d)
aneff = copy.deepcopy(an3d)
tle.seteff(tleeff)
tle.seteff(aneff)

tle.seteffratio(tleeff,aneff[max(aneff.keys())]['var'])

f, ((tl,tr),(bl,br)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
lab1=tle.get_effhist(tl,tleeff[1e3]['var'])
lab2=tle.get_effhist(tr,tleeff[1e4]['var'])
lab3=tle.get_effhist(bl,tleeff[1e5]['var'])
lab4=tle.get_effhist(br,tleeff[1e6]['var'])

tl.set_title("TLE "+plot.sn_mag(1e3)).set_fontsize(8)
tl.text(0.05, 0.9,"Min: "+plot.sn(lab1[0])+"\nMedian: "+plot.sn(lab1[1])+"\nMax: "+plot.sn(lab1[2]), ha='left', va='center', transform=tl.transAxes, fontsize=6)
tr.set_title("TLE "+plot.sn_mag(1e4)).set_fontsize(8)
tr.text(0.05, 0.9,"Min: "+plot.sn(lab2[0])+"\nMedian: "+plot.sn(lab2[1])+"\nMax: "+plot.sn(lab2[2]), ha='left', va='center', transform=tr.transAxes, fontsize=6)
bl.set_title("TLE "+plot.sn_mag(1e5)).set_fontsize(8)
bl.text(0.05, 0.9,"Min: "+plot.sn(lab3[0])+"\nMedian: "+plot.sn(lab3[1])+"\nMax: "+plot.sn(lab3[2]), ha='left', va='center', transform=bl.transAxes, fontsize=6)
br.set_title("TLE "+plot.sn_mag(1e6)).set_fontsize(8)
br.text(0.05, 0.9,"Min: "+plot.sn(lab4[0])+"\nMedian: "+plot.sn(lab4[1])+"\nMax: "+plot.sn(lab4[2]), ha='left', va='center', transform=br.transAxes, fontsize=6)
tl.set_ylabel('Number of voxels (scaled)')
tl.yaxis.set_label_coords(-0.2, 0.)
bl.set_xlabel('Gain factor w.r.t. Reference')
bl.xaxis.set_label_coords(1.1,-0.2)

#f.savefig('eff-histo.pdf', bbox_inches='tight')
plt.close('all')


### Yield + reldiff plot
tle_yrd = tle4d #no deepcopy of 4D images
an_yrd = an4d
tle_yrd_beam = tle4dbeam
an_yrd_beam = an4dbeam
tle.setprojectiondata(tle_yrd,an_yrd[max(an_yrd.keys())])
tle.setprojectiondata(tle_yrd_beam,an_yrd_beam[max(an_yrd_beam.keys())])

f, ((tl,tr), (ml,mr), (bl,br) ) = plt.subplots(nrows=3, ncols=2, sharex=False, sharey=False)

tle.get_yield(tl,tle_yrd,an_yrd[max(an_yrd.keys())],'Z')
tle.get_yield(tr,tle_yrd,an_yrd[max(an_yrd.keys())],'E')
tle.get_reldiff(ml,tle_yrd,'Z')
tle.get_reldiff(mr,tle_yrd,'E')
tle.get_reldiff(bl,tle_yrd_beam,'Z')
tle.get_reldiff(br,tle_yrd_beam,'E')

# tl.xaxis.set_visible(False)
# tr.xaxis.set_visible(False)
# tr.yaxis.set_visible(False)
# ml.xaxis.set_visible(False)
# mr.xaxis.set_visible(False)
# mr.yaxis.set_visible(False)
# br.yaxis.set_visible(False)

tl.set_ylim([0,2.8e-3])
tr.set_ylim([0,2.8e-3])
ml.set_ylim([-2.5,2.5])
mr.set_ylim([-2.5,2.5])
bl.set_ylim([-5,5])
br.set_ylim([-5,5])

tl.set_ylabel('Integrated Yield\n[PG/proton/voxel]')
tl.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.set_ylabel('Integrated\nRel. Diff.[\%]')
ml.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
bl.set_ylabel('Voxels beam path\nRel. Diff.[\%]')
bl.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
bl.set_xlabel('Depth [mm]')
br.set_xlabel('PG energy [MeV]')

lgd=tr.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.subplots_adjust(hspace=0.3)
f.savefig('yield-reldiff.pdf', bbox_inches='tight')
plt.close('all')


### Todo: eff slice
#http://www.scipy-lectures.org/intro/matplotlib/auto_examples/plot_imshow_ex.html
#tlevarim.saveslice('x',21)
#anvarim.saveslice('x',21)
#tleslice = tle10kvar.saveslice('y',21)
#anslice = an10Mvar.saveslice('y',21)

# with np.errstate(divide='ignore', invalid='ignore'):
# 	c=tleslice/anslice
# 	c[c == np.nan] = 0
# 	c[c == np.inf] = 0
# 	c.tofile('ratio.raw')
#todo print eff in that voxel
#opt: sum eff over some voxels
#opt: save a 2dtop projection of eff.

#repeat for a few sets of data, and then plot
