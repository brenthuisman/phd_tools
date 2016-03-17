#!/usr/bin/env python
import sys,copy,image,tle,plot,numpy as np,matplotlib.pyplot as plt,matplotlib as mpl,pickle
from math import sqrt

print >> sys.stderr, 'Processing'

### params
# ppsan = 314.248
# ppstle = 292.8
ppsan = (211.926+211.511)/2
ppstle = (199.421+200.71)/2
yn = 'mean3d.mhd' #yieldname
vn = 'var3d.mhd' #varname

### tledata
tleprims = [1e3,1e4,1e5,1e6]
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

### init
tle3d = tle.load_tledata(tledirs,tleprims,[mask90pc],ppstle,yn,vn)
an3d = tle.load_tledata(andirs,anprims,[mask90pc],ppsan,yn,vn)

tle_d = pickle.load(open("../../jm-method/parodi/sum.pydict"))['tle']
an_d = pickle.load(open("../../jm-method/parodi/sum.pydict"))['analog']

### plot relunc convergence
tleeff = copy.deepcopy(tle3d)
aneff = copy.deepcopy(an3d)
tle.seteff(tleeff)
tle.seteff(aneff)
tle.seteffratio(tleeff,aneff[max(aneff.keys())]['var'])

f, (tr,tl) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
#swapped left and right!!!!!!

#Relative uncertainties 90pc region

x_tle = np.array(tle_d.keys())
y_tle = [sqrt(value['var'][0])/value['yield'][0] for key, value in tle_d.iteritems()]
tle_2pc = tle.get_reluncconv(tl,x_tle/ppstle,y_tle)

x_an = np.array(an_d.keys())
y_an = [sqrt(value['var'][0])/value['yield'][0] for key, value in an_d.iteritems()]
an_2pc = tle.get_reluncconv(tl,x_an/ppsan,y_an)

tl.set_title('Median relative uncertainty\nGain: '+plot.sn(an_2pc/tle_2pc))
tl.set_ylabel('Relative Uncertainty [\%]')
tl.set_xlabel('Runtime [s]')
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
