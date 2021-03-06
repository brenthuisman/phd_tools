#!/usr/bin/env python
import image,numpy as np,auger,plot,dump
from scipy.ndimage.filters import gaussian_filter

###########################################################################################################

volume_offset=-149#waterbox sources

pgsrc_ct = image.image('stage2/data/source-139.mhd')
pgsrc_ct.toprojection(".x", [0,1,1,1])
pgsrc_ct_y = pgsrc_ct.imdata/pgsrc_ct.imdata.max()
pgsrc_rpct = image.image('stage2/data/source-144.mhd')
pgsrc_rpct.toprojection(".x", [0,1,1,1])
pgsrc_rpct_y = pgsrc_rpct.imdata/pgsrc_rpct.imdata.max()

pgsrc_ct_x = np.linspace(-149,149,150) #bincenters
pgsrc_ct_xhist = np.linspace(-150,150,151) #2mm voxels, endpoints
pgsrc_ct_x = pgsrc_ct_x+(volume_offset-pgsrc_ct_x[0])   #offset for pg source image
pgsrc_ct_xhist = pgsrc_ct_xhist+(volume_offset-pgsrc_ct_xhist[0]) #same

pgsrc_rpct_x = pgsrc_ct_x #is nu hetzelfde
pgsrc_rpct_xhist = pgsrc_ct_xhist

pgsrc_ctfo=auger.get_fop(pgsrc_ct_x,pgsrc_ct_y)
pgsrc_rpctfo=auger.get_fop(pgsrc_rpct_x,pgsrc_rpct_y)

###########################################################################################################

#emission in worldframe
smooth_param = 20 #IBA: 20, Priegnitz 2015

pgemis_ct = dump.thist2np_xy('fromcluster/run.8ZQJ/output.2399064/GammProdCount-Prod.root')
pgemis_rpct = dump.thist2np_xy('fromcluster/run.ahDK/output.2399464/GammProdCount-Prod.root')
pgemis_ct_x = np.array(pgemis_ct['histo'][0])
pgemis_ct_y = np.array(pgemis_ct['histo'][1])
pgemis_ct_y = pgemis_ct_y/pgemis_ct_y.max()
pgemis_rpct_x = np.array(pgemis_rpct['histo'][0])
pgemis_rpct_y = np.array(pgemis_rpct['histo'][1])
pgemis_rpct_y = pgemis_rpct_y/pgemis_rpct_y.max()

pgemis_ct_y_smooth = gaussian_filter(pgemis_ct_y, sigma=10)
pgemis_ct_y_smooth = pgemis_ct_y_smooth/pgemis_ct_y_smooth.max()
pgemis_rpct_y_smooth = gaussian_filter(pgemis_rpct_y, sigma=10)
pgemis_rpct_y_smooth = pgemis_rpct_y_smooth/pgemis_rpct_y_smooth.max()

pgemis_ctfo=auger.get_fop(pgemis_ct_x,pgemis_ct_y)
pgemis_rpctfo=auger.get_fop(pgemis_rpct_x,pgemis_rpct_y)

pgemis_smooth_ctfo=auger.get_fop(pgemis_ct_x,pgemis_ct_y_smooth)
pgemis_smooth_rpctfo=auger.get_fop(pgemis_rpct_x,pgemis_rpct_y_smooth)


pgemis_ct_y_smooth20 = gaussian_filter(pgemis_ct_y, sigma=20)
pgemis_ct_y_smooth20 = pgemis_ct_y_smooth20/pgemis_ct_y_smooth20.max()
pgemis_smooth20_ctfo=auger.get_fop(pgemis_ct_x,pgemis_ct_y_smooth20)

###########################################################################################################

#detection in local frame, remove shift. coords already centered as zero, so can just add the shift

det_offset = -17.31

ipnl = auger.getctset(1e9,'fromcluster/run.8ZQJ','fromcluster/run.ahDK','ipnl-auger-tof-1.root')

pgipnl_ct_x = np.array(ipnl['ct']['x'])
pgipnl_ct_x = pgipnl_ct_x+det_offset
pgipnl_ct_y = np.array(ipnl['ct']['av'])
pgipnl_ct_y = pgipnl_ct_y-(pgipnl_ct_y[pgipnl_ct_y < np.percentile(pgipnl_ct_y, 25)].mean())  #remove floor
pgipnl_ct_y = pgipnl_ct_y/pgipnl_ct_y.max() #scale

pgipnl_rpct_x = np.array(ipnl['rpct']['x'])
pgipnl_rpct_x = pgipnl_rpct_x+det_offset
pgipnl_rpct_y = np.array(ipnl['rpct']['av'])
pgipnl_rpct_y = pgipnl_rpct_y-(pgipnl_rpct_y[pgipnl_rpct_y < np.percentile(pgipnl_rpct_y, 25)].mean()) #remove floor
pgipnl_rpct_y = pgipnl_rpct_y/pgipnl_rpct_y.max() #scale

pgipnl_ctfo = np.mean(ipnl['ct']['falloff'])+det_offset
pgipnl_rpctfo = np.mean(ipnl['rpct']['falloff'])+det_offset


iba = auger.getctset(1e9,'fromcluster/run.8ZQJ','fromcluster/run.ahDK','iba-auger-notof-3.root')

pgiba_ct_x = np.array(iba['ct']['x'])
pgiba_ct_x = pgiba_ct_x+det_offset
pgiba_ct_y = np.array(iba['ct']['av'])
pgiba_ct_y = pgiba_ct_y-(pgiba_ct_y[pgiba_ct_y < np.percentile(pgiba_ct_y, 25)].mean())  #remove floor
pgiba_ct_y = pgiba_ct_y/pgiba_ct_y.max() #scale

pgiba_rpct_x = np.array(iba['rpct']['x'])
pgiba_rpct_x = pgiba_rpct_x+det_offset
pgiba_rpct_y = np.array(iba['rpct']['av'])
pgiba_rpct_y = pgiba_rpct_y-(pgiba_rpct_y[pgiba_rpct_y < np.percentile(pgiba_rpct_y, 25)].mean())  #remove floor
pgiba_rpct_y = pgiba_rpct_y/pgiba_rpct_y.max() #scale

pgiba_ctfo = np.mean(iba['ct']['falloff'])+det_offset
pgiba_rpctfo = np.mean(iba['rpct']['falloff'])+det_offset


###########################################################################################################

f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)

#ax1.step(pgsrc_ct_x,pgsrc_ct_y, color='steelblue',lw=1., alpha=0.2, label='PGSRC FOP: '+str(pgsrc_ctfo), where='mid')
#ax1.step(pgsrc_rpct_x,pgsrc_rpct_y, color='indianred',lw=1., alpha=0.2, label='PGSRC RPCT FOP: '+str(pgsrc_rpctfo), where='mid')

ax1.step(pgemis_ct_x,pgemis_ct_y, color='steelblue',lw=1., alpha=0.6, label='Prod FOP:\n'+str(pgemis_ctfo)[:5], where='mid')
#ax1.step(pgemis_rpct_x,pgemis_rpct_y, color='indianred',lw=1., alpha=0.4, label='PROD RPCT FOP: '+str(pgemis_rpctfo), where='mid')

ax1.step(pgemis_ct_x,pgemis_ct_y_smooth, color='seagreen',lw=1., alpha=0.6, label='Prod PSF10 FOP:\n'+str(pgemis_smooth_ctfo)[:5], where='mid')
#ax1.step(pgemis_rpct_x,pgemis_rpct_y_smooth, color='indianred',lw=1., alpha=0.6, label='PROD SMOOTH RPCT FOP: '+str(pgemis_smooth_rpctfo), where='mid')
ax1.plot(pgemis_ct_x, pgemis_ct_y_smooth20, linestyle='--', drawstyle='steps-mid', color='seagreen',lw=1., alpha=0.6, label='Prod PSF20 FOP:\n'+str(pgemis_smooth20_ctfo)[:5])

pgipnl_ctfo = auger.get_fop(pgipnl_ct_x,pgipnl_ct_y,plot=True,ax=ax1,label='Detected Smooth ')
#ax1.step(pgipnl_ct_x,pgipnl_ct_y, color='indianred',lw=1., alpha=0.8, label='PGIPNL FOP:\n'+str(pgipnl_ctfo)[:5], where='mid')
#ax1.step(pgipnl_rpct_x,pgipnl_rpct_y, color='indianred',lw=1., alpha=0.8, label='PGIPNL RPCT FOP: '+str(pgipnl_rpctfo), where='mid')


# CT WITHOUT SMOOTHING

ax2.step(pgemis_ct_x,pgemis_ct_y, color='steelblue',lw=1., alpha=0.6, label='Prod FOP:\n'+str(pgemis_ctfo)[:5], where='mid')
#ax1.step(pgemis_rpct_x,pgemis_rpct_y, color='indianred',lw=1., alpha=0.4, label='PROD RPCT FOP: '+str(pgemis_rpctfo), where='mid')

ax2.step(pgemis_ct_x,pgemis_ct_y_smooth, color='seagreen',lw=1., alpha=0.6, label='Prod Smooth FOP:\n'+str(pgemis_smooth_ctfo)[:5], where='mid')
#ax1.step(pgemis_rpct_x,pgemis_rpct_y_smooth, color='indianred',lw=1., alpha=0.6, label='PROD SMOOTH RPCT FOP: '+str(pgemis_smooth_rpctfo), where='mid')
ax2.plot(pgemis_ct_x, pgemis_ct_y_smooth20, linestyle='--', drawstyle='steps-mid', color='seagreen',lw=1., alpha=0.6, label='Prod PSF20 FOP:\n'+str(pgemis_smooth20_ctfo)[:5])

pgipnl_ctfo = auger.get_fop(pgipnl_ct_x,pgipnl_ct_y,plot=True,ax=ax2,smooth=False,label='Detected ')
#ax2.step(pgipnl_ct_x,pgipnl_ct_y, color='indianred',lw=1., alpha=0., label='PGIPNL FOP:\n'+str(pgipnl_ctfo)[:5], where='mid')
#ax1.step(pgipnl_rpct_x,pgipnl_rpct_y, color='indianred',lw=1., alpha=0.8, label='PGIPNL RPCT FOP: '+str(pgipnl_rpctfo), where='mid')




########################################### rpct:

##ax2.step(pgsrc_ct_x,pgsrc_ct_y, color='steelblue',lw=1., alpha=0.2, label='PGSRC FOP: '+str(pgsrc_ctfo), where='mid')
##ax2.step(pgsrc_rpct_x,pgsrc_rpct_y, color='indianred',lw=1., alpha=0.2, label='PGSRC RPCT FOP: '+str(pgsrc_rpctfo), where='mid')

#ax2.step(pgemis_ct_x,pgemis_ct_y, color='steelblue',lw=1., alpha=0.4, label='PROD FOP: '+str(pgemis_ctfo), where='mid')
##ax2.step(pgemis_rpct_x,pgemis_rpct_y, color='indianred',lw=1., alpha=0.4, label='PROD RPCT FOP: '+str(pgemis_rpctfo), where='mid')

#ax2.step(pgemis_ct_x,pgemis_ct_y_smooth, color='steelblue',lw=1., alpha=0.6, label='PROD SMOOTH FOP: '+str(pgemis_smooth_ctfo), where='mid')
##ax2.step(pgemis_rpct_x,pgemis_rpct_y_smooth, color='indianred',lw=1., alpha=0.6, label='PROD SMOOTH RPCT FOP: '+str(pgemis_smooth_rpctfo), where='mid')

#ax2.step(pgiba_ct_x,pgiba_ct_y, color='steelblue',lw=1., alpha=0.8, label='PGIBA FOP: '+str(pgiba_ctfo), where='mid')
##ax2.step(pgiba_rpct_x,pgiba_rpct_y, color='indianred',lw=1., alpha=0.8, label='PGIBA RPCT FOP: '+str(pgiba_rpctfo), where='mid')

ax1.set_xlim(-50,50)
ax2.set_xlim(-50,50)

ax1.legend(frameon = False,loc='upper right')
ax2.legend(frameon = False,loc='upper right')
plot.texax(ax1)
plot.texax(ax2)

f.savefig('pgevo3-waterbox.pdf', bbox_inches='tight')
plot.close('all')

